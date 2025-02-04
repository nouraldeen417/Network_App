// Path: your-javascript-file.js

// API endpoint URL
const routersApiUrl = 'http://127.0.0.1:8000/playground/api/routers/';
const switchesApiUrl = 'http://127.0.0.1:8000/playground/api/switches/';
const firewallsApiUrl = 'http://127.0.0.1:8000/playground/api/firewalls/';



// Function to fetch data and populate the table
async function fetchRouters() {
    try {
        const response = await fetch(routersApiUrl); // Call the API
        console.log(response);
        if (!response.ok) {
            throw new Error(`An error occurred: ${response.statusText}`);
        }
        const data = await response.json(); // Parse JSON response

        localStorage.setItem('routerData', JSON.stringify(data));
        console.log('Data stored in localStorage:', data);

        // Populate table with data
        const tableBody = document.getElementById('router-table').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ''; // Clear existing rows

        data.forEach(fact => {
            // Determine the max row count (interfaces vs neighbors)
            const maxRows = Math.max(fact.interfaces.length, fact.neighbors.length);

            for (let i = 0; i < maxRows; i++) {
                const row = document.createElement('tr');

                // Router Selection (Radio Button) - Only on the first row
                if (i === 0) {
                    const selectCell = document.createElement('td');
                    const radioButton = document.createElement('input');
                    radioButton.type = 'radio';
                    radioButton.name = 'router';
                    radioButton.value = fact.id;
                    selectCell.rowSpan = maxRows; // Span across all rows for this device
                    selectCell.appendChild(radioButton);
                    row.appendChild(selectCell);

                    // Device Cell - Only on the first row
                    const deviceCell = document.createElement('td');
                    deviceCell.textContent = fact.device;
                    deviceCell.rowSpan = maxRows; // Span across all rows for this device
                    row.appendChild(deviceCell);
                }

                // Interface Name, Subnet, and Status
                const interfaceCellName = document.createElement('td');
                const interfaceCellSubnet = document.createElement('td');
                const interfaceCellStatus = document.createElement('td');

                if (i < fact.interfaces.length) {
                    interfaceCellName.textContent = fact.interfaces[i].name;
                    if (fact.interfaces[i].address_subnet.length > 0  ){
                        interfaceCellSubnet.textContent = fact.interfaces[i].address_subnet[0].address + "/" + fact.interfaces[i].address_subnet[0].subnet;
                        console.log(fact.interfaces[i].address_subnet[0].address);
                    }
                    //interfaceCellSubnet.textContent = fact.interfaces[i].address_subnet;
                    interfaceCellStatus.textContent = fact.interfaces[i].status;
                } else {
                    interfaceCellName.textContent = '';
                    interfaceCellSubnet.textContent = '';
                    interfaceCellStatus.textContent = '';
                }

                row.appendChild(interfaceCellName);
                row.appendChild(interfaceCellSubnet);
                row.appendChild(interfaceCellStatus);

                // Neighbor Name, Subnet, and Port
                const neighborCellName = document.createElement('td');
                const neighborCellSubnet = document.createElement('td');
                const neighborCellPort = document.createElement('td');

                if (i < fact.neighbors.length) {
                    neighborCellName.textContent = fact.neighbors[i].name;
                    neighborCellSubnet.textContent = fact.neighbors[i].address_subnet;
                    neighborCellPort.textContent = fact.neighbors[i].port;
                } else {
                    neighborCellName.textContent = '';
                    neighborCellSubnet.textContent = '';
                    neighborCellPort.textContent = '';
                }

                row.appendChild(neighborCellName);
                row.appendChild(neighborCellSubnet);
                row.appendChild(neighborCellPort);

                // Append row to the table
                tableBody.appendChild(row);

                // Add click event listener to the row
                row.addEventListener('click', () => {
                    const radioButton = row.querySelector('input[type="radio"]');
                    if (radioButton) {
                        radioButton.checked = true;

                        // Enable the Configure button
                        const configureButton = document.getElementById('configure-btn');
                        configureButton.disabled = false;
                    }
                });
            }
        });

        // Add event listeners to radio buttons
        const radioButtons = document.querySelectorAll('input[name="router"]');
        const configureButton = document.getElementById('configure-btn');

        radioButtons.forEach(radio => {
            radio.addEventListener('change', () => {
                // Enable the Configure button when a router is selected
                configureButton.disabled = false;
            });
        });

        // Add event listener to the Configure button
        configureButton.addEventListener('click', () => {
            const selectedRouter = document.querySelector('input[name="router"]:checked');
            if (selectedRouter) {
                // Redirect to routerconfiguration.html with the selected router's name
                window.location.href = `/playground/routerconfiguration?router=${encodeURIComponent(selectedRouter.value)}`;
            } else {
                alert('Please select a router to configure.');
            }
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to fetch data and populate the form
async function fetchAndPopulateInterfaces() {
    try {
        // Fetch the data from the API
        const storedData = localStorage.getItem('routerData');

        if (!storedData) {
            console.error('No data found in localStorage.');
            storedData = await fetch(routersApiUrl);
        //return;
        }

        const data = JSON.parse(storedData);

        // Get the router ID from the hidden input
        const routerId = document.querySelector('input[name="router"]').value;

        // Find the router with the matching ID
        const selectedRouter = data.find(router => router.id === routerId);

        if (!selectedRouter) {
            console.error('Router not found.');
            return;
        }

        // Get the container for the radio buttons
        const radioContainer = document.getElementById('interface-radio-container');

        // Clear any existing content
        radioContainer.innerHTML = '';

        // Loop through the interfaces and create radio buttons
        selectedRouter.interfaces.forEach(interface => {
            // Create a radio button for the interface
            const radioButton = document.createElement('input');
            radioButton.type = 'radio';
            radioButton.name = 'interface';
            radioButton.value = interface.name; // Use interface name as the value
            radioButton.id = `interface-${interface.name}`;

            // Create a label for the radio button
            const label = document.createElement('label');
            label.htmlFor = `interface-${interface.name}`;
            label.textContent = `${interface.name} (${interface.address_subnet}) - ${interface.status}`;

            // Append the radio button and label to the container
            radioContainer.appendChild(radioButton);
            radioContainer.appendChild(label);
            radioContainer.appendChild(document.createElement('br')); // Add a line break
        });
    } catch (error) {
        console.error('Error fetching or populating data:', error);
    }
}



// Function to fetch data and populate the table
async function fetchSwitches() {
    try {
        const response = await fetch(switchesApiUrl); // Call the API
        console.log(response);
        if (!response.ok) {
            throw new Error(`An error occurred: ${response.statusText}`);
        }
        const data = await response.json(); // Parse JSON response

        // Populate table with data
        const tableBody = document.getElementById('switch-table').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ''; 
        
        const runningswitchesChecklist = document.getElementById('running-switches-checklist');
        runningswitchesChecklist.innerHTML = ''; 
        
        data.forEach(swtch => {
            const row = document.createElement('tr');

            // Create table cells for each router property
            const idCell = document.createElement('td');
            idCell.textContent = swtch.id;

            const nameCell = document.createElement('td');
            nameCell.textContent = swtch.name;

            const ipCell = document.createElement('td');
            ipCell.textContent = swtch.ip_address;

            const locationCell = document.createElement('td');
            locationCell.textContent = swtch.location;
            
            const statusCell = document.createElement('td');
            statusCell.textContent = swtch.status;
            
            // Append cells to the row
            row.appendChild(idCell);
            row.appendChild(nameCell);
            row.appendChild(ipCell);
            row.appendChild(locationCell);
            row.appendChild(statusCell);
            
            // Append row to the table body
            tableBody.appendChild(row);
            // Add stopped routers to the checklist
            if (swtch.status.toLowerCase() === 'running') {
                const listItem = document.createElement('li');

                // Create a checkbox for each stopped router
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.name = 'selectedSwitchIPs[]';
                checkbox.value = swtch.ip_address;

                const label = document.createElement('label');
                label.textContent = `${swtch.name} (ID: ${swtch.id}, IP: ${swtch.ip_address})`;
                label.htmlFor = `router-${swtch.id}`;

                listItem.appendChild(checkbox);
                listItem.appendChild(label);
                runningswitchesChecklist.appendChild(listItem);
            }
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to fetch data and populate the table
async function fetchFirewalls() {
    try {
        const response = await fetch(firewallsApiUrl); // Call the API
        console.log(response);
        if (!response.ok) {
            throw new Error(`An error occurred: ${response.statusText}`);
        }
        const data = await response.json(); // Parse JSON response

        // Populate table with data
        const tableBody = document.getElementById('firewall-table').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ''; 
        
        const runningfirewallsChecklist = document.getElementById('running-firewalls-checklist');
        runningfirewallsChecklist.innerHTML = ''; 
        
        data.forEach(firewall => {
            const row = document.createElement('tr');

            // Create table cells for each router property
            const idCell = document.createElement('td');
            idCell.textContent = firewall.id;

            const nameCell = document.createElement('td');
            nameCell.textContent = firewall.name;

            const ipCell = document.createElement('td');
            ipCell.textContent = firewall.ip_address;

            const locationCell = document.createElement('td');
            locationCell.textContent = firewall.location;
            
            const statusCell = document.createElement('td');
            statusCell.textContent = firewall.status;
            
            // Append cells to the row
            row.appendChild(idCell);
            row.appendChild(nameCell);
            row.appendChild(ipCell);
            row.appendChild(locationCell);
            row.appendChild(statusCell);
            
            // Append row to the table body
            tableBody.appendChild(row);
            // Add stopped routers to the checklist
            if (firewall.status.toLowerCase() === 'running') {
                const listItem = document.createElement('li');

                // Create a checkbox for each stopped router
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.name = 'selectedfirewallIPs[]';
                checkbox.value = firewall.ip_address;

                const label = document.createElement('label');
                label.textContent = `${firewall.name} (ID: ${firewall.id}, IP: ${firewall.ip_address})`;
                label.htmlFor = `firewall-${firewall.id}`;

                listItem.appendChild(checkbox);
                listItem.appendChild(label);
                runningfirewallsChecklist.appendChild(listItem);
            }
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
// Call the function when the page loads
//document.addEventListener('DOMContentLoaded', fetchRouters);
document.addEventListener('DOMContentLoaded', () => {
    fetchRouters();  // Initial data load
    fetchSwitches();  // Initial data load
    fetchFirewalls();
    fetchAndPopulateInterfaces();
    setInterval(fetchRouters, 600000);  // Refresh every 600,000 milliseconds (10 minutes)
});
