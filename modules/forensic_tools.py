#!/usr/bin/env python3
"""
A2Tool v4.0 - Forensic & Anti-Forensic Tools Module (10 Tools)
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time, shutil
from datetime import datetime
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except:
    class Fore: RED=GREEN=YELLOW=BLUE=MAGENTA=CYAN=WHITE='';RESET=''
    Style=Fore

R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; B=Fore.BLUE
M=Fore.MAGENTA; C=Fore.CYAN; W=Fore.WHITE; RS=Style.RESET_ALL

def _run(cmd, shell=True, timeout=30):
    try: return subprocess.check_output(cmd, shell=shell, stderr=subprocess.STDOUT, timeout=timeout).decode('utf-8', errors='ignore')
    except: return ''

def menu():
    while True:
        print(f"\n{M}╔══════════════════════════════════════════════════════════════╗{RS}")
        print(f"{M}║{W}           Forensic & Anti-Forensic Tools                   {M}║{RS}")
        print(f"{M}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{M}║{W} [01]{R}  Disk / Partition Analysis                          {M}║{RS}")
        print(f"{M}║{W} [02]{R}  Recover Deleted Files                              {M}║{RS}")
        print(f"{M}║{W} [03]{R}  Memory Dump Analysis                               {M}║{RS}")
        print(f"{M}║{W} [04]{R}  Log Wiping                                        {M}║{RS}")
        print(f"{M}║{W} [05]{R}  File Shredder (Secure Delete)                     {M}║{RS}")
        print(f"{M}║{W} [06]{R}  Timestamp Manipulation                             {M}║{RS}")
        print(f"{M}║{W} [07]{R}  Browser Forensics (History/Cookies)                {M}║{RS}")
        print(f"{M}║{W} [08]{R}  Network Forensics (PCAP Analysis)                  {M}║{RS}")
        print(f"{M}║{W} [09]{R}  Registry Forensics (Windows)                      {M}║{RS}")
        print(f"{M}║{W} [10]{R}  Anti-Forensic Data Hiding                         {M}║{RS}")
        print(f"{M}║{W} [0]{R}   Back to Main Menu                                  {M}║{RS}")
        print(f"{M}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[Forensic] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': disk_analysis()
        elif ch == '2': recover_files()
        elif ch == '3': memory_analysis()
        elif ch == '4': log_wiping()
        elif ch == '5': file_shredder()
        elif ch == '6': timestamp_manip()
        elif ch == '7': browser_forensics()
        elif ch == '8': network_forensics()
        elif ch == '9': registry_forensics()
        elif ch == '10': anti_forensic_hide()
        else: print(f"{R}[!] Invalid option{RS}")

def disk_analysis():
    print(f"\n{G}[+] Disk / Partition Analysis{RS}")
    
    if os.name == 'nt':
        print(f"\n{W}Windows Disk Info:{RS}")
        out = _run('wmic diskdrive get model,size,status')
        print(f"{Y}{out[:1000]}{RS}")
        out = _run('wmic logicaldisk get caption,description,filesystem,size,freespace')
        print(f"{Y}{out[:1000]}{RS}")
    else:
        print(f"\n{W}Linux Disk Info:{RS}")
        out = _run('lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE 2>/dev/null || fdisk -l 2>/dev/null')
        print(f"{Y}{out[:1500]}{RS}")
        out = _run('df -h 2>/dev/null')
        print(f"{Y}{out[:1000]}{RS}")
    
    # Partition table
    print(f"\n{W}Partition Table:{RS}")
    if os.name == 'nt':
        out = _run('diskpart /s 2>/dev/null || echo diskpart not available')
    else:
        out = _run('fdisk -l 2>/dev/null | head -30')
    print(f"{Y}{out[:1000]}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def recover_files():
    print(f"\n{G}[+] Recover Deleted Files{RS}")
    
    print(f"\n{W}Recovery Methods:{RS}")
    print(f"  {W}1.{RS} Windows: Recuva, TestDisk, PhotoRec")
    print(f"  {W}2.{RS} Linux: testdisk, photorec, foremost, scalpel")
    print(f"  {W}3.{RS} macOS: Disk Drill, Data Rescue")
    
    method = input(f"\n{Y}  Choice: {RS}").strip()
    drive = input(f"  {W}[?] Drive/partition to scan: {RS}").strip()
    
    if method == '2' and drive:
        print(f"{G}[+] Running photorec on {drive}...{RS}")
        os.system(f'photorec {drive} 2>/dev/null')
    elif method == '1':
        print(f"{Y}[!] Use Recuva or TestDisk for Windows recovery{RS}")
    elif method == '3':
        print(f"{Y}[!] Use Disk Drill for macOS recovery{RS}")
    
    print(f"\n{W}Quick check for recoverable files using foremost:{RS}")
    if drive:
        os.system(f'foremost -i {drive} -o recovered_files 2>/dev/null')
    
    print(f"\n{Y}[!] Deleted files are recoverable until overwritten{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def memory_analysis():
    print(f"\n{G}[+] Memory Dump Analysis{RS}")
    
    print(f"\n{W}Memory Acquisition Tools:{RS}")
    print(f"  1. Windows: WinPmem, FTK Imager, DumpIt")
    print(f"  2. Linux: LiME, avml, fmem")
    print(f"  3. macOS: Mac Memory Reader, osxpmem")
    
    print(f"\n{W}Memory Analysis Tools:{RS}")
    print(f"  • Volatility 3: volatility -f memory.dump windows.info")
    print(f"  • Rekall: rekall -f memory.dump")
    print(f"  • Redline (FireEye)")
    
    method = input(f"\n{Y}  Choice: {RS}").strip()
    
    if method == '1':
        outfile = input(f"  {W}[?] Output file: {RS}").strip() or 'memory.dump'
        print(f"{G}[+] Acquiring memory to {outfile}...{RS}")
        os.system(f'winpmem.exe {outfile} 2>/dev/null')
    elif method == '2':
        outfile = input(f"  {W}[?] Output file: {RS}").strip() or 'memory.dump'
        print(f"{G}[+] Loading LiME kernel module...{RS}")
        print(f"  insmod lime.ko path={outfile} format=lime")
    
    # Analyze with volatility if dump exists
    if os.path.exists('memory.dump') or os.path.exists(('memory.dump')):
        print(f"\n{G}[+] Analyzing memory dump...{RS}")
        try:
            import volatility3
            print(f"  {Y}[!] Run: volatility -f memory.dump windows.cmdline{RS}")
        except:
            print(f"  {Y}[!] Install volatility3: pip install volatility3{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def log_wiping():
    print(f"\n{G}[+] Log Wiping Tools{RS}")
    
    print(f"\n{W}Windows Logs:{RS}")
    print(f"  {W}•{RS} Clear event logs: wevtutil el | ForEach-Object { wevtutil cl $_ }")
    print(f"  {W}•{RS} wevtutil cl Application")
    print(f"  {W}•{RS} wevtutil cl System")
    print(f"  {W}•{RS} wevtutil cl Security")
    print(f"  {W}•{RS} del C:\\Windows\\System32\\winevt\\Logs\\*.evtx")
    
    print(f"\n{W}Linux Logs:{RS}")
    print(f"  {W}•{RS} Clear syslog: > /var/log/syslog")
    print(f"  {W}•{RS} Clear auth log: > /var/log/auth.log")
    print(f"  {W}•{RS} Clear kern log: > /var/log/kern.log")
    print(f"  {W}•{RS} Clear bash history: history -c && > ~/.bash_history")
    print(f"  {W}•{RS} Remove journalctl: journalctl --rotate && journalctl --vacuum-time=1s")
    print(f"  {W}•{RS} Wipe all: find /var/log -type f -exec cp /dev/null {} \\;")
    
    print(f"\n{W}Application Logs:{RS}")
    print(f"  {W}•{RS} Wipe browser history/clean")
    print(f"  {W}•{RS} Clear recent files")
    print(f"  {W}•{RS} Clear clipboard history")
    print(f"  {W}•{RS} Wipe temp directories")
    
    inp = input(f"\n{Y}[?] Execute log wipe? (y/n): {RS}").strip().lower()
    if inp == 'y':
        if os.name == 'nt':
            os.system('wevtutil cl Application 2>&1')
            os.system('wevtutil cl System 2>&1')
            os.system('wevtutil cl Security 2>&1')
            print(f"{G}[+] Windows event logs cleared{RS}")
        else:
            os.system('> /var/log/syslog 2>/dev/null')
            os.system('> /var/log/auth.log 2>/dev/null')
            os.system('history -c 2>/dev/null')
            print(f"{G}[+] Linux logs cleared{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def file_shredder():
    print(f"\n{G}[+] File Shredder (Secure Delete){RS}")
    file_path = input(f"  {W}[?] File/directory to shred: {RS}").strip()
    
    if not os.path.exists(file_path):
        print(f"{R}[-] Path not found{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    passes = int(input(f"  {W}[?] Number of overwrite passes (default: 3): {RS}").strip() or '3')
    
    print(f"\n{R}[!] SECURELY DELETING: {file_path}{RS}")
    print(f"{R}[!] This is IRREVERSIBLE!{RS}")
    confirm = input(f"\n{Y}[?] Type 'shred' to confirm: {RS}").strip()
    
    if confirm == 'shred':
        print(f"{G}[+] Shredding with {passes} passes...{RS}")
        
        if os.path.isdir(file_path):
            # Use shred for each file
            for root, dirs, files in os.walk(file_path):
                for f in files:
                    fpath = os.path.join(root, f)
                    print(f"  {C}Shredding:{RS} {fpath}")
                    if os.name == 'nt':
                        # Overwrite with random data
                        size = os.path.getsize(fpath)
                        with open(fpath, 'wb') as fp:
                            for _ in range(passes):
                                fp.seek(0)
                                fp.write(os.urandom(size))
                        os.remove(fpath)
                    else:
                        os.system(f'shred -n {passes} -z -u {fpath} 2>/dev/null')
            os.rmdir(file_path) if os.name != 'nt' else os.system(f'rmdir /s /q {file_path}')
        else:
            if os.name == 'nt':
                size = os.path.getsize(file_path)
                with open(file_path, 'wb') as fp:
                    for _ in range(passes):
                        fp.seek(0)
                        fp.write(os.urandom(size))
                os.remove(file_path)
            else:
                os.system(f'shred -n {passes} -z -u {file_path} 2>/dev/null')
        
        print(f"{G}[+] {file_path} securely deleted{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def timestamp_manip():
    print(f"\n{G}[+] Timestamp Manipulation{RS}")
    file_path = input(f"  {W}[?] File to modify: {RS}").strip()
    
    if not os.path.exists(file_path):
        print(f"{R}[-] File not found{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    print(f"\n{W}Current timestamps:{RS}")
    stat = os.stat(file_path)
    def ts2str(ts):
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print(f"  {C}Created:{RS} {ts2str(stat.st_ctime)}")
    print(f"  {C}Modified:{RS} {ts2str(stat.st_mtime)}")
    print(f"  {C}Accessed:{RS} {ts2str(stat.st_atime)}")
    
    new_time = input(f"\n  {W}[?] New timestamp (YYYY-MM-DD HH:MM:SS): {RS}").strip()
    if new_time:
        try:
            dt = datetime.strptime(new_time, '%Y-%m-%d %H:%M:%S')
            new_ts = dt.timestamp()
            
            if os.name == 'nt':
                import pywin32_setctime
                os.utime(file_path, (new_ts, new_ts))
                try:
                    from win32_setctime import setctime
                    setctime(file_path, new_ts)
                except: pass
            else:
                os.utime(file_path, (new_ts, new_ts))
                # Also set birth time on Linux (requires debugfs)
                print(f"{Y}[!] Set access/modify time. Birth time requires debugfs.{RS}")
            
            print(f"{G}[+] Timestamps changed to {new_time}{RS}")
        except Exception as e:
            print(f"{R}[-] Error: {e}{RS}")
    else:
        print(f"{Y}[-] No timestamp provided{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def browser_forensics():
    print(f"\n{G}[+] Browser Forensics{RS}")
    
    import sqlite3, shutil
    home = os.path.expanduser('~')
    
    print(f"\n{W}Browser Data Extraction:{RS}")
    
    # Chrome history
    chrome_paths = [
        os.path.join(home, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History'),
        os.path.join(home, '.config', 'google-chrome', 'Default', 'History'),
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"\n  {C}Chrome History:{RS}")
            try:
                shutil.copy2(path, 'chrome_history.db')
                conn = sqlite3.connect('chrome_history.db')
                cursor = conn.cursor()
                cursor.execute('SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 10')
                for row in cursor.fetchall():
                    # Convert Chrome time to timestamp
                    chrome_time = row[2] / 1000000 - 11644473600
                    dt = datetime.fromtimestamp(chrome_time) if chrome_time > 0 else 'Unknown'
                    print(f"  {G}[+]{RS} [{dt}] {Y}{row[0][:60]}{RS}")
                conn.close()
            except Exception as e:
                print(f"  {Y}[-] Error: {e}{RS}")
    
    # Firefox
    firefox_profiles = os.path.join(home, 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles')
    if os.path.exists(firefox_profiles):
        for profile in os.listdir(firefox_profiles):
            places = os.path.join(firefox_profiles, profile, 'places.sqlite')
            if os.path.exists(places):
                print(f"\n  {C}Firefox History:{RS}")
                try:
                    shutil.copy2(places, 'ff_history.db')
                    conn = sqlite3.connect('ff_history.db')
                    cursor = conn.cursor()
                    cursor.execute('SELECT url, title, last_visit_date FROM moz_places ORDER BY last_visit_date DESC LIMIT 10')
                    for row in cursor.fetchall():
                        print(f"  {G}[+]{RS} {Y}{row[0][:60]}{RS}")
                    conn.close()
                except Exception as e:
                    print(f"  {Y}[-] Error: {e}{RS}")
    
    print(f"\n{W}Browser artifacts (check manually):{RS}")
    print(f"  {W}•{RS} Bookmarks")
    print(f"  {W}•{RS} Cookies (cookies.sqlite / Cookies file)")
    print(f"  {W}•{RS} Saved passwords (Login Data)")
    print(f"  {W}•{RS} Cache / Downloads")
    print(f"  {W}•{RS} Form history (Web Data)")
    print(f"  {W}•{RS} Session restore files")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def network_forensics():
    print(f"\n{G}[+] Network Forensics (PCAP Analysis){RS}")
    pcap = input(f"  {W}[?] PCAP file path: {RS}").strip()
    
    if pcap and os.path.exists(pcap):
        print(f"\n{W}Analyzing {pcap}...{RS}")
        
        # Basic analysis with tshark
        out = _run(f'tshark -r {pcap} -q -z io,stat,1 2>/dev/null | head -20')
        if out:
            print(f"{Y}{out}{RS}")
        else:
            print(f"{Y}[-] tshark not available{RS}")
        
        # Extract HTTP objects
        print(f"\n{W}HTTP Objects:{RS}")
        out = _run(f'tshark -r {pcap} -Y http.request -T fields -e http.host -e http.request.uri 2>/dev/null | head -20')
        print(f"{Y}{out or 'No HTTP requests found'}{RS}")
        
        # Extract DNS queries
        print(f"\n{W}DNS Queries:{RS}")
        out = _run(f'tshark -r {pcap} -Y dns -T fields -e dns.qry.name 2>/dev/null | sort -u | head -20')
        print(f"{Y}{out or 'No DNS queries found'}{RS}")
        
        # Extract IPs
        print(f"\n{W}IP Conversations:{RS}")
        out = _run(f'tshark -r {pcap} -q -z conv,ip 2>/dev/null | head -20')
        print(f"{Y}{out}{RS}")
    
    print(f"\n{W}Network Forensic Tools:{RS}")
    print(f"  {W}•{RS} Wireshark / TShark")
    print(f"  {W}•{RS} NetworkMiner")
    print(f"  {W}•{RS} Xplico")
    print(f"  {W}•{RS} Zeek (Bro)")
    print(f"  {W}•{RS} CapLoader")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def registry_forensics():
    print(f"\n{G}[+] Windows Registry Forensics{RS}")
    print(f"{Y}[!] Windows only feature{RS}")
    
    if os.name != 'nt':
        print(f"{R}[-] Not a Windows system{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    print(f"\n{W}Registry Analysis:{RS}")
    
    # Startup programs
    print(f"\n  {C}Startup Programs (Run key):{RS}")
    out = _run('reg query "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"')
    print(f"  {Y}{out[:500]}{RS}")
    
    # Recent files
    print(f"\n  {C}Recent Documents:{RS}")
    out = _run('reg query "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs"')
    print(f"  {Y}{out[:500]}{RS}")
    
    # USB devices
    print(f"\n  {C}USB Device History:{RS}")
    out = _run('reg query "HKLM\\SYSTEM\\CurrentControlSet\\Enum\\USBSTOR"')
    print(f"  {Y}{out[:500]}{RS}")
    
    # Network interfaces
    print(f"\n  {C}Network History:{RS}")
    out = _run('reg query "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkList\\Profiles"')
    print(f"  {Y}{out[:500]}{RS}")
    
    # Browser history from registry
    print(f"\n  {C}Typed URLs:{RS}")
    out = _run('reg query "HKCU\\Software\\Microsoft\\Internet Explorer\\TypedURLs"')
    print(f"  {Y}{out[:500]}{RS}")
    
    print(f"\n{W}Registry Forensic Tools:{RS}")
    print(f"  {W}•{RS} RegRipper")
    print(f"  {W}•{RS} Registry Explorer")
    print(f"  {W}•{RS} RECmd (Zimmerman's tools)")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def anti_forensic_hide():
    print(f"\n{G}[+] Anti-Forensic Data Hiding{RS}")
    
    print(f"\n{W}Data Hiding Techniques:{RS}")
    print(f"  {W}1.{RS} Alternate Data Streams (NTFS) - Windows")
    print(f"  {W}2.{RS} Hidden partitions / unallocated space")
    print(f"  {W}3.{RS} Encrypted containers (VeraCrypt)")
    print(f"  {W}4.{RS} Steganography (hide in images/audio)")
    print(f"  {W}5.{RS} File extension spoofing")
    print(f"  {W}6.{RS} Dead space hiding (slack space)")
    print(f"  {W}7.{RS} Registry hiding")
    print(f"  {W}8.{RS} Process hiding (rootkit techniques)")
    
    method = input(f"\n{Y}  Choice: {RS}").strip()
    
    if method == '1' and os.name == 'nt':
        file_path = input(f"  {W}[?] File to hide: {RS}").strip()
        carrier = input(f"  {W}[?] Carrier file: {RS}").strip()
        if file_path and carrier:
            os.system(f'type {file_path} > {carrier}:hidden.txt')
            print(f"{G}[+] Data hidden in ADS of {carrier}{RS}")
            print(f"{W}Access: notepad {carrier}:hidden.txt{RS}")
            print(f"{W}Detect: dir /r {carrier}{RS}")
    
    elif method == '3':
        print(f"\n{W}Creating encrypted container with VeraCrypt:{RS}")
        print(f"  1. Install VeraCrypt")
        print(f"  2. Create a new volume")
        print(f"  3. Choose standard VeraCrypt volume")
        print(f"  4. Select encryption algorithm (AES)")
        print(f"  5. Set volume size and password")
        print(f"  6. Format and mount")
    
    elif method == '4':
        print(f"\n{W}Use steganography module (option 16 in main menu){RS}")
    
    elif method == '5':
        print(f"\n{W}File Extension Spoofing:{RS}")
        print(f"  Rename: malware.exe → malware.jpg (still executable)")
        print(f"  Double extension: document.pdf.exe")
        print(f"  RTL override: using Unicode RTL character")
        print(f"  Space padding: 'file.txt .exe'")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
