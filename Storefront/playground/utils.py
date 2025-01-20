# utils.py
import sys
# Add the path to the 'python' folder to the system path
sys.path.append("..")
# Now import 'some_file' from the 'python' directory
from python import hello,router
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
# MY Data I used to Test 
# class AutomationMethods:
#     @staticmethod
#     def Ping():
#         # Here you can add your processing logic
#         devices = []
        
#         # First device
#         d1 = Device(host="device1", task="task1", status="Running")
#         devices.append(d1)
        
#         # Second device
#         d2 = Device(host="device2", task="task2", status="Stopped")
#         devices.append(d2)
#         return devices
    
