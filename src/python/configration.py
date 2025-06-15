import ansible_runner
import re
import ipaddress
import os
# from ..python import show

NO_CHNAGE_MSG="Configuration already exists. No changes were made."
OK_MSG="ok"
VALID_IP_PATTERN = r"^((25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])/(1[0-9]|2[0-9]|3[0-2])$"

def _generate_masks(cidr):
    """
    Generate wildcard mask and subnet mask from CIDR notation.
    
    Args:
        cidr (str): Network address in CIDR notation (e.g., "192.168.1.0/24").
    
    Returns:
        dict: A dictionary containing the network, wildcard mask, and subnet mask.
    """
    # Parse the CIDR notation
    network = ipaddress.ip_network(cidr, strict=False)
    
    # Calculate the subnet mask
    subnet_mask = str(network.netmask)
    
    # Calculate the wildcard mask
    wildcard_mask = str(network.hostmask)
    
    return {
        "network": str(network.network_address),
        "wildcard_mask": wildcard_mask,
        "subnet_mask": subnet_mask
    }

def _get_ansibleresult(runner):
    # Convert stderr to a string if it exists, else set it to an empty string
    error_msg = runner.stdout.read().lower()
    for event in runner.events:
        if event.get('event') == 'runner_on_failed':
            error_msg = event['event_data'].get('res', {}).get('module_stderr', '') +  event['event_data'].get('res', {}).get('msg', '')

    
      
    if runner.rc != 0:
        if "could not match supplied host" in error_msg:
            return "Host not found in inventory."
        elif "ssh connection failed" in error_msg and "Timeout" in error_msg or "No route to host" in error_msg:
            return "Host is unreachable (network/firewall issue)."
        elif "ssh connection failed" in error_msg or "Failed to authenticate" in error_msg:
            return "Authentication failure (SSH key or password issue)."
        elif "overlaps" in error_msg and "ip address" in error_msg:
            return "IP Address used by another interface."
        else:
            return f"Unknown error: {error_msg}"
    
    changed = runner.stats.get('changed', {})
    print (changed)
    if not bool(changed):
        return "Configuration already exists. No changes were made." 

    return "ok"

def _validate_and_convert_to_list(input_data):
    """
    Validates input and converts to list if needed.
    
    Args:
        input_data: Input to be validated (can be list, string, or other type)
        
    Returns:
        list: The converted list or original list if input was already a list
    """
    if isinstance(input_data, list):
        return input_data
    elif isinstance(input_data, str):
        # Split by comma and strip whitespace from each element
        return [item.strip() for item in input_data.split(',')]
    else:
        # For other types, wrap in a list
        return [input_data]
def set_hostname(selected_host,new_hostname):
    error_msg = "Empty input"
    runner = 0
    if (new_hostname == "" ):
       return error_msg 
    else:        
        runner = ansible_runner.run(
        private_data_dir="../ansible/",  # Current directory
        playbook="playbooks/site.yaml",
        inventory="hosts",  # Path to external inventory file
        limit=selected_host,  # Dynamically target the selected host
        rotate_artifacts=10,
        extravars={  # Pass the selected role as a variable
                "selected_roles": 'hostname',  # Dynamically set the role
                "new_hostname": new_hostname
            }
        )
        error_msg = _get_ansibleresult(runner)

    return error_msg

def set_banner(selected_hosts,new_banner):
    error_msg = "Empty input"    
    if (new_banner == "" ):
        return error_msg 
    else:
        runner = ansible_runner.run(
        private_data_dir="../ansible/",      # Current directory
        playbook="playbooks/site.yaml",
        inventory="hosts",                   # Path to external inventory file
        limit=selected_hosts ,     # Limit to selected routers
        extravars={                          # Pass the selected role as a variable
                "selected_roles": 'banner',  # Dynamically set the role
                "new_banner": new_banner
            }
        )
    error_msg = _get_ansibleresult(runner)
    return error_msg

def set_interfaceconfigration(selected_hosts,interface_name,ip_subnet,tag="add_configration"):
    error_msg = "Please select any Interface to configure! "    
    runner = 0
    if (interface_name == None ):
      return error_msg  
    if re.fullmatch(VALID_IP_PATTERN, ip_subnet):
        runner = ansible_runner.run(
        private_data_dir="../ansible/",          # Current directory
        playbook="playbooks/site.yaml",
        inventory="hosts",                       # Path to external inventory file
        limit=selected_hosts,          # Limit to selected routers
        rotate_artifacts=10, 
        tags=tag,               
        extravars={                              # Pass the selected role as a variable
                "selected_roles": 'ip_config',   # Dynamically set the role
                "interfaces": interface_name,
                "ipv4": ip_subnet
            }
        )

    else :   
       error_msg = "Invalid IP/Subnet format."    
       return error_msg
    error_msg = _get_ansibleresult(runner)
    return error_msg
def set_interfaceon(selected_hosts,interface_name):
    error_msg = "Please select any Interface to configure! "    
    runner = 0
    if (interface_name == None ):
      return error_msg  
    else:
        runner = ansible_runner.run(
        private_data_dir="../ansible/",          # Current directory
        playbook="playbooks/site.yaml",
        inventory="hosts",                       # Path to external inventory file
        limit=selected_hosts,          # Limit to selected routers
        rotate_artifacts=10,                
        extravars={                              # Pass the selected role as a variable
                "selected_roles": 'interface-state',   # Dynamically set the role
                "interfaces": interface_name,
                "enable_state" : 'true' 
            }
        )

    error_msg = _get_ansibleresult(runner)
    return error_msg
def set_interfaceoff(selected_hosts,interface_name):
    error_msg = "Please select any Interface to configure! "    
    runner = 0
    if (interface_name == None ):
      return error_msg  
    else:
        runner = ansible_runner.run(
        private_data_dir="../ansible/",          # Current directory
        playbook="playbooks/site.yaml",
        inventory="hosts",                       # Path to external inventory file
        limit=selected_hosts,          # Limit to selected routers
        rotate_artifacts=10,                
        extravars={                              # Pass the selected role as a variable
                "selected_roles": 'interface-state',   # Dynamically set the role
                "interfaces": interface_name,
                "enable_state" : 'false' 
            }
        )

    error_msg = _get_ansibleresult(runner)
    return error_msg
def Switch_gateway(selected_hosts , gateway):
    command = f"lines='ip default-gateway {gateway}'"
        # module_args='{"commands": ["ip default-gateway {{ gateway }}"]}',
    result = ansible_runner.run(
        private_data_dir="../ansible/",          # Current directory
        inventory="hosts",  
        limit=selected_hosts,                     # Path to external inventory file
        module="ios_config",
        module_args=command,
        host_pattern="switches"  # Update with the correct host group from your inventory
    )
    return _get_ansibleresult(result)

def set_ospfconfigration(selected_hosts,interface_name,cidr_list, 
                         ospf_process_id, router_id, area_id,
                         hello_timer, dead_timer,tag="add_configration"):
    error_msg = "Please select any Interface to configure! "    
    runner = 0
    network_address=[]
    wildcard_mask=[]
    subnet_mask=[]
    cidr_list= _validate_and_convert_to_list(cidr_list)
    if (interface_name == None ):
      return error_msg  
    else:
        for cidr in cidr_list:
            masks = _generate_masks(cidr)
            network_address.append(masks["network"])  
            wildcard_mask.append(masks["wildcard_mask"])
            subnet_mask.append(masks["subnet_mask"])
        runner = ansible_runner.run(
        private_data_dir="../ansible/",          # Current directory
        playbook="playbooks/site.yaml",
        inventory="hosts",                       # Path to external inventory file
        limit=','.join(selected_hosts),                     # Path to external inventory file
        rotate_artifacts=10,
        tags=tag,                
        extravars={                              # Pass the selected role as a variable
                "selected_roles": 'ospf',   # Dynamically set the role
                "ospf_process_id": ospf_process_id,
                "router_id": router_id,
                "network_data": [{"network": net, "wildcard": wc} for net, wc in zip(network_address, wildcard_mask)],
                "area_id": area_id,
                "interface_name": interface_name,
                "subnet_mask": subnet_mask,
                "hello_timer": hello_timer,
                "dead_timer": dead_timer 
            }
        )

    error_msg = _get_ansibleresult(runner)
    return error_msg
def set_static_routing(selected_hosts,cidrs,next_hop,admin_distance,tag="add_configration"):
    error_msg = "Please select any Interface to configure! "    
    runner = 0

    if (next_hop == None and admin_distance == None):
      return error_msg  
    else:
        runner = ansible_runner.run(
        private_data_dir="../ansible/",          # Current directory
        playbook="playbooks/site.yaml",
        inventory="hosts",                       # Path to external inventory file
        limit=selected_hosts,          # Limit to selected routers
        rotate_artifacts=10,
        tags=tag,           
        extravars={                              # Pass the selected role as a variable
                "selected_roles": 'static_routing',   # Dynamically set the role
                "cidr_list":   cidrs ,
                "next_hop":next_hop,
                "admin_distance":admin_distance
            }
        )

    error_msg = _get_ansibleresult(runner)
    return error_msg

def set_valnconfigration(selected_hosts,interfaces_list,vlan_cidr, 
                         vlan_id, vlan_name,tag="add_configration"):
    error_msg = "Please select any Interface to configure! "    
    runner = 0
    if (interfaces_list == None ):
      return error_msg  
    if re.fullmatch(VALID_IP_PATTERN, vlan_cidr):
        runner = ansible_runner.run(
        private_data_dir="../ansible/",          # Current directory
        playbook="playbooks/site.yaml",
        inventory="hosts",                       # Path to external inventory file
        limit=','.join(selected_hosts),          # Limit to selected routers
        rotate_artifacts=10,
        tags=tag,                
        extravars={                              # Pass the selected role as a variable
                "selected_roles": 'vlan',   # Dynamically set the role
                "vlan_id": vlan_id,
                "vlan_name": vlan_name ,
                "vlan_interfaces": interfaces_list

            }
        )
    else :
        return "please add valid ip "
    error_msg = _get_ansibleresult(runner)
    print ("vlan"+str(vlan_id))
    if (error_msg == OK_MSG or error_msg == NO_CHNAGE_MSG ):
        error_msg=set_interfaceconfigration(selected_hosts[0],"vlan"+str(vlan_id),vlan_cidr,tag)    
        return error_msg
    return error_msg

def do_configration(selected_hosts , conf_str):
    error_msg = "Please select any Interface to configure! "    
    runner = 0
    if (conf_str == None ):
      return error_msg  
    else:
        runner = ansible_runner.run(
        private_data_dir="../ansible/",          # Current directory
        playbook="playbooks/site.yaml",
        inventory="hosts",                       # Path to external inventory file
        limit=','.join(selected_hosts),          # Limit to selected routers
        tags="line_config",
        rotate_artifacts=10,                
        extravars={                              # Pass the selected role as a variable
                "selected_roles": 'config',   # Dynamically set the role
                "config_commands": conf_str
            }
        )

    error_msg = _get_ansibleresult(runner)
    return error_msg

def apply_configrationfile(selected_hosts,config_file):    
    error_msg = "Please select any Interface to configure! "    
    runner = 0
    
    if (config_file == None ):
      return error_msg  
    else:
        Base_dir = "ansible_uploads"
        temp_dir = "../ansible/ansible_uploads"
        os.makedirs(temp_dir, exist_ok=True, mode=0o700)
        temp_path = os.path.join(temp_dir, config_file.name)  
        file_path = os.path.join(Base_dir, config_file.name)        
        # Save file
        with open(temp_path, 'wb+') as destination:
            for chunk in config_file.chunks():
                destination.write(chunk)
        print(f"File saved to {file_path}")
        runner = ansible_runner.run(
            private_data_dir="../ansible/",          # Current directory
            playbook="playbooks/site.yaml",
            inventory="hosts",                       # Path to external inventory file
            limit=','.join(selected_hosts),
            tags="file_config",                     # Limit to selected routers
            rotate_artifacts=10,                
            extravars={                              # Pass the selected role as a variable
                    "selected_roles": 'config',   # Dynamically set the role
                    "configuration_file_path": config_file.name
                }
        )

    error_msg = _get_ansibleresult(runner)
    return error_msg


def backup_cisco_devices(selected_hosts, backup_dir='backups'):
    """
    Backup Cisco IOS devices using Ansible
    
    Args:
        devices: List of devices [{'name': str, 'ip': str, 'username': str, 'password': str}]
        backup_dir: Local directory to store backups
    
    Returns:
        dict: {'success': bool, 'backup_files': list, 'errors': list}
    """
    error_msg = "Please select any Interface to configure! "    
    runner = 0
    if (backup_dir == None ):
      return error_msg  
    else:
        runner = ansible_runner.run(
            private_data_dir="../ansible/",          # Current directory
            playbook="playbooks/site.yaml",
            inventory="hosts",                       # Path to external inventory file
            limit=','.join(selected_hosts),          # Limit to selected routers
            rotate_artifacts=10,                
            extravars={                              # Pass the selected role as a variable
                    "selected_roles": 'backup',   # Dynamically set the role
                }
        )

    error_msg = _get_ansibleresult(runner)
    return error_msg

# print(backup_cisco_devices(["Router_01","Router_02","Router_03"], backup_dir='backups'))
# print(apply_configrationfile(["Router_03"],"/root/Network_App/ansible/templates/backup_Router_03_2025-03-31_05-21-05.cfg"))
# config_commands="""
# hostname R1
# """
# # print (type(config_commands))    

# print(do_configration( ["Router_01"] , config_commands)
# )


# set_static_routing('Router_01','remove_configration',["0.0.0.0/0","192.168.10.0/24"],"192.168.3.2",10)

# set_valnconfigration('Switch_01','remove_configration',["GigabitEthernet1/0","GigabitEthernet1/1"],"192.168.10.10/24", 
#                          50, "work")
# Run the function
# if status == 0:
#     print("OSPF neighbors retrieved successfully!")
# else:
#     print("Failed to retrieve OSPF neighbors.")

# print(set_hostname('Router_01','R1'))
# print(set_banner(x,'fuck you'))
# print(set_interfaceon(x,"GigabitEthernet0/1"))
# print(set_interfaceoff(x,"GigabitEthernet0/1"))
# print(set_interfaceconfigration('Router_01',"GigabitEthernet0/1","192.168.5.10/24"))
# set_ospfconfigration(
#     selected_hosts='Router_01',
#     cidr_list=["192.168.2.0/24"],
#     tag='add_configration',
#     ospf_process_id=1,
#     router_id="1.1.1.1",
#     area_id=0,
#     interface_name="GigabitEthernet0/3",
#     interface_ip="192.168.3.1",
#     hello_timer=10,
#     dead_timer=40
# )
# set_ospfconfigration(
#     selected_hosts='Router_02',
#     tag='add_configration',
#     cidr_list=["192.168.4.0/24"],
#     ospf_process_id=1,
#     router_id="2.2.2.2",
#     area_id=0,
#     interface_name="GigabitEthernet0/0",
#     interface_ip="192.168.3.2",
#     hello_timer=10,
#     dead_timer=40
# ) 

# show.ospf_neighbors()
# show.ospf_database()
# show.routing_table()


# print(status)

# set_static_routing('Router_01','remove_configration',"0.0.0.0/0","192.168.3.2",150)

# Switch_gateway('Switch_01', "192.168.2.1")
