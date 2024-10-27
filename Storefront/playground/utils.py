# utils.py
class AutomationMethods:
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
    
class Device:
    def __init__(self, host, task, status):
        self.host = host
        self.task = task
        self.status = status