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

    class Vlan:
        def __init__(self, id, name ,status,port):
            self.id = id
            self.name = name
            self.status = status
            self.port=port

    def __init__(self, id, device, interfaces, neighbors,vlans):
        self.id = id
        self.device = device
        self.interfaces = [self.Interface(*interface) for interface in interfaces]  # List of Interface objects
        self.neighbors  = [self.Neighbor(*neighbor) for neighbor in neighbors]      # List of Neighbor objects
        self.vlans      = [self.Vlan(*vlan) for vlan in vlans]                      # List of Neighbor objects

def switches_facts():
    r = ansible_runner.run(
    private_data_dir="../ansible/",  # Current directory
    playbook="playbooks/device.yaml",
    inventory="hosts",  # Path to external inventory file
    tags="switches",
    rotate_artifacts=1,
    extravars={                              # Pass the selected role as a variable
        "target_hosts": 'switches'}
    )
    # Get the list of hosts where tasks ran
    hosts_with_tasks = [host for host in  r.stats["ok"]]
    facts = []
    # Print the hosts where tasks were executed

    for host in hosts_with_tasks:
        facts_file = "../ansible/temp/switch_facts_" + host + ".json"

        with open(facts_file, "r") as f:
            router_facts = json.load(f)
        vlan_output = router_facts["vlans"]["stdout"][0]
        facts.append(Facts(id=host ,device=router_facts["net_hostname"], 
                           interfaces=router_interface_list(router_facts["net_interfaces"]),
                           neighbors=router_neighbor_list(router_facts["net_neighbors"]),
                           vlans=parse_vlan_table(vlan_output)))
                        
    print (facts[0].id,
           facts[0].device , 
           facts[0].interfaces[0].name , 
           facts[0].interfaces[0].address_subnet ,
           facts[0].interfaces[0].status ,
           facts[0].interfaces[0].description ,
           facts[0].neighbors[0].name,
           facts[0].neighbors[0].address_subnet,
           facts[0].neighbors[0].port,
           facts[0].vlans[0].id,
           facts[0].vlans[0].name,
           facts[0].vlans[0].status,
           facts[0].vlans[0].port)
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

def parse_vlan_table(output):
    # Initialize a list to store VLAN information
    vlans = []
    
    # Split the output into lines
    lines = output.splitlines()
    
    # Regex to match VLAN entries
    vlan_pattern = re.compile(
        r"^(?P<vlan_id>\d+)\s+"          # VLAN ID
        r"(?P<name>\S+)\s+"              # VLAN Name
        r"(?P<status>\S+)\s*"            # Status
        r"(?P<ports>.*)$",               # Ports (optional)
        re.MULTILINE
    )
    
    # Temporary variable to track the current VLAN
    current_vlan = None
    
    # Iterate through each line
    for line in lines:
        # Skip lines that are part of the header or footer
        if re.match(r"^\s*VLAN Name\s+Status\s+Ports", line) or re.match(r"^-+", line):
            continue
        
        # Check if the line matches a VLAN entry
        match = vlan_pattern.search(line)
        if match:
            # If there's a current VLAN being processed, add it to the list
            if current_vlan:
                vlans.append(current_vlan)
            
            # Start a new VLAN entry
            vlan_id = int(match.group("vlan_id"))  # VLAN ID
            name = match.group("name")             # VLAN Name
            status = match.group("status")         # Status
            ports = match.group("ports").strip()   # Ports (strip any leading/trailing whitespace)
            
            current_vlan = [vlan_id, name, status, ports]
        else:
            # If the line doesn't match a VLAN entry, it's a continuation of ports for the current VLAN
            if current_vlan and line.strip():
                current_vlan[3] += ' ' + line.strip()
    
    # Add the last VLAN entry to the list
    if current_vlan:
        vlans.append(current_vlan)
    
    return vlans


# data6 = """
# 1    default    active    Gi3/0, Gi3/1, Gi3/2, Gi3/3
# 10    Sales    active    Gi1/1, Gi1/2, Gi1/3, Gi2/0
# 20    Production    active    Gi0/2, Gi0/3, Gi1/0
# 30    HR    active    Gi2/1, Gi2/2
# 40    Wi-Fi    active    
# 1002 fddi-default    act/unsup    
# 1003 token-ring-default   act/unsup    
# 1004 fddinet-default   act/unsup    
# 1005 trnet-default    act/unsup    
# """

# vlan_info = parse_vlan_table(data6)
# for vlan in vlan_info:
#     print(vlan)
switches_facts()