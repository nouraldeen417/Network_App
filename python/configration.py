import ansible_runner
import re

VALID_IP_PATTERN = r"^((25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])/(1[0-9]|2[0-9]|3[0-2])$"

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
        rotate_artifacts=1,
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
        private_data_dir="../ansible/",  # Current directory
        playbook="playbooks/site.yaml",
        inventory="hosts",  # Path to external inventory file
        limit=selected_hosts ,         # Limit to selected routers
        extravars={                          # Pass the selected role as a variable
                "selected_roles": 'banner',  # Dynamically set the role
                "new_banner": new_banner
            }
        )
    error_msg = _get_ansibleresult(runner)
    return error_msg



def set_interfaceconfigration(selected_hosts,interface_name,ip_subnet):
    error_msg = "Please select any Interface to configure! "    
    runner = 0
    if (interface_name == None ):
      return error_msg  
    if re.fullmatch(VALID_IP_PATTERN, ip_subnet):
        runner = ansible_runner.run(
        private_data_dir="../ansible/",         # Current directory
        playbook="playbooks/site.yaml",
        inventory="hosts",                      # Path to external inventory file
        limit=selected_hosts,          # Limit to selected routers
        rotate_artifacts=1,                
        extravars={                             # Pass the selected role as a variable
                "selected_roles": 'ip_config',  # Dynamically set the role
                "interfaces": interface_name,
                "ipv4": ip_subnet
            }
        )

    else :   
       error_msg = "Invalid IP/Subnet format."    
       return error_msg
    error_msg = _get_ansibleresult(runner)
    return error_msg

# x=['Router_01','Router_02']
# # print(set_hostname('Router_01','R1'))
# print(set_banner(x,'fuck you'))
# # print(set_interfaceconfigration('Router_01',"GigabitEthernet0/1","192.168.5.10/24"))
