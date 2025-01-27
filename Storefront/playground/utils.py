# utils.py
import sys
# Add the path to the 'python' folder to the system path
sys.path.append("..")
# Now import 'some_file' from the 'python' directory
#from python import hello,router
class AutomationMethods:
    @staticmethod
    
    def Ping():
        status=AutomationMethodsData.Ping() #status has three lists host-ip list[], status list[] ,task name list[]
        print(status)
        return  status

    def Router_list():
        Fact_data=AutomationMethodsData.Routers_facts() #Fact_data has three lists host-ip list[], status list[] ,task name list[]
        print(Fact_data)
        return  Fact_data
    
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
        routers = []
        
        # First device
        d1 = Router(name="Router1" , ip="192.167.0.1",loc="home",stat="Stopped")
        routers.append(d1)
        
        # Second device
        d2 = Router(name="Router2" , ip="192.167.0.1",loc="home",stat="Running")
        routers.append(d2)
        return routers
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

class Router:
    def __init__(self, name, ip, loc,stat):
        self.name = name
        self.ip_address=ip
        self.location=loc,
        self.status=stat

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
