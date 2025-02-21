import ansible_runner
import json
import re

class Facts:
    class Interface:
        def __init__(self, name, address_subnet, status,description):
            self.name = name
            self.address_subnet = address_subnet
            self.status = status
            self.description=description


    class Neighbor:
        def __init__(self, name, address_subnet ,port):
            self.name = name
            self.address_subnet = address_subnet
            self.port = port

    class Routing:
        def __init__(self, protocol, net ,intf,next_hop,admin_distance):
            self.protocol = protocol
            self.network = net
            self.interface = intf
            self.next_hop=next_hop
            self.admin_distance=admin_distance
    def __init__(self, id, device, interfaces, neighbors,routing_tables):
        self.id = id
        self.device = device
        self.interfaces = [self.Interface(*interface) for interface in interfaces]  # List of Interface objects
        self.neighbors = [self.Neighbor(*neighbor) for neighbor in neighbors]  # List of Neighbor objects
        self.routing = [self.Routing(*routing_table) for routing_table in routing_tables]  # List of Neighbor objects

def Routers_facts():
    r = ansible_runner.run(
    private_data_dir="../ansible/",  # Current directory
    playbook="playbooks/device.yaml",
    inventory="hosts",  # Path to external inventory file
    tags="routers",
    rotate_artifacts=1,        
    extravars={                              # Pass the selected role as a variable
        "target_hosts": 'routers'}
    )
    # Get the list of hosts where tasks ran
    hosts_with_tasks = [host for host in  r.stats["ok"]]
    facts = []
    # Print the hosts where tasks were executed

    for host in hosts_with_tasks:
        facts_file = "../ansible/temp/router_facts_" + host + ".json"

        with open(facts_file, "r") as f:
            router_facts = json.load(f)
        # print(router_interface_list(router_facts["net_interfaces"]))    
        routing_table_output = router_facts["routing_table"]["stdout"][0]

        facts.append(Facts(id=host ,device=router_facts["net_hostname"], 
                           interfaces=router_interface_list(router_facts["net_interfaces"]),
                           neighbors=router_neighbor_list(router_facts["net_neighbors"]),
                           routing_tables=parse_routing_table(routing_table_output)))


    print (facts[0].id,
           facts[0].device , 
           facts[0].interfaces[0].name , 
           facts[0].interfaces[0].address_subnet ,
           facts[0].interfaces[0].status ,
           facts[0].interfaces[0].description ,
           facts[0].neighbors[0].name,
           facts[0].neighbors[0].address_subnet,
           facts[0].neighbors[0].port,
           facts[0].routing[0].protocol,           
           facts[0].routing[1].protocol,
           facts[0].routing[0].next_hop,
           facts[0].routing[0].admin_distance)
    print("\n")
    # print (facts[1].id,
    #        facts[1].device , 
    #        facts[1].interfaces[1].name , 
    #        facts[1].interfaces[1].address_subnet ,
    #        facts[1].interfaces[1].status ,
    #        facts[1].neighbors[0].name,
    #        facts[1].neighbors[0].address_subnet,
    #        facts[1].neighbors[0].port)
    return facts

def router_interface_list(dict):
    temp =[]
    for i in dict:
        temp.append([i,dict[i]["ipv4"],dict[i]["lineprotocol"],dict[i]["description"]])
    return temp    

def router_neighbor_list(dict):
    temp =[]
    for i in dict:
        for j in dict[i]:
            temp.append([j["host"],j["ip"],j["port"]])
    return temp    



def parse_routing_table(output):
    # Map protocol codes to human-readable descriptions
    protocol_map = {
        "C": "Direct Connected",
        "L": "Local",
        "S": "Static",
        "O": "OSPF",
        "O IA": "OSPF Inter-Area",
        "O E1": "OSPF External Type 1",
        "O E2": "OSPF External Type 2",
        "R": "RIP",
        "B": "BGP",
        "D": "EIGRP",
        "*": "Default",
    }

    routes = []
    lines = output.splitlines()

    # Regex to match routing table entries
    route_pattern = re.compile(
        r"^\s*(?P<protocol>\*?[A-Za-z0-9\s]+?)\s+"  # Protocol (may include * for default routes)
        r"(?P<network>[\d./]+)\s+"                 # Network (e.g., 192.168.1.0/24)
        r"(?:\[(?P<admin_distance>\d+)/(?P<metric>\d+)\])?\s*"  # Admin distance and metric (optional)
        r"(?:via\s+(?P<next_hop>[\d.]+))?\s*"      # Next hop (optional)
        r"(?:,\s+(?P<uptime>[\w\s]+))?\s*"         # Uptime (optional)
        r"(?:,\s+(?P<interface>\S+))?"             # Interface (optional)
    )

    # Regex to match variably subnetted lines
    subnetted_pattern = re.compile(
        r"^\s*(?P<protocol>[CL])\s+"               # Protocol (C or L)
        r"(?P<network>[\d./]+)\s+"                 # Network (e.g., 192.168.1.0/24)
        r"is directly connected,\s+"               # Static text
        r"(?P<interface>\S+)"                      # Interface
    )

    for line in lines:
        # Skip the "Gateway of last resort" line
        if "Gateway of last resort" in line:
            continue

        # Skip the "variably subnetted" lines (they are not actual routes)
        if "variably subnetted" in line:
            continue

        # Check if the line matches a routing table entry
        match = route_pattern.search(line)
        if match:
            protocol_code = match.group("protocol").strip()
            network = match.group("network")
            next_hop = match.group("next_hop") or "Directly Connected"
            interface = match.group("interface") or "N/A"
            admin_distance = match.group("admin_distance") or "N/A"

            # Map protocol code to human-readable description
            protocol = protocol_map.get(protocol_code, f"Unknown ({protocol_code})")

            # Append the parsed data as a list
            routes.append([
                protocol,
                network,
                next_hop,
                interface,
                admin_distance
                                        ])
        else:
            # Check if the line matches a variably subnetted entry
            subnetted_match = subnetted_pattern.search(line)
            if subnetted_match:
                protocol_code = subnetted_match.group("protocol").strip()
                network = subnetted_match.group("network")
                interface = subnetted_match.group("interface")

                # Map protocol code to human-readable description
                protocol = protocol_map.get(protocol_code, f"Unknown ({protocol_code})")

                # Append the parsed data as a list
                routes.append([
                    protocol,
                    network,
                    "Directly Connected",
                    interface,
                    "N/A"
                ])

    return routes

# def parse_routing_table(output):
#     # Map protocol codes to human-readable descriptions
#     protocol_map = {
#         "C": "Direct Connected",
#         "L": "Local",
#         "S": "Static",
#         "O": "OSPF",
#         "R": "RIP",
#         "B": "BGP",
#         "D": "EIGRP",
#     }

#     routes = []
#     lines = output.splitlines()
#     # Regex to match routing table entries
#     route_pattern = re.compile(
#         r"^\s*(?P<protocol>\w+)\s+"
#         r"(?P<network>[\d./]+)\s+"
#         r".*,\s+"
#         r"(?P<interface>\S+)"
#     )

#     for line in lines:
#         match = route_pattern.search(line)
#         if match:
#             protocol_code = match.group("protocol")
#             network = match.group("network")
#             interface = match.group("interface")

#             # Map protocol code to human-readable description
#             protocol = protocol_map.get(protocol_code, f"Unknown ({protocol_code})")

#             # Append the parsed data as a list
#             routes.append([protocol, network, interface])

#     return routes

Routers_facts()
