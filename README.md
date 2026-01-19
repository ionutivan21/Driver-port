# Driver-port
Acest tool este asemănător lui nmap

# 🚗 Driver Port

**Driver Port** is an educational, nmap-like network port scanner written in Python.  
Designed to run in Termux and Linux environments.

## ✨ Features
- TCP Connect Scan
- Host discovery
- Light service detection
- Top ports scanning
- Multithreaded scanning
- Save results to file

## 🛠 Installation
```bash
pkg install python
pip install colorama
git clone https://github.com/ionutivan21/Driver-Port.git
cd Driver-Port
python driverport.py 127.0.0.1

#usage

python driverport.py <target>
python driverport.py <target> -p 1-1000
python driverport.py <target> --top
python driverport.py <target> -o output.txt
