import ansible_runner

def set_hostname(selected_host,new_hostname):
    runner = ansible_runner.run(
    private_data_dir="../ansible/",  # Current directory
    playbook="playbooks/site.yaml",
    inventory="hosts",  # Path to external inventory file
    limit=selected_host,  # Dynamically target the selected host
    extravars={  # Pass the selected role as a variable
            "selected_roles": 'hostname',  # Dynamically set the role
            "new_hostname": new_hostname
        }
    )


    return  runner.status
 
def set_banner(selected_host,new_banner):
    runner = ansible_runner.run(
    private_data_dir="../ansible/",  # Current directory
    playbook="playbooks/site.yaml",
    inventory="hosts",  # Path to external inventory file
    limit=selected_host,  # Dynamically target the selected host
    extravars={  # Pass the selected role as a variable
            "selected_roles": 'banner',  # Dynamically set the role
            "new_banner": new_banner
        }
    )

    return  runner.status
#interface number [0/1]  ipv4/mask
def set_interfaceconfigration(selected_host,interface_name,ip):
    runner = ansible_runner.run(
    private_data_dir="../ansible/",  # Current directory
    playbook="playbooks/site.yaml",
    inventory="hosts",  # Path to external inventory file
    limit=selected_host,  # Dynamically target the selected host
    extravars={  # Pass the selected role as a variable
            "selected_roles": 'ip_config',  # Dynamically set the role
            "interfaces": interface_name,
            "ipv4": ip
        }
    )

    return  runner.status

x = {
    'interfacenum' : '0/3',
    'ipv4' : "192.168.10.25/24" 
    }

# print(set_hostname('Router1','R1'))
# print(set_banner('Router1','fuck you'))
# print(set_interfaceconfigration('Router_01',"x","192.168.1.100"))
