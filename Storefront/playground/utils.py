import sys
# Add the path to the 'python' folder to the system path
sys.path.append("..")
# Now import 'some_file' from the 'python' directory
from python import hello
class AutomationMethods:
    @staticmethod
    
    def Ping(hostname):
        status=hello.Ping() #status has three lists host-ip list[], status list[] ,task name list[]
        print(status)
        return  status

