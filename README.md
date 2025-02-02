# Network Automation WebApp

## Overview
This project provides a **simple web application** for network engineers to **configure, manage, and monitor Cisco IOS devices** using **Ansible**. The web interface, built with Django, makes automation accessible and user-friendly.

### **Technologies Used:**
- **Ansible** – Automates network configurations.
- **Django Framework** – Provides a powerful and scalable web interface.
- **Python** – Core programming language.
- **HTML, CSS, JavaScript** – Frontend for a smooth user experience.

---
## **Why Ansible?**
Ansible simplifies **network automation** by eliminating manual configuration tasks. With its **agentless** approach, it connects via SSH, making it efficient and easy to scale.

---
## **Why Django?**
Django ensures **security, scalability, and rapid development** with built-in authentication, database management, and a structured framework, making it an excellent choice for web applications.

---
## **Setup Instructions**
### **Enable SSH Between Linux Machine and Cisco Devices**
Before using the application, ensure that SSH is enabled on your Cisco devices:

#### **Device-Side Configuration**
```plaintext
1. Set a username and password:
   username $user privilege 15 secret $pass

2. Set the domain name:
   ip domain-name $domain-name

3. Generate an RSA key (use the same key length as the server, e.g., 3072 bits):
   crypto key generate rsa modulus 3072

4. Enable SSH version 2:
   ip ssh version 2

5. Allow SSH connections:
   line vty 0 15
   login local
   transport input ssh
```
**Note:** If the device is a switch, you **must** assign an IP address to a VLAN. Contact your network administrator if needed.

---
## **Installation & Running the Application**

### **Clone the Repository**
Click on this **https://github.com/nouraldeen417/Network_App.git** to clone the repo:
```bash
git clone <repo_link_here>
cd Network_App
```

### **Understanding Important Files**
- **`hosts_sample`** – Sample Ansible inventory file. **Follow the same syntax** when adding your network devices.
- **`setup.sh`** – This script installs all necessary dependencies and prepares the environment.
- **`start.sh`** – This script starts the web application.

### **Run the Setup Script**
To set up the environment, run:
```bash
chmod +x setup.sh
./setup.sh
```

### **Start the Application**
Once the setup is complete, start the application with:
```bash
chmod +x start.sh
./start.sh
```

---
## **First-Time User Setup**
When you first run the application, **register a new user**. This user will be the **super admin** and will have full control over the platform, including:
- Approving other users.
- Managing permissions.
- Controlling network configurations.

---
## **Need Help?**
If you encounter any issues, feel free to contact us:
- **Email (Owner 1):** owner1@example.com
- **Email (Owner 2):** owner2@example.com

We hope this application makes network automation easier for you! 🚀

