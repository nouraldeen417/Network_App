import ansible_runner
import json
import re

class Facts:
    class Interface:
        def __init__(self, name, address_subnet, status):
            self.name = name
            self.address_subnet = address_subnet
            self.status = status


    class Neighbor:
        def __init__(self, name, address_subnet ,port):
            self.name = name
            self.address_subnet = address_subnet
            self.port = port

    class Routing:
        def __init__(self, protocol, net ,intf):
            self.protocol = protocol
            self.network = net
            self.interface = intf
    def __init__(self, id, device, interfaces, neighbors,routing_tables):
        self.id = id
        self.device = device
        self.interfaces = [self.Interface(*interface) for interface in interfaces]  # List of Interface objects
        self.neighbors = [self.Neighbor(*neighbor) for neighbor in neighbors]  # List of Neighbor objects
        self.routing = [self.Routing(*routing_table) for routing_table in routing_tables]  # List of Neighbor objects

def Routers_facts():
    r = ansible_runner.run(
    private_data_dir="../ansible/",  # Current directory
    playbook="playbooks/routers.yaml",
    inventory="hosts",  # Path to external inventory file
    rotate_artifacts=1
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
           facts[0].neighbors[0].name,
           facts[0].neighbors[0].address_subnet,
           facts[0].neighbors[0].port,
           facts[0].routing[0].protocol,           
           facts[0].routing[1].protocol)
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
        temp.append([i,dict[i]["ipv4"],dict[i]["lineprotocol"]])
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
        "R": "RIP",
        "B": "BGP",
        "D": "EIGRP",
    }

    routes = []
    lines = output.splitlines()
    # Regex to match routing table entries
    route_pattern = re.compile(
        r"^\s*(?P<protocol>\w+)\s+"
        r"(?P<network>[\d./]+)\s+"
        r"is directly connected,\s+"
        r"(?P<interface>\S+)"
    )

    for line in lines:
        match = route_pattern.search(line)
        if match:
            protocol_code = match.group("protocol")
            network = match.group("network")
            interface = match.group("interface")

            # Map protocol code to human-readable description
            protocol = protocol_map.get(protocol_code, f"Unknown ({protocol_code})")

            # Append the parsed data as a list
            routes.append([protocol, network, interface])

    return routes

# Routers_facts()
