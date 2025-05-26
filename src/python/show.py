import ansible_runner
SEPRATION_STRING="\t\t\t \n"

def ospf_neighbors():
    result = ansible_runner.run(
        private_data_dir="../ansible/",          # Current directory
        inventory="hosts",                       # Path to external inventory file
        module="ios_command",
        module_args='{"commands": ["show ip ospf neighbor"]}',
        host_pattern="routers"  # Update with the correct host group from your inventory
    )

    output_string = ""  # Initialize an empty string to store the final output

    # Extract and display command output for each host
    for event in result.events:
        if "res" in event["event_data"]:  # Check if the result exists in the event data
            host = event["event_data"]["host"]  # Get the hostname
            response = event["event_data"]["res"]
            if isinstance(response, dict) and "stdout" in response:
                output_string += f"Host: {host}\n"  # Add hostname to the output string
                for output in response["stdout"]:
                    output_string += f"{output}\n"  # Add command output to the string
                output_string += "-" * 40 + "\n"  # Add a separator for readability

    return output_string  # Return the final string containing all host outputs
def routing_table():
    result = ansible_runner.run(
        private_data_dir="../ansible/",          # Current directory
        inventory="hosts",                       # Path to external inventory file
        module="ios_command",
        module_args='{"commands": ["show ip route"]}',
        host_pattern="routers"  # Update with the correct host group from your inventory
    )

    output_string = ""  # Initialize an empty string to store the final output

    # Extract and display command output for each host
    for event in result.events:
        if "res" in event["event_data"]:  # Check if the result exists in the event data
            host = event["event_data"]["host"]  # Get the hostname
            response = event["event_data"]["res"]
            if isinstance(response, dict) and "stdout" in response:
                output_string += f"Host: {host}\n"  # Add hostname to the output string
                for output in response["stdout"]:
                    output_string += f"{output}\n"  # Add command output to the string
                output_string += "-" * 40 + "\n"  # Add a separator for readability

    return output_string  # Return the final string containing all host outputs

def ospf_database():
    result = ansible_runner.run(
        private_data_dir="../ansible/",          # Current directory
        inventory="hosts",                       # Path to external inventory file
        module="ios_command",
        module_args='{"commands": ["show ip ospf database"]}',
        host_pattern="routers"  # Update with the correct host group from your inventory
    )

    output_string = ""  # Initialize an empty string to store the final output

    # Extract and display command output for each host
    for event in result.events:
        if "res" in event["event_data"]:  # Check if the result exists in the event data
            host = event["event_data"]["host"]  # Get the hostname
            response = event["event_data"]["res"]
            if isinstance(response, dict) and "stdout" in response:
                output_string += f"Host: {host}\n"  # Add hostname to the output string
                for output in response["stdout"]:
                    output_string += f"{output}\n"  # Add command output to the string
                output_string += "-" * 40 + "\n"  # Add a separator for readability

    return output_string  # Return the final string containing all host outputs

def vlan_information():
    result = ansible_runner.run(
        private_data_dir="../ansible/",          # Current directory
        inventory="hosts",                       # Path to external inventory file
        module="ios_command",
        module_args='{"commands": ["show vlan brief"]}',
        host_pattern="switches"  # Update with the correct host group from your inventory
    )

    output_string = ""  # Initialize an empty string to store the final output

    # Extract and display command output for each host
    for event in result.events:
        if "res" in event["event_data"]:  # Check if the result exists in the event data
            host = event["event_data"]["host"]  # Get the hostname
            response = event["event_data"]["res"]
            if isinstance(response, dict) and "stdout" in response:
                output_string += f"Host: {host}\n"  # Add hostname to the output string
                for output in response["stdout"]:
                    output_string += f"{output}\n"  # Add command output to the string
                output_string += "-" * 40 + "\n"  # Add a separator for readability

    return output_string  # Return the final string containing all host outputs

# print(ospf_neighbors())
# print(routing_table())
# print(ospf_database())
# print(vlan_information())
