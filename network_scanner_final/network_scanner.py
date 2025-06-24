
import customtkinter as ctk
import threading
import socket
import time

# Globals
stop_scan = False
open_ports_count = 0

# Scanner logic
def scan_network(subnet, ports_input, scan_all):
    global stop_scan, open_ports_count
    stop_scan = False
    open_ports_count = 0
    result_text.delete(1.0, "end")
    progress_bar.set(0)
    status_label.configure(text="Scanning...")
    total_ips = 254

    if scan_all:
        ports = range(1, 65536)
    else:
        ports = [int(p.strip()) for p in ports_input.split(",") if p.strip().isdigit()]
    
    def scan_thread():
        global open_ports_count
        for i in range(1, 255):
            if stop_scan:
                break
            ip = f"{subnet}.{i}"
            found = scan_ip(ip, ports)
            if found > 0:
                open_ports_count += found
            progress_bar.set(i / total_ips)
            status_label.configure(text=f"Scanning... Open ports: {open_ports_count}")
        
        if not stop_scan:
            status_label.configure(text=f"Scan complete! Total open ports: {open_ports_count}")
        else:
            status_label.configure(text=f"Scan stopped. Open ports: {open_ports_count}")

    threading.Thread(target=scan_thread).start()

def scan_ip(ip, ports):
    found_ports = 0
    for port in ports:
        if stop_scan:
            break
        try:
            socket.setdefaulttimeout(0.5)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((ip, port))
            if result == 0:
                result_text.insert("end", f"[+] {ip} : Port {port} OPEN\n")
                found_ports += 1
            s.close()
        except:
            pass
    return found_ports

def stop_scanning():
    global stop_scan
    stop_scan = True
    status_label.configure(text="Stopping...")

# GUI setup
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Modern Network Scanner (Async + Stop + Counter)")

subnet_label = ctk.CTkLabel(root, text="Subnet (e.g. 192.168.1)")
subnet_label.pack(pady=5)
subnet_entry = ctk.CTkEntry(root)
subnet_entry.pack(pady=5)

port_label = ctk.CTkLabel(root, text="Ports (comma separated, e.g. 22,80,443)")
port_label.pack(pady=5)
port_entry = ctk.CTkEntry(root)
port_entry.pack(pady=5)

scan_all_var = ctk.BooleanVar()
scan_all_checkbox = ctk.CTkCheckBox(root, text="Scan ALL ports (1-65535)", variable=scan_all_var)
scan_all_checkbox.pack(pady=5)

scan_button = ctk.CTkButton(root, text="Start Scan", 
    command=lambda: scan_network(subnet_entry.get(), port_entry.get(), scan_all_var.get()))
scan_button.pack(pady=10)

stop_button = ctk.CTkButton(root, text="Stop Scan", command=stop_scanning)
stop_button.pack(pady=5)

progress_bar = ctk.CTkProgressBar(root, orientation="horizontal", width=400)
progress_bar.pack(pady=10)
progress_bar.set(0)

status_label = ctk.CTkLabel(root, text="Idle")
status_label.pack(pady=5)

result_text = ctk.CTkTextbox(root, height=400, width=700)
result_text.pack(pady=10)

root.mainloop()
