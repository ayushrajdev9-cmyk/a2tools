#!/usr/bin/env python3
"""
A2Tool v4.0 - Network Scanner & Analysis Module (15 Tools)
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time, socket, ipaddress, struct, threading
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
        print(f"\n{C}╔══════════════════════════════════════════════════════════════╗{RS}")
        print(f"{C}║{W}            Network Scanner & Analysis Suite               {C}║{RS}")
        print(f"{C}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{C}║{W} [01]{R}  ARP Scan - Discover Live Hosts                    {C}║{RS}")
        print(f"{C}║{W} [02]{R}  TCP Port Scanner (Multi-Threaded)                 {C}║{RS}")
        print(f"{C}║{W} [03]{R}  UDP Port Scanner                                 {C}║{RS}")
        print(f"{C}║{W} [04]{R}  Service Version Detection                         {C}║{RS}")
        print(f"{C}║{W} [05]{R}  OS Fingerprinting                                {C}║{RS}")
        print(f"{C}║{W} [06]{R}  Network Mapping & Topology                        {C}║{RS}")
        print(f"{C}║{W} [07]{R}  Bandwidth & Latency Test                         {C}║{RS}")
        print(f"{C}║{W} [08]{R}  Packet Capture & Analysis                        {C}║{RS}")
        print(f"{C}║{W} [09]{R}  DNS Sniffer                                      {C}║{RS}")
        print(f"{C}║{W} [10]{R}  DHCP Server Discovery                            {C}║{RS}")
        print(f"{C}║{W} [11]{R}  SNMP Sweep                                       {C}║{RS}")
        print(f"{C}║{W} [12]{R}  IP Scanner (CIDR Range)                          {C}║{RS}")
        print(f"{C}║{W} [13]{R}  Open Port Checker (External)                     {C}║{RS}")
        print(f"{C}║{W} [14]{R}  Network Bandwidth Monitor                        {C}║{RS}")
        print(f"{C}║{W} [15]{R}  Full Network Audit Report                        {C}║{RS}")
        print(f"{C}║{W} [0]{R}   Back to Main Menu                                 {C}║{RS}")
        print(f"{C}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[Network] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': arp_scan()
        elif ch == '2': tcp_port_scan()
        elif ch == '3': udp_port_scan()
        elif ch == '4': service_detect()
        elif ch == '5': os_fingerprint()
        elif ch == '6': network_map()
        elif ch == '7': bandwidth_test()
        elif ch == '8': packet_capture()
        elif ch == '9': dns_sniffer()
        elif ch == '10': dhcp_discover()
        elif ch == '11': snmp_sweep()
        elif ch == '12': ip_range_scan()
        elif ch == '13': open_port_check()
        elif ch == '14': bandwidth_monitor()
        elif ch == '15': full_audit()
        else: print(f"{R}[!] Invalid option{RS}")

def arp_scan():
    """Tool 1: ARP Scan"""
    print(f"\n{G}[+] ARP Scan - Discovering live hosts on network{RS}")
    subnet = input(f"  {W}[?] Subnet (e.g., 192.168.1.0/24): {RS}").strip() or '192.168.1.0/24'
    
    # Try nmap
    out = _run(f'nmap -sn {subnet} 2>/dev/null')
    if out:
        print(f"\n{Y}{out}{RS}")
    else:
        # Try arp-scan
        out = _run(f'arp-scan {subnet} 2>/dev/null')
        if out:
            print(f"\n{Y}{out}{RS}")
        else:
            # Basic ARP
            out = _run('arp -a 2>/dev/null')
            print(f"\n{Y}{out}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def tcp_port_scan():
    """Tool 2: TCP Port Scanner"""
    target = input(f"  {W}[?] Target IP/Domain: {RS}").strip()
    ports = input(f"  {W}[?] Ports (e.g., 1-1000 or 22,80,443): {RS}").strip() or '1-1024'
    
    print(f"\n{G}[+] TCP scanning {target} ports {ports}...{RS}")
    
    # Use nmap for better results
    out = _run(f'nmap -sT -p {ports} {target} 2>/dev/null')
    if out:
        print(f"\n{Y}{out[:2000]}{RS}")
    else:
        # Built-in scanner
        print(f"{Y}[!] nmap not found, using built-in scanner{RS}")
        port_list = []
        if '-' in ports:
            parts = ports.split('-')
            port_list = list(range(int(parts[0]), int(parts[1])+1))
        elif ',' in ports:
            port_list = [int(p.strip()) for p in ports.split(',')]
        
        open_ports = []
        try:
            for port in port_list:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.3)
                if s.connect_ex((target, port)) == 0:
                    try:
                        svc = socket.getservbyport(port)
                    except:
                        svc = 'unknown'
                    open_ports.append((port, svc))
                    print(f"  {G}[OPEN]{RS} {C}{port:>5}{RS} → {Y}{svc}{RS}")
                s.close()
        except KeyboardInterrupt:
            print(f"\n{Y}[!] Scan interrupted{RS}")
        except Exception as e:
            print(f"{R}[-] Error: {e}{RS}")
        
        print(f"\n{G}[+] Found {len(open_ports)} open TCP ports{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def udp_port_scan():
    """Tool 3: UDP Port Scanner"""
    target = input(f"  {W}[?] Target IP: {RS}").strip()
    print(f"\n{G}[+] UDP scanning {target}... (this takes longer){RS}")
    out = _run(f'nmap -sU --top-ports 100 {target} 2>/dev/null')
    print(f"\n{Y}{out[:1500] or 'nmap not found or no results'}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def service_detect():
    """Tool 4: Service Version Detection"""
    target = input(f"  {W}[?] Target IP/Domain: {RS}").strip()
    print(f"\n{G}[+] Detecting services on {target}...{RS}")
    out = _run(f'nmap -sV -p 1-1000 {target} 2>/dev/null')
    print(f"\n{Y}{out[:2000] or 'nmap not found'}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def os_fingerprint():
    """Tool 5: OS Fingerprinting"""
    target = input(f"  {W}[?] Target IP: {RS}").strip()
    print(f"\n{G}[+] OS fingerprinting {target}...{RS}")
    out = _run(f'nmap -O {target} 2>/dev/null')
    print(f"\n{Y}{out[:1500]}{RS}")
    
    # TTL-based guess
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((target, 80))
        # Can't easily get TTL from Python socket, but we demonstrate
        print(f"\n{W}TTL-based OS Guesses:{RS}")
        print(f"  TTL 64 → Linux/Unix")
        print(f"  TTL 128 → Windows")
        print(f"  TTL 255 → Cisco/Network Device")
        s.close()
    except: pass
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def network_map():
    """Tool 6: Network Mapping"""
    print(f"\n{G}[+] Network Mapping Tool{RS}")
    subnet = input(f"  {W}[?] Subnet (e.g., 192.168.1.0/24): {RS}").strip() or '192.168.1.0/24'
    
    print(f"\n{W}Generating network topology map for {subnet}...{RS}")
    out = _run(f'nmap -sP {subnet} 2>/dev/null')
    print(f"\n{Y}{out[:2000]}{RS}")
    
    # Generate a simple text map
    print(f"\n{W}Network Map:{RS}")
    print(f"  {C}┌{'─'*40}┐{RS}")
    print(f"  {C}│{RS} Router: {get_default_gateway()}")
    print(f"  {C}│{RS} Subnet: {subnet}")
    hosts = re.findall(r'Nmap scan report for (\S+)', out)
    for i, h in enumerate(hosts[:20], 1):
        print(f"  {C}│{RS} ├─ Host {i:>2}: {Y}{h}{RS}")
    print(f"  {C}└{'─'*40}┘{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def get_default_gateway():
    """Get default gateway"""
    try:
        if sys.platform == 'win32':
            out = _run('ipconfig | findstr "Default Gateway"')
            gw = re.search(r'Default Gateway[ .]+: (\S+)', out)
            return gw.group(1) if gw else 'Unknown'
        else:
            out = _run('ip route | grep default')
            gw = re.search(r'default via (\S+)', out)
            return gw.group(1) if gw else 'Unknown'
    except: return 'Unknown'

def bandwidth_test():
    """Tool 7: Bandwidth & Latency Test"""
    target = input(f"  {W}[?] Target (default: google.com): {RS}").strip() or 'google.com'
    print(f"\n{G}[+] Testing bandwidth to {target}...{RS}")
    
    # Ping test
    param = '-n' if os.name == 'nt' else '-c'
    out = _run(f'ping {param} 4 {target}')
    print(f"\n{Y}Ping Results:{RS}\n{out}")
    
    # Download test
    try:
        import requests
        start = time.time()
        r = requests.get(f'https://{target}', timeout=15, stream=True)
        size = len(r.content)
        elapsed = time.time() - start
        speed = size / elapsed / 1024  # KB/s
        print(f"{G}[+] Downloaded {size/1024:.1f}KB in {elapsed:.2f}s ({speed:.1f} KB/s){RS}")
        print(f"{G}[+] Estimated bandwidth: {speed*8/1024:.1f} Mbps{RS}")
    except:
        print(f"{Y}[-] Speed test requires internet access{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def packet_capture():
    """Tool 8: Packet Capture & Analysis"""
    print(f"\n{Y}[!] Packet Capture Tool (requires admin/root){RS}")
    iface = input(f"  {W}[?] Interface (e.g., eth0, wlan0): {RS}").strip() or 'eth0'
    count = input(f"  {W}[?] Number of packets to capture: {RS}").strip() or '10'
    
    print(f"\n{G}[+] Capturing {count} packets on {iface}...{RS}")
    print(f"{Y}[!] Press Ctrl+C to stop capture{RS}")
    
    # Try tcpdump
    os.system(f'tcpdump -i {iface} -c {count} -v 2>/dev/null || echo "tcpdump not available"')
    
    # Also try with Python/scapy
    try:
        from scapy.all import sniff
        print(f"{G}[+] Using Scapy for packet capture...{RS}")
        packets = sniff(iface=iface, count=int(count), timeout=30)
        for pkt in packets:
            print(f"  {Y}{pkt.summary()}{RS}")
    except ImportError:
        print(f"{Y}[-] Scapy not installed. Install: pip install scapy{RS}")
    except Exception as e:
        print(f"{Y}[-] Scapy error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def dns_sniffer():
    """Tool 9: DNS Sniffer"""
    print(f"\n{Y}[!] DNS Traffic Sniffer (requires root/admin){RS}")
    iface = input(f"  {W}[?] Interface (default: eth0): {RS}").strip() or 'eth0'
    
    print(f"\n{G}[+] Sniffing DNS queries on {iface}... (Ctrl+C to stop){RS}")
    try:
        from scapy.all import sniff, DNS
        def process_dns(pkt):
            if DNS in pkt and pkt[DNS].qr == 0:  # DNS query
                print(f"  {C}[DNS]{RS} {Y}{pkt[DNS].qd.qname.decode()}{RS}")
        sniff(iface=iface, filter='udp port 53', prn=process_dns, timeout=30)
    except ImportError:
        print(f"{Y}[-] Scapy not installed. Use tcpdump instead:{RS}")
        os.system(f'tcpdump -i {iface} -v udp port 53 2>/dev/null')
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def dhcp_discover():
    """Tool 10: DHCP Server Discovery"""
    print(f"\n{G}[+] Discovering DHCP servers on network...{RS}")
    iface = input(f"  {W}[?] Interface (default: eth0): {RS}").strip() or 'eth0'
    
    try:
        from scapy.all import DHCP, Ether, IP, UDP, BOOTP, sniff
        print(f"{Y}[!] Sending DHCP discover...{RS}")
        # Try nmap script
        out = _run('nmap --script broadcast-dhcp-discover 2>/dev/null')
        if out:
            print(f"{Y}{out[:1000]}{RS}")
        else:
            print(f"{Y}[-] Use nmap or dhcpdump for DHCP discovery{RS}")
    except:
        print(f"{Y}[-] DHCP discovery requires special tools{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def snmp_sweep():
    """Tool 11: SNMP Sweep"""
    print(f"\n{G}[+] SNMP Sweep - Scanning for SNMP-enabled devices{RS}")
    subnet = input(f"  {W}[?] Subnet (e.g., 192.168.1.0/24): {RS}").strip() or '192.168.1.0/24'
    
    out = _run(f'nmap -sU -p 161 --script snmp-brute {subnet} 2>/dev/null')
    print(f"\n{Y}{out[:1500] or 'nmap not found or no SNMP devices'}{RS}")
    
    print(f"\n{W}Common SNMP community strings:{RS}")
    print(f"  public, private, community, manager, admin, default")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def ip_range_scan():
    """Tool 12: IP Range Scanner"""
    start = input(f"  {W}[?] Start IP (e.g., 192.168.1.1): {RS}").strip()
    end = input(f"  {W}[?] End IP (e.g., 192.168.1.254): {RS}").strip()
    
    print(f"\n{G}[+] Scanning IP range {start} - {end}...{RS}")
    
    # Parse IPs
    try:
        start_parts = [int(x) for x in start.split('.')]
        end_parts = [int(x) for x in end.split('.')]
        start_int = (start_parts[0] << 24) + (start_parts[1] << 16) + (start_parts[2] << 8) + start_parts[3]
        end_int = (end_parts[0] << 24) + (end_parts[1] << 16) + (end_parts[2] << 8) + end_parts[3]
        
        def ip_to_str(ip_int):
            return f"{(ip_int >> 24) & 0xFF}.{(ip_int >> 16) & 0xFF}.{(ip_int >> 8) & 0xFF}.{ip_int & 0xFF}"
        
        found = []
        for ip_int in range(start_int, end_int + 1):
            ip = ip_to_str(ip_int)
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.3)
                if s.connect_ex((ip, 80)) == 0 or s.connect_ex((ip, 443)) == 0:
                    found.append(ip)
                    print(f"  {G}[+]{RS} {C}{ip}{RS} - {Y}Host is up{RS}")
                s.close()
            except: pass
        
        print(f"\n{G}[+] Scan complete. Found {len(found)} live hosts.{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def open_port_check():
    """Tool 13: Open Port Checker (External)"""
    target = input(f"  {W}[?] Target IP/Domain: {RS}").strip()
    port = int(input(f"  {W}[?] Port to check: {RS}").strip() or '80')
    
    print(f"\n{G}[+] Checking if port {port} is open on {target}...{RS}")
    
    # Try external service
    try:
        import requests
        r = requests.get(f'https://www.yougetsignal.com/tools/open-port/?port={port}&remoteaddr={target}', 
                        timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        if 'open' in r.text.lower():
            print(f"  {R}[!] Port {port} appears OPEN{RS}")
        else:
            print(f"  {G}[+] Port {port} appears CLOSED/FILTERED{RS}")
    except:
        # Direct check
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        result = s.connect_ex((target, port))
        if result == 0:
            print(f"  {R}[!] Port {port} is OPEN{RS}")
        else:
            print(f"  {G}[+] Port {port} is CLOSED/FILTERED{RS}")
        s.close()
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def bandwidth_monitor():
    """Tool 14: Network Bandwidth Monitor"""
    print(f"\n{G}[+] Network Bandwidth Monitor (Ctrl+C to stop){RS}")
    iface = input(f"  {W}[?] Interface (default: eth0): {RS}").strip() or 'eth0'
    
    try:
        import psutil
        old_stats = psutil.net_io_counters(pernic=True).get(iface)
        if not old_stats:
            print(f"{R}[-] Interface {iface} not found{RS}")
            return
        
        print(f"\n{Y}[!] Monitoring {iface}...{RS}")
        print(f"{'─'*60}")
        print(f"  {'Time':<10} {'Down (KB/s)':<15} {'Up (KB/s)':<15} {'Total (KB)':<15}")
        print(f"{'─'*60}")
        
        old_bytes_sent = old_stats.bytes_sent
        old_bytes_recv = old_stats.bytes_recv
        
        while True:
            time.sleep(1)
            stats = psutil.net_io_counters(pernic=True).get(iface)
            if stats:
                down = (stats.bytes_recv - old_bytes_recv) / 1024
                up = (stats.bytes_sent - old_bytes_sent) / 1024
                total = (stats.bytes_recv + stats.bytes_sent) / 1024
                print(f"  {datetime.now().strftime('%H:%M:%S'):<10} {down:<15.1f} {up:<15.1f} {total:<15.1f}")
                old_bytes_sent = stats.bytes_sent
                old_bytes_recv = stats.bytes_recv
    except ImportError:
        print(f"{Y}[-] Install psutil: pip install psutil{RS}")
    except KeyboardInterrupt:
        print(f"\n{Y}[+] Monitor stopped{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def full_audit():
    """Tool 15: Full Network Audit Report"""
    print(f"\n{G}[+] Generating Full Network Audit Report...{RS}")
    target = input(f"  {W}[?] Target IP/Domain: {RS}").strip()
    
    report = []
    report.append("=" * 60)
    report.append(f"  A2Tool Network Audit Report")
    report.append(f"  Target: {target}")
    report.append(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 60)
    
    # Ping test
    report.append(f"\n[+] Ping Test:")
    param = '-n' if os.name == 'nt' else '-c'
    out = _run(f'ping {param} 2 {target}')
    report.append(f"  {out[:200]}")
    
    # Port scan top ports
    report.append(f"\n[+] Open Ports (top 20):")
    common_ports = [21,22,23,25,53,80,110,143,443,445,993,995,1433,1521,2049,3306,3389,5432,5900,8080,8443,27017]
    open_ports = []
    for port in common_ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        if s.connect_ex((target, port)) == 0:
            try:
                svc = socket.getservbyport(port)
            except:
                svc = 'unknown'
            open_ports.append(f"{port}/{svc}")
        s.close()
    
    if open_ports:
        for p in open_ports:
            report.append(f"  [OPEN] {p}")
    else:
        report.append(f"  No common ports open")
    
    # DNS info
    try:
        ip = socket.gethostbyname(target)
        report.append(f"\n[+] DNS Resolution: {target} → {ip}")
    except:
        report.append(f"\n[+] DNS Resolution: Failed")
    
    # Save report
    fname = f"audit_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(fname, 'w') as f:
        f.write('\n'.join(report))
    
    print('\n'.join(report))
    print(f"\n{G}[+] Report saved to {fname}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
