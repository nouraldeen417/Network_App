
// const switchesApiUrl = 'http://127.0.0.1:8000/playground/api/switches/';
const switchesApiUrl = 'http://192.168.1.100/playground/api/switches/';
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
        console.log(tableBody);
        tableBody.innerHTML = ''; 

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
            }
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

document.addEventListener('DOMContentLoaded', () => {
    fetchSwitches();  // Initial data load
    setInterval(fetchSwitches, 600000);  // Refresh every 600,000 milliseconds (10 minutes)
});
