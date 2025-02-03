# utils.py
import sys
# Add the path to the 'python' folder to the system path
sys.path.append("..")
# Now import 'some_file' from the 'python' directory
from python import hello,router,configration
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
    
    def Set_Hostname(router,hostname):
        status=configration.set_hostname(router,hostname)
        return status
    
    def Switch_list():
        Fact_data=AutomationMethodsData.Switches_facts() #Fact_data has three lists host-ip list[], status list[] ,task name list[]
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
        # Here you can add your processing logic
        routers_facts = []

        # First router facts
        interfaces1 = [
            ("Gig0/0", "192.167.0.1/24", "running"),
            ("Gig0/1", "192.167.1.1/24", "stop")
        ]
        neighbors1 = [
            ("Router2", "192.167.0.2/24", "Gig0/0")
        ]
        facts1 = Facts("Router1", interfaces1, neighbors1)
        routers_facts.append(facts1)

        # Second router facts
        interfaces2 = [
            ("Gig0/0", "192.167.0.2/24", "running"),
            ("Gig0/1", "192.167.2.1/24", "stop")
        ]
        neighbors2 = [
            ("Router1", "192.167.0.1/24", "Gig0/0")
        ]
        facts2 = Facts("Router2", interfaces2, neighbors2)
        routers_facts.append(facts2)

        return routers_facts

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
