
from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename
import threading
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from scapy.all import sniff, IP


MONITOR_DIR = None
BACKUP_DIR = None
log_messages = []
monitor_password = None  
app = Flask(__name__)
monitor_thread = None
observer = None
is_monitoring = False


network_logs = []  
network_thread = None  
network_monitoring_active = False


os.makedirs('./Ransomware/replace_destination', exist_ok=True)



def log_message(message):
    """Log a message to the shared log list."""
    global log_messages
    log_messages.append(message)
    print(message)



class RansomwareHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.monitored_file = None
        self.original_content = None
        self._initialize_tracked_file()

    def _initialize_tracked_file(self):
        """Initialize tracking for the user-provided file."""
        if MONITOR_DIR:
            for filename in os.listdir(MONITOR_DIR):
                file_path = os.path.join(MONITOR_DIR, filename)
                if os.path.isfile(file_path):
                    self.monitored_file = filename
                    with open(file_path, "rb") as f:
                        self.original_content = f.read()
            log_message("Initialized tracking for the uploaded file.")

    def on_modified(self, event):
        """Detect modifications to the monitored file."""
        if self.monitored_file and os.path.basename(event.src_path) == self.monitored_file:
            with open(event.src_path, "rb") as f:
                current_content = f.read()

            if self.original_content and current_content != self.original_content:
                log_message(f"Content change detected in {self.monitored_file}")

                
                self._create_backup(self.monitored_file)

                
                try:
                    os.remove(event.src_path)
                    log_message(f"Monitored file {self.monitored_file} has been deleted due to content change.")
                except Exception as e:
                    log_message(f"Failed to delete monitored file {self.monitored_file}: {e}")

                
                self.original_content = current_content
            else:
                log_message(f"No content change detected in {self.monitored_file}")

    def on_deleted(self, event):
        """Handle file deletion and create a backup if needed."""
        if self.monitored_file and os.path.basename(event.src_path) == self.monitored_file:
            log_message(f"File {self.monitored_file} was deleted.")
            # Create backup of the file content at the time of deletion
            self._create_backup(self.monitored_file)

    def _create_backup(self, filename):
        # Ensure backup directory exists
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)

        backup_path = os.path.join(BACKUP_DIR, filename)
        try:
            with open(backup_path, "wb") as f_backup:
                f_backup.write(self.original_content)
            log_message(f"Backup created for {filename} at {backup_path}")
        except Exception as e:
            log_message(f"Failed to create backup for {filename}: {e}")


def start_monitoring():
    """Start directory monitoring."""
    global monitor_thread, observer, is_monitoring
    if not MONITOR_DIR or not BACKUP_DIR:
        log_message("Please configure monitoring and backup paths first.")
        return "Paths not configured."
    if is_monitoring:
        return "Monitoring is already running."
    is_monitoring = True
    observer = Observer()
    event_handler = RansomwareHandler()
    observer.schedule(event_handler, path=MONITOR_DIR, recursive=False)
    monitor_thread = threading.Thread(target=observer.start)
    monitor_thread.start()
    log_message("Monitoring started.")


def stop_monitoring():
    """Stop directory monitoring."""
    global observer, is_monitoring
    if not is_monitoring:
        return "Monitoring is not running."
    observer.stop()
    observer.join()
    is_monitoring = False
    log_message("Monitoring stopped.")



def process_packet(packet):
    """Process each captured packet and log network traffic."""
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        log_entry = f"Packet: {ip_src} -> {ip_dst}"
        network_logs.append(log_entry)
        print(log_entry)  # Log to console


def start_network_monitoring():
    """Start monitoring network traffic."""
    global network_thread, network_monitoring_active
    if network_monitoring_active:
        return "Network monitoring is already active."

    def monitor():
        try:
            sniff(filter="ip", prn=process_packet, store=0)
        except Exception as e:
            network_logs.append(f"Error in network monitoring: {e}")
        finally:
            network_monitoring_active = False

    network_thread = threading.Thread(target=monitor, daemon=True)
    network_thread.start()
    network_monitoring_active = True
    network_logs.append("Started network monitoring.")
    return "Network monitoring started."


def stop_network_monitoring():
    """Stop monitoring network traffic."""
    global network_monitoring_active
    if not network_monitoring_active:
        return "Network monitoring is not active."

    network_monitoring_active = False
    network_logs.append("Stopped network monitoring.")
    return "Network monitoring stopped."



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start")
def start():
    start_monitoring()
    return jsonify({"message": "Monitoring started."})


@app.route("/stop")
def stop():
    stop_monitoring()
    return jsonify({"message": "Monitoring stopped."})


@app.route("/logs")
def logs():
    return jsonify({"logs": log_messages})


@app.route("/backups")
def backups():
    backup_files = os.listdir(BACKUP_DIR)
    return jsonify({"backups": backup_files})


@app.route("/configure", methods=["POST"])
def configure():
    global MONITOR_DIR, BACKUP_DIR

    
    if "monitor-file" not in request.files or "backup-folder" not in request.form:
        return jsonify({"message": "File or backup path missing."}), 400

    monitor_file = request.files["monitor-file"]
    backup_folder = request.form["backup-folder"]

    
    MONITOR_DIR = "./Ransomware/to_monitor"
    os.makedirs(MONITOR_DIR, exist_ok=True)

    file_path = os.path.join(MONITOR_DIR, secure_filename(monitor_file.filename))
    monitor_file.save(file_path)

    
    BACKUP_DIR = os.path.abspath(backup_folder)
    os.makedirs(BACKUP_DIR, exist_ok=True)

    log_message(f"Monitoring set for file: {file_path}")
    log_message(f"Backup folder set to: {BACKUP_DIR}")

    return jsonify({"message": "Configuration successful."})


@app.route("/set-password", methods=["POST"])
def set_password():
    global monitor_password
    data = request.json
    if "password" not in data:
        return jsonify({"message": "Password is required."}), 400

    monitor_password = data["password"]
    return jsonify({"message": "Password set successfully."})


@app.route("/validate-password", methods=["POST"])
def validate_password():
    global monitor_password
    data = request.json
    if "password" not in data:
        return jsonify({"message": "Password is required."}), 400

    if data["password"] == monitor_password:
        return jsonify({"message": "Password validated successfully."})
    else:
        return jsonify({"message": "Invalid password."}), 403


@app.route("/start-network")
def start_network():
    message = start_network_monitoring()
    return jsonify({"message": message})


@app.route("/stop-network")
def stop_network():
    message = stop_network_monitoring()
    return jsonify({"message": message})


@app.route("/network-logs")
def get_network_logs():
    return jsonify({"logs": network_logs})


if __name__ == "__main__":
    app.run(debug=True)



