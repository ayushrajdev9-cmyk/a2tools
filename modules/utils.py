#!/usr/bin/env python3
"""
A2Tool v4.0 - Utilities Module
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time, platform, socket, hashlib, random, string, threading
from datetime import datetime
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except:
    class Fore: RED=GREEN=YELLOW=BLUE=MAGENTA=CYAN=WHITE='';RESET=''
    class Style: RESET_ALL='';BRIGHT='';DIM='';NORMAL=''

R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; B=Fore.BLUE
M=Fore.MAGENTA; C=Fore.CYAN; W=Fore.WHITE; RS=Style.RESET_ALL

OS_NAME = platform.system().lower()
IS_WIN = OS_NAME == 'windows'
IS_LNX = OS_NAME == 'linux'

def _run(cmd, shell=True, timeout=30):
    try: return subprocess.check_output(cmd, shell=shell, stderr=subprocess.STDOUT, timeout=timeout).decode('utf-8', errors='ignore')
    except: return ''

def run_external_tool(tool, choice, category):
    """Run an external tool with parameters"""
    print(f"\n{Y}[!] Running {tool} (option {choice}) in {category} category{RS}")
    if tool == 'nmap':
        target = input(f"  {W}[?] Target: {RS}").strip()
        print(f"{G}[+] Running nmap scan...{RS}")
        os.system(f'nmap -sV {target}')
    elif tool == 'sqlmap':
        target = input(f"  {W}[?] Target URL: {RS}").strip()
        print(f"{G}[+] Running sqlmap...{RS}")
        os.system(f'sqlmap -u {target} --batch')
    elif tool == 'hydra':
        target = input(f"  {W}[?] Target: {RS}").strip()
        service = input(f"  {W}[?] Service (ssh/ftp/http-post-form): {RS}").strip()
        user = input(f"  {W}[?] Username: {RS}").strip()
        wordlist = input(f"  {W}[?] Password list: {RS}").strip()
        print(f"{G}[+] Running hydra...{RS}")
        os.system(f'hydra -l {user} -P {wordlist} {target} {service}')
    else:
        print(f"{Y}[!] Tool {tool} not configured. Running raw...{RS}")
        os.system(f'{tool} --help 2>/dev/null || echo "Tool not found"')
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def system_info_dump(choice):
    """System information dump"""
    print(f"\n{G}[+] System Information Dump{RS}")
    
    if IS_WIN:
        cmds = {
            '1': 'systeminfo',
            '2': 'tasklist /svc',
            '3': 'wmic product get name,version',
            '4': 'wmic qfe list',
            '5': 'netstat -ano',
            '6': 'whoami /priv'
        }
        cmd = cmds.get(choice, 'systeminfo')
        out = _run(cmd)
        print(f"  {Y}{out[:2000]}{RS}")
    else:
        cmds = {
            '1': 'uname -a && cat /etc/os-release && lscpu 2>/dev/null || cat /proc/cpuinfo',
            '2': 'ps aux && ss -tlnp',
            '3': 'dpkg -l 2>/dev/null || rpm -qa 2>/dev/null || pacman -Q 2>/dev/null',
            '4': 'dmesg | grep -i error | head -20',
            '5': 'netstat -tulanp',
            '6': 'find / -perm -4000 2>/dev/null'
        }
        cmd = cmds.get(choice, 'uname -a')
        out = _run(cmd)
        print(f"  {Y}{out[:2000]}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def generate_password(length=16):
    """Generate a strong random password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return ''.join(random.choice(chars) for _ in range(length))

def hash_string(text, algo='sha256'):
    """Hash a string using various algorithms"""
    h = hashlib.new(algo)
    h.update(text.encode())
    return h.hexdigest()

def port_scan_thread(target, port, timeout=1):
    """Threaded port scanner helper"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((target, port))
        s.close()
        return port, result == 0
    except:
        return port, False

def scan_ports_threaded(target, ports, threads=100):
    """Multi-threaded port scanning"""
    print(f"{G}[+] Scanning {target} with {threads} threads...{RS}")
    results = []
    from concurrent.futures import ThreadPoolExecutor
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(port_scan_thread, target, p): p for p in ports}
        for future in concurrent.futures.as_completed(futures):
            port, is_open = future.result()
            if is_open:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = 'unknown'
                results.append((port, service))
    
    return results

def print_banner(text, color=C):
    """Print a formatted banner"""
    width = len(text) + 4
    print(f"{color}╔{'═' * width}╗{RS}")
    print(f"{color}║  {W}{text}{color}  ║{RS}")
    print(f"{color}╚{'═' * width}╝{RS}")

def save_to_file(filename, data):
    """Save data to file"""
    with open(filename, 'w') as f:
        f.write(data)
    print(f"{G}[+] Saved to {filename}{RS}")

def load_wordlist(path):
    """Load a wordlist file"""
    try:
        with open(path, 'r', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def check_root():
    """Check if running as root/administrator"""
    if IS_WIN:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    else:
        return os.geteuid() == 0

def get_public_ip():
    """Get public IP address"""
    try:
        import requests
        r = requests.get('https://api.ipify.org?format=json', timeout=10)
        return r.json()['ip']
    except:
        return 'Unknown'

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'

def loading_animation(duration=2):
    """Show a loading animation"""
    import itertools
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    end_time = time.time() + duration
    while time.time() < end_time:
        print(f'\r{spinner.__next__()} Working...', end='', flush=True)
        time.sleep(0.1)
    print('\r' + ' ' * 30, end='\r')
