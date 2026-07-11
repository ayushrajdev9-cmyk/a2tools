#!/usr/bin/env python3
import os, sys, time, subprocess, platform
from colorama import Fore, Style, init; init(autoreset=True)
R=Fore.RED;G=Fore.GREEN;Y=Fore.YELLOW;B=Fore.BLUE;M=Fore.MAGENTA;C=Fore.CYAN;W=Fore.WHITE;RS=Style.RESET_ALL

def run_external_tool(tool, choice, category):
    print(f"\n{Y}[!] {tool} integration - Option {choice} in {category}{RS}")
    print(f"{Y}[!] Use {tool} directly for full functionality.{RS}")

def system_info_dump(choice):
    if choice=='1':
        print(f"\n{C}[*] System Info:{RS}")
        print(f"  {W}OS: {platform.system()} {platform.release()}{RS}")
        print(f"  {W}Node: {platform.node()}{RS}")
        print(f"  {W}Arch: {platform.machine()}{RS}")
        if os.name=='nt':
            try:
                out=subprocess.check_output('systeminfo | findstr /B /C:"OS Name" /C:"OS Version"',shell=True,timeout=15).decode()
                print(out)
            except: pass
        else:
            try: print(f"  {W}Kernel: {subprocess.check_output(['uname','-a'],timeout=5).decode().strip()}{RS}")
            except: pass
    elif choice=='2':
        print(f"\n{C}[*] Ports/Services:{RS}")
        if os.name=='nt':
            try: print(subprocess.check_output('netstat -an',shell=True,timeout=10).decode()[:2000])
            except: pass
        else:
            try: print(subprocess.check_output(['ss','-tuln'],timeout=10).decode()[:2000])
            except: pass
    elif choice=='5':
        print(f"\n{C}[*] Vulnerability checks:{RS}")
        if os.name!='nt':
            try:
                print(f"{Y}SUID:{RS}")
                subprocess.run('find / -perm -4000 2>/dev/null',shell=True,timeout=10)
            except: pass
        print(f"{G}[+] Done.{RS}")
    else:
        print(f"{Y}[!] Option not implemented.{RS}")
    input(f"\n{Y}[+] Press Enter...{RS}")

def check_dependencies():
    missing=[]
    for tool in ['nmap','hydra','aircrack-ng','sqlmap','hashcat','john','msfconsole','ngrok']:
        try:
            subprocess.run(['where',tool] if os.name=='nt' else ['which',tool],capture_output=True,timeout=3)
        except:
            missing.append(tool)
    if missing:
        print(f"{Y}[!] Missing: {', '.join(missing)}{RS}")
    else:
        print(f"{G}[+] All external tools found.{RS}")
