#!/usr/bin/env python3
"""
A2Tool v4.0 - Vulnerability Scanner Module (10 Tools)
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time, socket
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
        print(f"\n{R}╔══════════════════════════════════════════════════════════════╗{RS}")
        print(f"{R}║{W}            System Info & Vulnerability Scanner             {R}║{RS}")
        print(f"{R}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{R}║{W} [01]{R}  System Information Dump                            {R}║{RS}")
        print(f"{R}║{W} [02]{R}  Running Services & Ports                           {R}║{RS}")
        print(f"{R}║{W} [03]{R}  Installed Software Audit                           {R}║{RS}")
        print(f"{R}║{W} [04]{R}  CVE Database Lookup                                {R}║{RS}")
        print(f"{R}║{W} [05]{R}  Open Port Vulnerability Scanner                    {R}║{RS}")
        print(f"{R}║{W} [06]{R}  SUID / SGID / Sticky Bit Check                    {R}║{RS}")
        print(f"{R}║{W} [07]{R}  Web Vulnerability Scanner (Nikto)                  {R}║{RS}")
        print(f"{R}║{W} [08]{R}  Network Vulnerability Scanner (NSE)                {R}║{RS}")
        print(f"{R}║{W} [09]{R}  Malware Scanner (YARA Rules)                       {R}║{RS}")
        print(f"{R}║{W} [10]{R}  Full Security Audit & Report                      {R}║{RS}")
        print(f"{R}║{W} [0]{R}   Back to Main Menu                                  {R}║{RS}")
        print(f"{R}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[Vuln] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': sys_info()
        elif ch == '2': running_services()
        elif ch == '3': software_audit()
        elif ch == '4': cve_lookup()
        elif ch == '5': port_vuln_scan()
        elif ch == '6': suid_check()
        elif ch == '7': web_vuln_scan()
        elif ch == '8': network_vuln_nse()
        elif ch == '9': malware_scan()
        elif ch == '10': full_audit_report()
        else: print(f"{R}[!] Invalid option{RS}")

def sys_info():
    print(f"\n{G}[+] System Information Dump{RS}")
    
    print(f"\n  {W}Basic Info:{RS}")
    print(f"  {C}OS:{RS} {platform.system()} {platform.release()} {platform.version()}")
    print(f"  {C}Arch:{RS} {platform.machine()}")
    print(f"  {C}Processor:{RS} {platform.processor()}")
    print(f"  {C}Hostname:{RS} {platform.node()}")
    print(f"  {C}Python:{RS} {sys.version}")
    
    # User info
    print(f"\n  {W}User Info:{RS}")
    if os.name == 'nt':
        out = _run('whoami')
        print(f"  {C}User:{RS} {out.strip()}")
        out = _run('net user %username% | findstr /C:"Account active"')
        print(f"  {C}Status:{RS} {out.strip()[:50]}")
    else:
        out = _run('id; whoami')
        print(f"  {C}User:{RS} {out[:100]}")
    
    # Environment
    print(f"\n  {W}Notable Environment Vars:{RS}")
    for var in ['PATH', 'HOME', 'USER', 'TEMP', 'SHELL', 'PWD']:
        val = os.environ.get(var, 'N/A')
        print(f"  {C}{var}:{RS} {val[:80]}")
    
    # Disk usage
    print(f"\n  {W}Disk Usage:{RS}")
    if os.name == 'nt':
        out = _run('wmic logicaldisk get caption,freespace,size')
    else:
        out = _run('df -h / 2>/dev/null')
    print(f"  {Y}{out[:300]}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def running_services():
    print(f"\n{G}[+] Running Services & Open Ports{RS}")
    
    if os.name == 'nt':
        print(f"\n  {W}Services:{RS}")
        out = _run('net start | head -40')
        print(f"  {Y}{out[:1500]}{RS}")
        
        print(f"\n  {W}Listening Ports:{RS}")
        out = _run('netstat -ano | findstr LISTEN | head -30')
        print(f"  {Y}{out[:1500]}{RS}")
    else:
        print(f"\n  {W}Services:{RS}")
        out = _run('systemctl list-units --type=service --state=running 2>/dev/null | head -30')
        print(f"  {Y}{out or 'systemctl not available'}{RS}")
        
        print(f"\n  {W}Listening Ports:{RS}")
        out = _run('ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null')
        print(f"  {Y}{out[:1500]}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def software_audit():
    print(f"\n{G}[+] Installed Software Audit{RS}")
    
    if os.name == 'nt':
        print(f"\n  {W}Installed Programs:{RS}")
        out = _run('wmic product get name,version,vendor | head -50')
        print(f"  {Y}{out[:2000]}{RS}")
    else:
        print(f"\n  {W}Installed Packages:{RS}")
        pkg_managers = [
            'dpkg -l 2>/dev/null | head -50',
            'rpm -qa 2>/dev/null | head -50',
            'pacman -Q 2>/dev/null | head -50'
        ]
        for cmd in pkg_managers:
            out = _run(cmd)
            if out:
                print(f"  {Y}{out[:1500]}{RS}")
                break
    
    # Check for outdated/vulnerable software
    print(f"\n  {W}Security Software Check:{RS}")
    sec_software = ['antivirus', 'firewall', 'ids', 'ips', 'selinux', 'apparmor']
    for sw in sec_software:
        out = _run(f'which {sw} 2>/dev/null || where {sw} 2>/dev/null')
        if out:
            print(f"  {G}[✓]{RS} {sw} - {out.strip()[:40]}")
        else:
            print(f"  {R}[✗]{RS} {sw} - Not installed")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def cve_lookup():
    print(f"\n{G}[+] CVE Database Lookup{RS}")
    query = input(f"  {W}[?] Search (software name, CVE ID, keyword): {RS}").strip()
    
    if not query:
        print(f"{Y}[-] No query provided{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    print(f"\n{W}Searching for CVEs related to: '{query}'{RS}")
    
    # Online CVE search
    print(f"\n  {W}CVE Links:{RS}")
    print(f"  {C}[+]{RS} https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={query}")
    print(f"  {C}[+]{RS} https://nvd.nist.gov/vuln/search?query={query}")
    print(f"  {C}[+]{RS} https://cvedetails.com/google-search-results.php?q={query}")
    print(f"  {C}[+]{RS} https://sploitus.com/?query={query}")
    print(f"  {C}[+]{RS} https://exploit-db.com/search?q={query}")
    
    # Try local searchsploit
    out = _run(f'searchsploit {query} 2>/dev/null')
    if out:
        print(f"\n  {W}Local Exploit-DB Results:{RS}")
        print(f"  {Y}{out[:1000]}{RS}")
    
    # Check for known software vulnerabilities
    known_vulns = {
        'openssh': 'CVE-2024-6387 (regreSSHion) - RCE in OpenSSH server',
        'apache': 'CVE-2021-41773 (Path Traversal), CVE-2021-42013',
        'nginx': 'CVE-2021-23017 (DNS resolver), CVE-2021-3618',
        'mysql': 'CVE-2023-21971, CVE-2022-21367',
        'php': 'CVE-2024-4577 (Windows CGI RCE), CVE-2023-3824',
        'wordpress': 'CVE-2023-4512, Multiple plugin vulnerabilities',
        'windows': 'MS17-010 (EternalBlue), CVE-2021-1675 (PrintNightmare)',
        'samba': 'CVE-2021-44142 (Samba vfs_fruit), CVE-2020-1472',
        'docker': 'CVE-2024-21626 (runc), CVE-2019-5736',
        'kubernetes': 'CVE-2023-3676, CVE-2023-3235',
    }
    
    for soft, cve in known_vulns.items():
        if soft.lower() in query.lower():
            print(f"\n  {R}[!] Known vulnerability:{RS} {Y}{cve}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def port_vuln_scan():
    print(f"\n{G}[+] Open Port Vulnerability Scanner{RS}")
    target = input(f"  {W}[?] Target IP: {RS}").strip()
    
    if not target:
        print(f"{Y}[-] No target{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    print(f"{G}[+] Scanning {target} for open ports and known vulnerabilities...{RS}")
    
    # Quick port scan
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
            open_ports.append((port, svc))
        s.close()
    
    if open_ports:
        print(f"\n  {W}Open Ports & Vulnerability Assessment:{RS}")
        port_vulns = {
            21: ('FTP', 'Anonymous login, weak credentials, vsFTPd 2.3.4 backdoor'),
            22: ('SSH', 'Brute force, CVE-2024-6387 (regreSSHion), weak ciphers'),
            23: ('Telnet', 'Unencrypted traffic, credential sniffing'),
            25: ('SMTP', 'Open relay, user enumeration, spoofing'),
            80: ('HTTP', 'Web attacks, directory busting, SQL injection'),
            110: ('POP3', 'Unencrypted login, credential theft'),
            143: ('IMAP', 'Unencrypted login, credential theft'),
            443: ('HTTPS', 'Check SSL/TLS vulnerabilities, Heartbleed'),
            445: ('SMB', 'EternalBlue, SMBGhost, relay attacks'),
            3306: ('MySQL', 'Default credentials, SQL injection, local file read'),
            3389: ('RDP', 'BlueKeep, RDP man-in-middle, credential brute force'),
            5900: ('VNC', 'No auth, weak auth, known CVEs'),
            8080: ('HTTP-Proxy', 'Web attacks, directory busting'),
            27017: ('MongoDB', 'No auth by default, data exposure'),
        }
        
        for port, svc in open_ports:
            vuln_info = port_vulns.get(port, ('Unknown', 'Check manually'))
            print(f"\n  {R}[OPEN]{RS} Port {C}{port:>5}{RS} ({Y}{svc}{RS})")
            print(f"       {W}Vulnerabilities:{RS} {vuln_info[1]}")
    else:
        print(f"\n  {G}[+] No common ports open{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def suid_check():
    print(f"\n{G}[+] SUID / SGID / Sticky Bit Check{RS}")
    
    if os.name == 'nt':
        print(f"{Y}[!] SUID/SGID is a Linux concept{RS}")
        print(f"\n{W}Windows equivalent checks:{RS}")
        out = _run('whoami /priv')
        print(f"  {Y}{out[:1000]}{RS}")
        print(f"\n{W}Run with high integrity:{RS}")
        out2 = _run('whoami /groups')
        print(f"  {Y}{out2[:500]}{RS}")
    else:
        print(f"\n  {W}SUID Binaries (potential privilege escalation):{RS}")
        out = _run('find / -perm -4000 -type f 2>/dev/null | head -30')
        if out:
            for line in out.split('\n'):
                if line.strip():
                    print(f"  {R}[SUID]{RS} {Y}{line}{RS}")
        else:
            print(f"  {G}[+] No SUID binaries found{RS}")
        
        print(f"\n  {W}SGID Binaries:{RS}")
        out = _run('find / -perm -2000 -type f 2>/dev/null | head -20')
        if out:
            for line in out.split('\n'):
                if line.strip():
                    print(f"  {Y}[SGID]{RS} {line}")
        else:
            print(f"  {G}[+] No SGID binaries found{RS}")
        
        print(f"\n  {W}World-Writable Directories:{RS}")
        out = _run('find / -perm -777 -type d 2>/dev/null | head -10')
        if out:
            for line in out.split('\n'):
                if line.strip():
                    print(f"  {Y}[WW]{RS} {line}")
        
        # Check for known SUID exploits
        suid_exploits = {
            'nmap': 'nmap --interactive',
            'vim': 'vim -c "!sh"',
            'less': 'less /etc/passwd; !sh',
            'more': 'more /etc/passwd; !sh',
            'find': 'find . -exec /bin/sh -p \\; -quit',
            'python': 'python -c "import os;os.execl(\'/bin/sh\',\'sh\',\'-p\')"',
            'perl': 'perl -e "exec \'/bin/sh\';"',
            'awk': 'awk \'BEGIN {system("/bin/sh")}\'',
        }
        
        print(f"\n  {W}Escalation Methods for Common SUID Binaries:{RS}")
        for binary, exploit in suid_exploits.items():
            print(f"  {C}{binary:<10}{RS} {Y}{exploit}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def web_vuln_scan():
    print(f"\n{G}[+] Web Vulnerability Scanner (Nikto wrapper){RS}")
    target = input(f"  {W}[?] Target URL: {RS}").strip()
    
    if not target:
        print(f"{Y}[-] No target{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    print(f"\n{W}Checking web server...{RS}")
    try:
        import requests
        r = requests.get(target, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        print(f"  {C}Status:{RS} {r.status_code}")
        print(f"  {C}Server:{RS} {r.headers.get('Server', 'Unknown')}")
        print(f"  {C}Content-Type:{RS} {r.headers.get('Content-Type', 'N/A')}")
        print(f"  {C}Content-Length:{RS} {len(r.content):,} bytes")
        
        # Check security headers
        sec_headers = {
            'X-Frame-Options': 'Clickjacking protection',
            'X-Content-Type-Options': 'MIME-sniffing protection',
            'X-XSS-Protection': 'XSS protection',
            'Strict-Transport-Security': 'HSTS',
            'Content-Security-Policy': 'CSP',
        }
        
        missing = []
        for header, desc in sec_headers.items():
            if header in r.headers:
                print(f"  {G}[✓]{RS} {header} ({desc})")
            else:
                missing.append(header)
        
        if missing:
            print(f"\n  {R}[!] Missing Security Headers:{RS}")
            for h in missing:
                print(f"  {R}[-]{RS} {h}")
    
    except Exception as e:
        print(f"{R}[-] Connection failed: {e}{RS}")
    
    # Run nikto if available
    print(f"\n{W}Running Nikto (if installed):{RS}")
    out = _run(f'nikto -h {target} 2>/dev/null')
    if out:
        print(f"{Y}{out[:1500]}{RS}")
    else:
        print(f"{Y}[!] Nikto not installed. Install: apt install nikto{RS}")
        print(f"{Y}[!] Or visit: https://github.com/sullo/nikto{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def network_vuln_nse():
    print(f"\n{G}[+] Network Vulnerability Scanner (NMAP NSE){RS}")
    target = input(f"  {W}[?] Target IP/Domain: {RS}").strip()
    
    if not target:
        print(f"{Y}[-] No target{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    print(f"\n{W}Available NSE Vulnerability Scans:{RS}")
    print(f"  1. Basic vuln scan: nmap -sV --script vuln {target}")
    print(f"  2. SMB vulns: nmap -p445 --script smb-vuln* {target}")
    print(f"  3. Web vulns: nmap -p80,443 --script http-vuln* {target}")
    print(f"  4. All vulns: nmap -sV --script "vuln and safe" {target}")
    print(f"  5. Brute force: nmap --script brute {target}")
    print(f"  6. Default + vuln: nmap -sC -sV --script vuln {target}")
    
    ch = input(f"\n{Y}  Choice: {RS}").strip()
    
    cmd_map = {
        '1': f'nmap -sV --script vuln {target}',
        '2': f'nmap -p445 --script smb-vuln* {target}',
        '3': f'nmap -p80,443 --script http-vuln* {target}',
        '4': f'nmap -sV --script "vuln and safe" {target}',
        '5': f'nmap --script brute {target}',
        '6': f'nmap -sC -sV --script vuln {target}',
    }
    
    cmd = cmd_map.get(ch, cmd_map['1'])
    print(f"\n{G}[+] Running: {cmd}{RS}")
    print(f"{Y}[!] This may take several minutes...{RS}")
    
    run_now = input(f"{Y}[?] Run now? (y/n): {RS}").strip().lower()
    if run_now == 'y':
        os.system(cmd)
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def malware_scan():
    print(f"\n{G}[+] Malware Scanner (YARA Rules){RS}")
    target_dir = input(f"  {W}[?] Directory to scan: {RS}").strip() or '.'
    
    if not os.path.exists(target_dir):
        print(f"{R}[-] Directory not found{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    # Simple heuristic scan
    print(f"\n{W}Performing heuristic malware scan on {target_dir}...{RS}")
    
    suspicious_patterns = [
        (b'eval(base64_decode', 'PHP base64 eval'),
        (b'system($_GET', 'PHP webshell'),
        (b'CreateObject("Wscript.Shell")', 'VBS/JS backdoor'),
        (b'powershell -ExecutionPolicy Bypass', 'PowerShell threat'),
        (b'SendStringToPipe', 'Keylogger indicator'),
        (b'REG_SZ /v', 'Registry persistence'),
        (b'HTTP/1.1", "POST', 'Data exfiltration'),
        (b'CreateRemoteThread', 'Process injection'),
        (b'shellcode', 'Shellcode payload'),
        (b'meterpreter', 'Metasploit payload'),
    ]
    
    found_threats = []
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                if os.path.getsize(filepath) > 10 * 1024 * 1024:  # Skip large files
                    continue
                
                with open(filepath, 'rb') as f:
                    content = f.read()
                
                for pattern, desc in suspicious_patterns:
                    if pattern in content:
                        found_threats.append((filepath, desc))
                        print(f"  {R}[!]{RS} {filepath}")
                        print(f"      {Y}{desc}{RS}")
            except:
                pass
    
    if not found_threats:
        print(f"  {G}[+] No suspicious patterns found{RS}")
    else:
        print(f"\n{R}[!] Found {len(found_threats)} potential threats{RS}")
    
    # YARA check
    print(f"\n{W}YARA Rule Check:{RS}")
    out = _run('which yara 2>/dev/null')
    if out:
        print(f"  {G}[+] YARA installed{RS}")
        rules_file = input(f"  {W}[?] YARA rules file: {RS}").strip()
        if rules_file and os.path.exists(rules_file):
            os.system(f'yara {rules_file} {target_dir}')
    else:
        print(f"  {Y}[-] YARA not installed (apt install yara){RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def full_audit_report():
    print(f"\n{G}[+] Full Security Audit & Report{RS}")
    target = input(f"  {W}[?] Target IP/Domain (or 'local' for local system): {RS}").strip() or 'local'
    
    print(f"{W}Generating comprehensive security audit report...{RS}")
    
    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append(f"  A2Tool v4.0 - Security Audit Report")
    report_lines.append(f"  Target: {target}")
    report_lines.append(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("=" * 70)
    
    if target == 'local':
        # System info
        report_lines.append(f"\n[1] System Information")
        report_lines.append(f"  OS: {platform.system()} {platform.release()}")
        report_lines.append(f"  Hostname: {platform.node()}")
        report_lines.append(f"  User: {os.environ.get('USER', os.environ.get('USERNAME', 'Unknown'))}")
        
        # Open ports
        report_lines.append(f"\n[2] Open Ports (local)")
        common_ports = [21,22,23,25,53,80,110,143,443,445,993,995,3306,3389,5900,8080]
        open_ports = []
        for port in common_ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex(('127.0.0.1', port)) == 0:
                try:
                    svc = socket.getservbyport(port)
                except:
                    svc = 'unknown'
                open_ports.append(f"{port}/{svc}")
            s.close()
        report_lines.append(f"  Open ports: {', '.join(open_ports) if open_ports else 'None detected'}")
    
    else:
        # Target scan
        report_lines.append(f"\n[1] Target Information")
        try:
            ip = socket.gethostbyname(target)
            report_lines.append(f"  Resolved IP: {ip}")
        except:
            report_lines.append(f"  Resolved IP: Failed to resolve")
        
        # Quick port scan
        report_lines.append(f"\n[2] Open Ports Scan")
        common_ports = [21,22,23,25,53,80,110,143,443,445,993,995,3306,3389,5900,8080]
        open_ports = []
        for port in common_ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            if s.connect_ex((target, port)) == 0:
                try:
                    svc = socket.getservbyport(port)
                except:
                    svc = 'unknown'
                open_ports.append(f"{port}/{svc}")
            s.close()
        report_lines.append(f"  Open ports: {', '.join(open_ports) if open_ports else 'None detected'}")
    
    report_lines.append(f"\n[3] Security Recommendations")
    report_lines.append(f"  • Keep all software updated")
    report_lines.append(f"  • Use strong, unique passwords")
    report_lines.append(f"  • Enable firewall and restrict unnecessary ports")
    report_lines.append(f"  • Use encryption (HTTPS, SSH) for all services")
    report_lines.append(f"  • Implement monitoring and logging")
    report_lines.append(f"  • Regular security audits and penetration testing")
    report_lines.append(f"  • Use multi-factor authentication")
    report_lines.append(f"  • Disable unnecessary services")
    report_lines.append(f"  • Apply security patches promptly")
    
    report_lines.append(f"\n" + "=" * 70)
    report_lines.append(f"  Report generated by A2Tool v4.0")
    report_lines.append(f"  Author: Ayush Rajdev & Anzar Iqbal")
    report_lines.append("=" * 70)
    
    # Print and save
    print('\n'.join(report_lines))
    
    fname = f"security_audit_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(fname, 'w') as f:
        f.write('\n'.join(report_lines))
    print(f"\n{G}[+] Report saved to {fname}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
