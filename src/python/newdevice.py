import ansible_runner
import configparser
from io import StringIO

def add_device_to_inventory(device_name, device_ip, device_type):
    """
    Safely adds a new device to inventory while preserving all existing formatting
    
    Args:
        device_name: The device name (e.g., "Router_03")
        device_ip: The device IP (e.g., "192.168.4.2")
        device_type: One of "router", "switch", or "l3sw"
    """
    # Map device types to inventory groups
    group_mapping = {
        "router": "routers",
        "switch": "switches",
        "l3switch": "L3_switches"
    }

    target_group = group_mapping.get(device_type.lower())
    if not target_group:
        raise ValueError(f"Invalid device type: {device_type}")
        

    new_entry = f"{device_name} ansible_host={device_ip}"
    added = False
    output_lines = []
    in_target_group = False
    with open('../ansible/inventory/hosts', 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            
            # Check if we're entering our target group
            if line.strip() == f"[{target_group}]":
                in_target_group = True
                output_lines.append(line)
                continue
                
            # Check if we're leaving any group
            if line.startswith('[') and line.endswith(']'):
                if in_target_group and not added:
                    # Add our new entry before leaving group
                    output_lines.append(new_entry)
                    added = True
                in_target_group = False
                
            # Preserve existing lines
            output_lines.append(line)
            
            # Add our new entry at end of target group
            if in_target_group and not added:
                next_line = f.peek() if hasattr(f, 'peek') else ''
                if not next_line or next_line.startswith('['):
                    output_lines.append(new_entry)
                    added = True
    
    # If group didn't exist, add it with our new entry
    if not added:
        output_lines.append(f"[{target_group}]")
        output_lines.append(new_entry)
    
    # Write back to file
    with open('../ansible/inventory/hosts', 'w') as f:
        f.write('\n'.join(output_lines))
        if not output_lines[-1].endswith('\n'):
            f.write('\n')  # Ensure ending newline


#ping all hosts in tobology
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

    return "ok"

def add_newdevice(cidr,devicename,type,username,password):
    # Create minimal in-memory inventory
    inventory = {
        "all": {
            "hosts": {
                cidr: {}  # Just the single IP we want to target
            },
            "vars": {
                "ansible_connection": "ssh",
                "ansible_user": username,  # Default user
                "ansible_password":password,
                "ansible_connection":"ansible.netcommon.network_cli",
                "ansible_network_os":"cisco.ios.ios"
            }
        }
    }
    r = ansible_runner.run(
    private_data_dir="../ansible/",  # Current directory
    playbook="playbooks/ping.yaml",
    inventory=inventory,
    rotate_artifacts=10
    )
    result = _get_ansibleresult(r)
    if result == "ok":
        result = add_ansibleuser(cidr,username,password) # helping function
        if result == "ok" :
            print(result)
            add_device_to_inventory(devicename,cidr,type) # helping function
    return result
def add_ansibleuser(cidr,username,password):
    # Create minimal in-memory inventory
    inventory = {
        "all": {
            "hosts": {
                cidr: {}  # Just the single IP we want to target
            },
            "vars": {
                "ansible_connection": "ssh",
                "ansible_user": username,  # Default user
                "ansible_password":password,
                "ansible_connection":"ansible.netcommon.network_cli",
                "ansible_network_os":"cisco.ios.ios"
            }
        }
    }
    r = ansible_runner.run(
    private_data_dir="../ansible/",  # Current directory
    playbook="playbooks/user.yaml",
    inventory=inventory,
    rotate_artifacts=10
    )
    result = _get_ansibleresult(r)
    return result

