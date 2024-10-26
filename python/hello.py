import ansible_runner
#ping all hosts in tobology
def Ping():
    r = ansible_runner.run(
    private_data_dir="../ansible/",  # Current directory
    playbook="playbooks/ping.yaml",
    inventory="hosts",  # Path to external inventory file
    )
    host=[]
    task=[]
    status=[]

    for event in r.events: 
        event_data = event.get('event_data', {})
        cur_stat= event.get('event')
        #Check for task completion statuses
        if cur_stat in ('runner_on_ok', 'runner_on_skipped', 'runner_on_failed', 'runner_on_unreachable'):
            host.append(event_data.get('host', event_data.get('remote_addr')))  
            task.append(event_data.get('task', event_data.get('name', event_data.get('play'))))
            status.append(event.get('event'))

    # print(host + status + task)
    return  host,status,task 

