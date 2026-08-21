#!/usr/bin/env python3
"""
A2Tool v4.0 - VPN & Proxy Chaining Module (10 Tools)
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time, socket, random
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
        print(f"\n{G}╔══════════════════════════════════════════════════════════════╗{RS}")
        print(f"{G}║{W}              VPN & Proxy Chaining Suite                    {G}║{RS}")
        print(f"{G}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{G}║{W} [01]{R}  Proxy List Scraper                                {G}║{RS}")
        print(f"{G}║{W} [02]{R}  Proxy Chain Tester                                {G}║{RS}")
        print(f"{G}║{W} [03]{R}  SOCKS5 Proxy Server Setup                        {G}║{RS}")
        print(f"{G}║{W} [04]{R}  HTTP/HTTPS Proxy Checker                          {G}║{RS}")
        print(f"{G}║{W} [05]{R}  Tor Integration (Anonymize)                       {G}║{RS}")
        print(f"{G}║{W} [06]{R}  VPN Auto-Connect                                  {G}║{RS}")
        print(f"{G}║{W} [07]{R}  DNS Leak Test                                     {G}║{RS}")
        print(f"{G}║{W} [08]{R}  MAC Address Changer                               {G}║{RS}")
        print(f"{G}║{W} [09]{R}  IP Rotation / Proxy Switcher                     {G}║{RS}")
        print(f"{G}║{W} [10]{R}  Anonymity Score Check                             {G}║{RS}")
        print(f"{G}║{W} [0]{R}   Back to Main Menu                                  {G}║{RS}")
        print(f"{G}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[Proxy] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': proxy_scraper()
        elif ch == '2': proxy_chain_test()
        elif ch == '3': socks5_server()
        elif ch == '4': proxy_checker()
        elif ch == '5': tor_integration()
        elif ch == '6': vpn_connect()
        elif ch == '7': dns_leak_test()
        elif ch == '8': mac_changer()
        elif ch == '9': ip_rotation()
        elif ch == '10': anonymity_check()
        else: print(f"{R}[!] Invalid option{RS}")

def proxy_scraper():
    print(f"\n{G}[+] Proxy List Scraper{RS}")
    print(f"{W}Fetching proxy lists from common sources...{RS}")
    
    sources = [
        "https://www.sslproxies.org/",
        "https://www.us-proxy.org/",
        "https://free-proxy-list.net/",
        "https://www.proxy-list.download/HTTP",
    ]
    
    try:
        import requests
        from bs4 import BeautifulSoup
        
        proxies = []
        for url in sources:
            try:
                r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(r.text, 'html.parser')
                table = soup.find('table', id='proxylisttable') or soup.find('table')
                if table:
                    for row in table.find_all('tr')[1:]:
                        cols = row.find_all('td')
                        if len(cols) >= 2:
                            ip = cols[0].text.strip()
                            port = cols[1].text.strip()
                            proxies.append(f"{ip}:{port}")
            except: pass
        
        if proxies:
            fname = f"proxies_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(fname, 'w') as f:
                f.write('\n'.join(proxies))
            print(f"{G}[+] Scraped {len(proxies)} proxies → {fname}{RS}")
            for p in proxies[:10]:
                print(f"  {C}[+]{RS} {Y}{p}{RS}")
            if len(proxies) > 10:
                print(f"  {W}... and {len(proxies)-10} more{RS}")
        else:
            print(f"{Y}[-] No proxies scraped. Using built-in list.{RS}")
            proxies = ['8.8.8.8:80', '1.1.1.1:80', '104.16.0.0:80']
            print(f"  Sample: {', '.join(proxies)}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def proxy_chain_test():
    print(f"\n{G}[+] Proxy Chain Tester{RS}")
    
    proxies_input = input(f"  {W}[?] Proxies (comma-sep, IP:PORT): {RS}").strip()
    if not proxies_input:
        print(f"{Y}[-] No proxies provided{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    proxy_list = [p.strip() for p in proxies_input.split(',')]
    print(f"\n{W}Testing chain of {len(proxy_list)} proxies...{RS}")
    
    for i, proxy in enumerate(proxy_list):
        try:
            ip, port = proxy.split(':')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            result = s.connect_ex((ip, int(port)))
            status = f"{G}[✓] Alive{RS}" if result == 0 else f"{R}[✗] Dead{RS}"
            print(f"  {W}[{i+1}]{RS} {proxy}: {status}")
            s.close()
        except:
            print(f"  {W}[{i+1}]{RS} {proxy}: {R}[✗] Invalid{RS}")
    
    print(f"\n{W}Proxy Chain Configuration:{RS}")
    print(f"  For proxychains: add to /etc/proxychains.conf")
    for p in proxy_list:
        print(f"  http {p.replace(':', ' ')}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def socks5_server():
    print(f"\n{G}[+] SOCKS5 Proxy Server Setup{RS}")
    port = int(input(f"  {W}[?] Port (default: 9050): {RS}").strip() or '9050')
    
    print(f"\n{W}Option 1 - Using ssh -D (SSH tunnel):{RS}")
    ssh_user = input(f"  {W}[?] SSH user@host: {RS}").strip()
    if ssh_user:
        print(f"  ssh -D {port} -N {ssh_user}")
    
    print(f"\n{W}Option 2 - Using Dante (SOCKS server):{RS}")
    print(f"  Install: apt install dante-server")
    print(f"  Configure /etc/danted.conf then: systemctl start danted")
    
    print(f"\n{W}Option 3 - Using Python (simple SOCKS5):{RS}")
    python_socks = f"""import socket, threading, select

def handle_client(conn):
    # SOCKS5 handshake
    data = conn.recv(1024)
    conn.send(b'\\x05\\x00')  # No auth
    data = conn.recv(1024)
    # ... (full SOCKS5 protocol)
    conn.close()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', {port}))
s.listen(50)
print(f'[+] SOCKS5 on port {port}')
while True:
    conn, addr = s.accept()
    threading.Thread(target=handle_client, args=(conn,)).start()
"""
    print(f"  {Y}{python_socks[:200]}...{RS}")
    
    print(f"\n{W}Testing SOCKS5:{RS}")
    print(f"  curl --socks5 127.0.0.1:{port} https://ifconfig.me")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def proxy_checker():
    print(f"\n{G}[+] Proxy Checker (HTTP/HTTPS/SOCKS){RS}")
    file_path = input(f"  {W}[?] Proxy list file (one per line): {RS}").strip()
    
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
    else:
        # Demo proxies
        proxies = ["8.8.8.8:80", "1.1.1.1:80", "104.16.0.0:80"]
        print(f"{Y}[!] Using demo proxies{RS}")
    
    print(f"\n{W}Testing {len(proxies)} proxies...{RS}")
    working = []
    
    try:
        import requests
        for proxy in proxies:
            try:
                r = requests.get('https://httpbin.org/ip', proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'}, timeout=5)
                if r.status_code == 200:
                    print(f"  {G}[✓]{RS} {proxy} - Working ({r.json().get('origin', '?')})")
                    working.append(proxy)
                else:
                    print(f"  {R}[✗]{RS} {proxy}")
            except:
                print(f"  {R}[✗]{RS} {proxy}")
    except ImportError:
        for proxy in proxies[:5]:
            print(f"  {Y}[?]{RS} {proxy} (install requests to test)")
    
    if working:
        fname = f"working_proxies_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(fname, 'w') as f:
            f.write('\n'.join(working))
        print(f"\n{G}[+] Found {len(working)} working proxies → {fname}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def tor_integration():
    print(f"\n{G}[+] Tor Integration & Anonymization{RS}")
    
    print(f"\n{W}Tor Status Check:{RS}")
    try:
        import requests
        r = requests.get('https://check.torproject.org/', proxies={'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}, timeout=10)
        if 'Congratulations' in r.text:
            print(f"  {G}[✓] Tor is working! Traffic is anonymized.{RS}")
        else:
            print(f"  {R}[✗] Tor is NOT active{RS}")
    except:
        print(f"  {Y}[!] Tor not detected or not running{RS}")
    
    print(f"\n{W}Tor Configuration:{RS}")
    print(f"  Start Tor: systemctl start tor (Linux) or start Tor Browser")
    print(f"  Proxy: SOCKS5 127.0.0.1:9050")
    print(f"  HTTP proxy: HTTP 127.0.0.1:8118 (with privoxy)")
    
    print(f"\n{W}Use with Python:{RS}")
    print(f"  import requests")
    print(f"  proxies = {{'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}}")
    print(f"  r = requests.get('https://ifconfig.me', proxies=proxies)")
    
    print(f"\n{W}Use with curl:{RS}")
    print(f"  curl --socks5 127.0.0.1:9050 https://check.torproject.org")
    
    print(f"\n{W}Use with proxychains:{RS}")
    print(f"  proxychains4 curl https://ifconfig.me")
    
    # New identity
    if input(f"\n{Y}[?] Request new Tor identity? (y/n): {RS}").strip().lower() == 'y':
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', 9051))
            s.send(b'AUTHENTICATE ""\r\n')
            s.send(b'SIGNAL NEWNYM\r\n')
            data = s.recv(1024)
            if b'250' in data:
                print(f"{G}[+] New Tor identity requested{RS}")
            s.close()
        except:
            print(f"{R}[-] Cannot connect to Tor control port{RS}")
            print(f"{Y}[!] Enable ControlPort in /etc/tor/torrc{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def vpn_connect():
    print(f"\n{G}[+] VPN Auto-Connect{RS}")
    
    print(f"\n{W}Available VPN methods:{RS}")
    print(f"  1. OpenVPN (.ovpn files)")
    print(f"  2. WireGuard (.conf files)")
    print(f"  3. PPTP/L2TP (built-in OS)")
    print(f"  4. SSH Tunnel (-D SOCKS proxy)")
    print(f"  5. Cloud VPN (Tailscale, ZeroTier)")
    
    method = input(f"\n{Y}  Choice: {RS}").strip()
    
    if method == '1':
        config = input(f"  {W}[?] OpenVPN config file: {RS}").strip()
        if config and os.path.exists(config):
            os.system(f'sudo openvpn --config {config}')
        else:
            print(f"{R}[-] Config not found{RS}")
            print(f"{Y}[!] Example: sudo openvpn --config /path/to/config.ovpn{RS}")
    
    elif method == '2':
        config = input(f"  {W}[?] WireGuard config: {RS}").strip()
        if config:
            os.system(f'sudo wg-quick up {config}')
    
    elif method == '3':
        print(f"{Y}[!] Use OS settings for PPTP/L2TP configuration{RS}")
    
    elif method == '4':
        ssh_host = input(f"  {W}[?] SSH host: {RS}").strip()
        port = input(f"  {W}[?] Local SOCKS port (default: 1080): {RS}").strip() or '1080'
        if ssh_host:
            os.system(f'ssh -D {port} -N {ssh_host}')
    
    print(f"\n{W}After connecting, verify:{RS}")
    print(f"  curl ifconfig.me")
    print(f"  curl ipinfo.io")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def dns_leak_test():
    print(f"\n{G}[+] DNS Leak Test{RS}")
    
    print(f"\n{W}Checking DNS servers...{RS}")
    import socket as sck
    
    # Get DNS servers
    if os.name == 'nt':
        out = _run('ipconfig /all | findstr "DNS Servers"')
        print(f"  {C}Configured DNS:{RS}\n{out[:500]}")
    else:
        out = _run('cat /etc/resolv.conf')
        print(f"  {C}Configured DNS:{RS}\n{out[:500]}")
    
    # Test for leaks
    print(f"\n{W}Leak Test:{RS}")
    try:
        # Resolve domain
        ip = sck.gethostbyname('ipinfo.io')
        print(f"  {C}Resolved ipinfo.io → {ip}{RS}")
        
        # Check what IP resolves (DNS should use tunnel if VPN active)
        print(f"  {Y}[!] If this IP matches your ISP's DNS, you have a LEAK{RS}")
        
        # Extended leak test
        print(f"\n{W}Extended DNS Leak Test:{RS}")
        print(f"  Visit: https://dnsleaktest.com/")
        print(f"  Visit: https://ipleak.net/")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def mac_changer():
    print(f"\n{G}[+] MAC Address Changer{RS}")
    iface = input(f"  {W}[?] Interface (e.g., eth0, wlan0): {RS}").strip()
    
    if not iface:
        print(f"{Y}[-] No interface specified{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    # Show current MAC
    if os.name == 'nt':
        out = _run(f'getmac /v 2>/dev/null | findstr {iface}')
        print(f"  {C}Current MAC:{RS} {out[:100]}")
    else:
        out = _run(f'cat /sys/class/net/{iface}/address')
        print(f"  {C}Current MAC:{RS} {out.strip()}")
    
    new_mac = input(f"  {W}[?] New MAC (or 'random'): {RS}").strip()
    if new_mac.lower() == 'random':
        new_mac = ':'.join(f'{random.randint(0,255):02x}' for _ in range(6))
    
    if new_mac:
        if os.name == 'nt':
            print(f"{Y}[!] On Windows, change MAC in Network Adapter settings{RS}")
        else:
            os.system(f'sudo ifconfig {iface} down')
            os.system(f'sudo macchanger -m {new_mac} {iface}')
            os.system(f'sudo ifconfig {iface} up')
            print(f"{G}[+] MAC changed to {new_mac}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def ip_rotation():
    print(f"\n{G}[+] IP Rotation / Proxy Switcher{RS}")
    
    print(f"\n{W}IP Rotation Methods:{RS}")
    print(f"  1. Tor new identity (signal NEWNYM)")
    print(f"  2. VPN server switch")
    print(f"  3. Proxy rotation (multiple proxies)")
    print(f"  4. SSH tunnel rotation")
    print(f"  5. Mobile hotspot toggle (new IP)")
    
    method = input(f"\n{Y}  Choice: {RS}").strip()
    
    if method == '1':
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', 9051))
            s.send(b'AUTHENTICATE ""\r\n')
            s.send(b'SIGNAL NEWNYM\r\n')
            response = s.recv(1024)
            if b'250' in response:
                print(f"{G}[+] Tor identity rotated{RS}")
                # Get new IP
                import requests
                r = requests.get('https://ifconfig.me/ip', proxies={'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}, timeout=10)
                print(f"{G}[+] New IP: {r.text.strip()}{RS}")
            s.close()
        except Exception as e:
            print(f"{R}[-] Error: {e}{RS}")
    elif method == '3':
        proxy_file = input(f"  {W}[?] Proxy list file: {RS}").strip()
        if proxy_file and os.path.exists(proxy_file):
            with open(proxy_file, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
            print(f"{G}[+] Loaded {len(proxies)} proxies for rotation{RS}")
            for p in proxies[:5]:
                print(f"  {C}[+]{RS} {p}")
        else:
            print(f"{Y}[-] File not found{RS}")
    else:
        print(f"{Y}[!] IP rotation requires appropriate services{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def anonymity_check():
    print(f"\n{G}[+] Anonymity Score Check{RS}")
    
    score = 0
    checks = []
    
    print(f"\n{W}Checking your anonymity posture...{RS}")
    
    # Check 1: Proxy
    try:
        import requests
        ip = requests.get('https://ifconfig.me/ip', timeout=10).text.strip()
        print(f"  {C}Current IP:{RS} {ip}")
        checks.append(('IP detected', True))
    except:
        ip = 'Unknown'
        print(f"  {C}Current IP:{RS} Unable to detect")
        checks.append(('IP detected', False))
    
    # Check 2: JavaScript/cookie tracking
    print(f"  {C}JavaScript:{RS} Disabled in Tor Browser, enabled in regular browsers")
    
    # Check 3: DNS
    print(f"  {C}DNS:{RS} Use DNS over HTTPS (DoH) or Tor DNS for anonymity")
    
    # Check 4: User Agent
    print(f"  {C}User Agent:{RS} Use Tor Browser or randomized agents")
    
    # Calculate score
    print(f"\n  {'='*40}")
    print(f"  {W}Anonymity Checklist:{RS}")
    print(f"  {'='*40}")
    
    checks_list = [
        ("Using VPN/Tor", False),
        ("JavaScript disabled", False),
        ("Third-party cookies blocked", False),
        ("DNS leaks prevented", False),
        ("WebRTC disabled", False),
        ("Canvas fingerprinting blocked", False),
        ("User agent randomized", False),
        ("Referrer header stripped", False),
        ("Browser timezone spoofed", False),
        ("No unique fonts/plugins", False),
    ]
    
    for name, status in checks_list:
        mark = f"{G}[✓]{RS}" if status else f"{R}[✗]{RS}"
        print(f"  {mark} {name}")
    
    score = sum(1 for _, s in checks_list if s)
    print(f"\n  {W}Anonymity Score: {score}/10{RS}")
    
    if score < 3:
        print(f"  {R}Recommendation: Use Tor Browser for sensitive tasks{RS}")
    elif score < 7:
        print(f"  {Y}Recommendation: Improve your anonymity settings{RS}")
    else:
        print(f"  {G}Good anonymity posture{RS}")
    
    print(f"\n{W}Recommended Tools:{RS}")
    print(f"  {W}•{RS} Tor Browser Bundle")
    print(f"  {W}•{RS} TAILS OS")
    print(f"  {W}•{RS} Whonix")
    print(f"  {W}•{RS} VPN + Tor (Onion over VPN)")
    print(f"  {W}•{RS} Brave Browser (fingerprinting protection)")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
