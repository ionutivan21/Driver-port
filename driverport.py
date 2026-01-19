#!/usr/bin/env python3
# ==========================================
# Tool Name : Driver Port
# Author    : ionutivan21
# Version   : 1.1
# Purpose   : Nmap-like educational port scanner
# Platform  : Termux / Linux
# ==========================================

import socket
import threading
import argparse
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

AUTHOR = "ionutivan21"
VERSION = "1.1"
TOOL_NAME = "Driver Port"

TOP_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 139, 143,
    443, 445, 3306, 3389, 8080
]

SERVICE_PROBES = {
    21: b"USER anonymous\r\n",
    22: b"\r\n",
    25: b"HELO test\r\n",
    80: b"HEAD / HTTP/1.0\r\n\r\n",
    443: b"HEAD / HTTP/1.0\r\n\r\n",
}

BANNER = Fore.CYAN + f"""
██████╗ ██████╗ ██╗██╗   ██╗███████╗██████╗ 
██╔══██╗██╔══██╗██║██║   ██║██╔════╝██╔══██╗
██║  ██║██████╔╝██║██║   ██║█████╗  ██████╔╝
██║  ██║██╔══██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
██████╔╝██║  ██║██║ ╚████╔╝ ███████╗██║  ██║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

{TOOL_NAME} v{VERSION}
Author: {AUTHOR}
"""

print(BANNER)

# ---------- CLI ----------
parser = argparse.ArgumentParser(
    description=f"{TOOL_NAME} – nmap-like port scanner"
)
parser.add_argument("target", help="Target IP or hostname")
parser.add_argument("-p", "--ports", help="Port range (ex: 1-1000)")
parser.add_argument("--top", action="store_true", help="Scan top common ports")
parser.add_argument("-t", "--timeout", type=float, default=0.5)
parser.add_argument("-o", "--output", help="Save output to file")

args = parser.parse_args()

target = args.target
timeout = args.timeout
open_ports = []

# ---------- Host Discovery ----------
def host_alive():
    try:
        socket.gethostbyname(target)
        return True
    except:
        return False

print(Fore.YELLOW + f"[+] Scanning target: {target}")

if not host_alive():
    print(Fore.RED + "[!] Host seems down or invalid")
    exit()

print(Fore.GREEN + "[+] Host is alive\n")

# ---------- Port list ----------
if args.top:
    ports = TOP_PORTS
elif args.ports:
    try:
        start, end = map(int, args.ports.split("-"))
        ports = range(start, end + 1)
    except:
        print(Fore.RED + "[!] Invalid port range")
        exit()
else:
    ports = range(1, 1025)

# ---------- Scan ----------
def scan_port(port):
    try:
        s = socket.socket()
        s.settimeout(timeout)
        if s.connect_ex((target, port)) == 0:
            banner = "unknown"
            try:
                probe = SERVICE_PROBES.get(port, b"\r\n")
                s.send(probe)
                banner = s.recv(1024).decode(errors="ignore").strip()
            except:
                pass

            open_ports.append((port, banner))
            print(Fore.GREEN + f"[OPEN] {port:<5} | {banner}")
        s.close()
    except:
        pass

threads = []

start_time = datetime.now()

for p in ports:
    t = threading.Thread(target=scan_port, args=(p,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end_time = datetime.now()

# ---------- Output ----------
print(Style.BRIGHT + Fore.CYAN + "\nScan finished")
print(Fore.CYAN + f"Open ports: {len(open_ports)}")
print(Fore.CYAN + f"Time taken: {end_time - start_time}")

if args.output:
    with open(args.output, "w") as f:
        f.write(f"{TOOL_NAME} v{VERSION}\n")
        f.write(f"Target: {target}\n\n")
        for p, b in open_ports:
            f.write(f"{p} | {b}\n")
    print(Fore.YELLOW + f"[+] Results saved to {args.output}")
