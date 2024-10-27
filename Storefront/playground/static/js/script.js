// Path: your-javascript-file.js

// API endpoint URL
const apiUrl = 'http://127.0.0.1:8000/playground/api/routers/';

// Function to fetch data and populate the table
async function fetchRouters() {
    try {
        const response = await fetch(apiUrl); // Call the API
        console.log(response);
        if (!response.ok) {
            throw new Error(`An error occurred: ${response.statusText}`);
        }
        const data = await response.json(); // Parse JSON response

        // Populate table with data
        const tableBody = document.getElementById('router-table').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ''; 
        
        const stoppedRoutersChecklist = document.getElementById('stopped-routers-checklist');
        stoppedRoutersChecklist.innerHTML = ''; 
        
        data.forEach(router => {
            const row = document.createElement('tr');

            // Create table cells for each router property
            const idCell = document.createElement('td');
            idCell.textContent = router.id;

            const nameCell = document.createElement('td');
            nameCell.textContent = router.name;

            const ipCell = document.createElement('td');
            ipCell.textContent = router.ip_address;

            const locationCell = document.createElement('td');
            locationCell.textContent = router.location;
            
            const statusCell = document.createElement('td');
            statusCell.textContent = router.status;
            
            // Append cells to the row
            row.appendChild(idCell);
            row.appendChild(nameCell);
            row.appendChild(ipCell);
            row.appendChild(locationCell);
            row.appendChild(statusCell);
            
            // Append row to the table body
            tableBody.appendChild(row);
            // Add stopped routers to the checklist
            if (router.status.toLowerCase() === 'stopped') {
                const listItem = document.createElement('li');

                // Create a checkbox for each stopped router
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.name = 'selectedRouterIPs[]';
                checkbox.value = router.ip_address;

                const label = document.createElement('label');
                label.textContent = `${router.name} (ID: ${router.id}, IP: ${router.ip_address})`;
                label.htmlFor = `router-${router.id}`;

                listItem.appendChild(checkbox);
                listItem.appendChild(label);
                stoppedRoutersChecklist.appendChild(listItem);
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
    setInterval(fetchRouters, 600000);  // Refresh every 600,000 milliseconds (10 minutes)
});
