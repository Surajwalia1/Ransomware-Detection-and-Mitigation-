# 🛡️ Ransomware and Network Monitoring System  

**A robust solution to secure your files and monitor your network traffic, equipped with ransomware detection, backup functionality, and live network monitoring. Built for modern cybersecurity needs.**

---

## 🚀 Features  

### 🔐 **Ransomware Monitoring**  
- Monitors files for unauthorized modifications.  
- Instantly creates backups for your critical data.  
- Deletes maliciously altered files to prevent further harm.  

### 🌐 **Network Monitoring**  
- Captures and logs real-time network traffic.  
- Provides insights into suspicious connections.  

### ⚙️ **Custom Configuration**  
- Upload files to monitor and set custom backup paths.  
- Password-protected controls for monitoring operations.  

### 📜 **Logs & Notifications**  
- View detailed logs for both file and network monitoring.  
- Ensure transparency and traceability of all actions.  

---

## 📂 Project Structure  

```bash  
📦 Project
├── Ransomware (Monitored files and backups)
│   ├── to_monitor/  
│   ├── replace_destination/  
├── templates/ (Frontend HTML templates)  
├── app.py (Flask-based backend logic)  
├── static/ (CSS, JS, and other static assets)


🛠️ Technologies Used
Frontend: HTML5, CSS3, Bootstrap 5, Font Awesome
Backend: Flask (Python), Watchdog, Scapy
Libraries: jQuery, Python threading, Werkzeug


🎯 Getting Started
Clone the Repository

bash
git clone https://github.com/Surajwalia1/ransomware-network-monitoring.git  
cd ransomware-network-monitoring

Install Dependencies
bash
pip install -r requirements.txt
 
Run the Application
bash
python app.py  
Access the web interface at http://localhost:5000/.

# 🔐 RansomShield: Advanced Ransomware Defense System

## 🔑 How to Use

1️⃣ **Configure Monitoring**
- Upload the file to monitor.
- Set the backup directory path.

2️⃣ **Start Monitoring**
- Use password-protected controls to start/stop monitoring.

3️⃣ **View Logs**
- Check detailed logs for ransomware and network activity via the UI.

---

## 💡 Key Methodologies

- **File Monitoring**: Uses `Watchdog` to monitor file changes and detect anomalies.
- **Network Monitoring**: Employs `Scapy` for capturing and logging packet-level details.
- **Backup Strategy**: Automatically creates backups when malicious changes are detected.


---

## 🧑‍💻 Contributions

We welcome contributions! If you’d like to improve this project, feel free to:

1. Fork the repository.
2. Create a new branch for your feature.
3. Submit a pull request.

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

