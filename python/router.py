
import ansible_runner
import json


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

    def __init__(self, device, interfaces, neighbors):
        self.device = device
        self.interfaces = [self.Interface(*interface) for interface in interfaces]  # List of Interface objects
        self.neighbors = [self.Neighbor(*neighbor) for neighbor in neighbors]  # List of Neighbor objects
          
def Routers_facts():
    r = ansible_runner.run(
    private_data_dir="../ansible/",  # Current directory
    playbook="playbooks/routers.yaml",
    inventory="hosts",  # Path to external inventory file
    )
    # Get the list of hosts where tasks ran
    hosts_with_tasks = [host for host in  r.stats["ok"]]

    facts = []
    # Print the hosts where tasks were executed

    for host in hosts_with_tasks:
        facts_file = "/root/python/Network/ansible/temp/router_facts_" + host + ".json"

        with open(facts_file, "r") as f:
            router_facts = json.load(f)
        # print(router_interface_list(router_facts["net_interfaces"]))    
        facts.append(Facts(device=router_facts["net_hostname"], 
                           interfaces=router_interface_list(router_facts["net_interfaces"]),
                           neighbors=router_neighbor_list(router_facts["net_neighbors"])))
       
    return facts
    # print (facts[0].device , 
    #        facts[0].interfaces[0].name , 
    #        facts[0].interfaces[0].address_subnet ,
    #        facts[0].interfaces[0].status ,
    #        facts[0].neighbors[0].name,
    #        facts[0].neighbors[0].address_subnet,
    #        facts[0].neighbors[0].port)
    # print("\n")
    # print (facts[1].device , 
    #        facts[1].interfaces[1].name , 
    #        facts[1].interfaces[1].address_subnet ,
    #        facts[1].interfaces[1].status ,
    #        facts[1].neighbors[0].name,
    #        facts[1].neighbors[0].address_subnet,
    #        facts[1].neighbors[0].port)

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

Routers_facts()
