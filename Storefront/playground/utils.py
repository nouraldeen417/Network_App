# utils.py
import sys
import random
# Add the path to the 'python' folder to the system path
sys.path.append("..")
# Now import 'some_file' from the 'python' directory
from python import hello,router,configration,switch
class AutomationMethods:
    @staticmethod
    
    def Ping():
        status=hello.Ping() #status has three lists host-ip list[], status list[] ,task name list[]
        print(status)
        return  status

    def Router_list():
        Fact_data=router.Routers_facts() #Fact_data has three lists host-ip list[], status list[] ,task name list[]        
        print(Fact_data)
        return  Fact_data
    
    def Set_Hostname(selected_host,hostname):
        status = configration.set_hostname(selected_host,hostname) #"ok"
        print (status)
        return status
    
    def Set_Banner(selected_host,banner):
        status = configration.set_banner(selected_host,banner) #"ok"
        return status
    
    def set_interfaceconfigration(selected_host,interface_name,ipv4):
        print("sucess")
        print(selected_host)
        print(interface_name)
        print(ipv4)
        status = configration.set_interfaceconfigration(selected_host,interface_name,ipv4) #"ok"
        print(status)
        return status
    
    def Switch_list():
        Fact_data=switch.switches_facts() #Fact_data has three lists host-ip list[], status list[] ,task name list[]
        print(Fact_data)
        return Fact_data
    def Firewall_list():
        Fact_data=AutomationMethodsData.Firewalls_facts() #Fact_data has three lists host-ip list[], status list[] ,task name list[]
        print(Fact_data)
        return Fact_data














#MY Data I used to Test 
class AutomationMethodsData:
    @staticmethod
    def Ping():
        # Here you can add your processing logic
        devices = []
        
        # First device
        d1 = Device(host="device1", task="task1", status="Running")
        devices.append(d1)
        
        # Second device
        d2 = Device(host="device2", task="task2", status="Stopped")
        devices.append(d2)
        return devices
    
    def Routers_facts():
        dummy_interfaces = [
        ("GigabitEthernet0/0", "192.168.1.1/24", "up"),
        ("GigabitEthernet0/1", "192.168.2.1/24", "down"),
        ("GigabitEthernet0/2", "10.0.0.1/24", "up"),
        ]

        dummy_neighbors = [
        ("RouterA", "192.168.1.2/24", "GigabitEthernet0/0"),
        ("Switch1", "192.168.2.2/24", "GigabitEthernet0/1"),
        ("Firewall1", "10.0.0.2/24", "GigabitEthernet0/2"),
        ]

        dummy_routing_table = [
        ("OSPF", "192.168.3.0/24", "GigabitEthernet0/0"),
        ("Static", "172.16.0.0/16", "GigabitEthernet0/1"),
        ("BGP", "10.10.10.0/24", "GigabitEthernet0/2"),
        ]

        device_name = f"Device-{random.randint(100, 999)}"
        device_id = device_name
        facts=[]
        facts.append(Facts(device_id, device_name, dummy_interfaces, dummy_neighbors, dummy_routing_table));
        device_name = f"Device-{random.randint(100, 999)}"
        device_id = device_name
        dummy_routing_table = [
        ("VLAN", "192.168.3.0/24", "GigabitEthernet0/0"),
        ("Static", "172.16.0.0/16", "GigabitEthernet0/1"),
        ]
        facts.append(Facts(device_id, device_name, dummy_interfaces, dummy_neighbors, dummy_routing_table));
        return facts

    def Switches_facts():
        # Here you can add your processing logic
        Switches = []
        
        # First device
        d1 = Switch(name="Swithc1" , ip="192.167.0.1",loc="home",stat="Stopped")
        Switches.append(d1)
        
        # Second device
        d2 = Switch(name="Switch2" , ip="192.167.0.1",loc="home",stat="Running")
        Switches.append(d2)
        return Switches
    
    def Firewalls_facts():
        # Here you can add your processing logic
        firewalls = []
        
        # First device
        d1 = Firewall(name="Firewall1" , ip="192.167.0.1",loc="home",stat="Stopped")
        firewalls.append(d1)
        
        # Second device
        d2 = Firewall(name="Firewall2" , ip="192.167.0.1",loc="home",stat="Running")
        firewalls.append(d2)
        return firewalls
    
class Device:
    def __init__(self, host, task, status):
        self.host = host
        self.task = task
        self.status = status
        
class Switch:
    def __init__(self, name, ip, loc,stat):
        self.name = name
        self.ip_address=ip
        self.location=loc,
        self.status=stat

class Firewall:
    def __init__(self, name, ip, loc,stat):
        self.name = name
        self.ip_address=ip
        self.location=loc,
        self.status=stat
        
class Facts:
    class Interface:
        def __init__(self, name, address_subnet, status,description):
            self.name = name
            self.address_subnet = address_subnet
            self.status = status
            self.description=description #new data


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
            self.next_hop=next_hop #new data
            self.admin_distance=admin_distance #new data
    def __init__(self, id, device, interfaces, neighbors,routing_tables):
        self.id = id
        self.device = device
        self.interfaces = [self.Interface(*interface) for interface in interfaces]  # List of Interface objects
        self.neighbors = [self.Neighbor(*neighbor) for neighbor in neighbors]  # List of Neighbor objects
        self.routing = [self.Routing(*routing_table) for routing_table in routing_tables]  # List of Neighbor objects

#switch_fact
class Facts:
    class Interface:
        def __init__(self, name, address_subnet, status,description):
            self.name = name
            self.address_subnet = address_subnet
            self.status = status
            self.description=description #new data


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
