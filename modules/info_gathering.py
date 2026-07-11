#!/usr/bin/env python3
import os, sys, time, json, socket, subprocess, re, urllib.request
from colorama import Fore, Style, init; init(autoreset=True)
R=Fore.RED;G=Fore.GREEN;Y=Fore.YELLOW;B=Fore.BLUE;M=Fore.MAGENTA;C=Fore.CYAN;W=Fore.WHITE;RS=Style.RESET_ALL
IS_WINDOWS=os.name=='nt'

def whois_lookup():
    d=input(Y+"  Domain/IP: "+RS).strip()
    if not d: return
    try:
        data=urllib.request.urlopen(f'https://www.whois.com/whois/{d}').read().decode()
        for line in data.split("\n"):
            if any(x in line.lower() for x in ['domain name','registrar','creation date','expiry','name server','registrant']):
                print("  "+C+line.strip()+RS)
    except: print(R+"[!] Failed"+RS)

def dns_enum():
    d=input(Y+"  Domain: "+RS).strip()
    if not d: return
    print(f"\n{C}[*] DNS for {d}:"+RS)
    try:
        ip=socket.gethostbyname(d)
        print(f"  {G}[+] A: {W}{ip}{RS}")
    except: print(R+"[!] DNS failed"+RS)

def port_scan():
    t=input(Y+"  Target IP: "+RS).strip()
    if not t: return
    p=input(Y+"  Ports (1-1000): "+RS).strip() or "1-1000"
    print(f"\n{C}[*] Scanning {t}..."+RS)
    def scan(p):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.settimeout(0.5)
        try:
            if s.connect_ex((t,int(p)))==0: print(f"  {G}[+] Port {p}: OPEN"+RS)
        except: pass
        finally: s.close()
    if '-' in p:
        import threading
        start,end=map(int,p.split('-'))
        threads=[]
        for pn in range(start,min(end+1,65536)):
            th=threading.Thread(target=scan,args=(pn,),daemon=True); th.start(); threads.append(th)
            if len(threads)>=200:
                for th in threads: th.join()
                threads=[]
        for th in threads: th.join()
    else:
        for pn in p.split(','): scan(pn.strip())

def subdomain_enum():
    d=input(Y+"  Domain: "+RS).strip()
    if not d: return
    subs=['www','mail','admin','ftp','ssh','api','dev','test','stage','prod','vpn','webmail','blog','wiki','shop','app','secure','login']
    print(f"\n{C}[*] Scanning subdomains..."+RS)
    for sub in subs:
        try:
            ip=socket.gethostbyname(f"{sub}.{d}")
            print(f"  {G}[+] {W}{sub}.{d}{RS} -> {G}{ip}{RS}")
        except: pass

def geoip():
    ip=input(Y+"  IP: "+RS).strip()
    if not ip: return
    try:
        data=json.loads(urllib.request.urlopen(f'http://ip-api.com/json/{ip}').read())
        for k,v in data.items(): print(f"  {C}{k}: {W}{v}{RS}")
    except: print(R+"[!] GeoIP failed"+RS)

def email_harvest():
    d=input(Y+"  Domain: "+RS).strip()
    if not d: return
    try:
        data=urllib.request.urlopen(f'https://www.google.com/search?q=email+%40{d}').read().decode()
        emails=set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.'+d.replace('.',r'\.'),data))
        for e in emails: print(f"  {G}[+] {W}{e}{RS}")
    except: print(R+"[!] Harvest failed"+RS)

def google_dork():
    print(f"\n{Y}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}Google Dork Cheat Sheet{R}                             {Y}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    dorks={'Passwords':'filetype:txt intext:password intext:username','Configs':'filetype:conf inurl:config','Databases':'filetype:sql intext:insert into','Logs':'filetype:log intext:password','Backups':'filetype:bak intext:password','phpMyAdmin':'inurl:phpmyadmin','Cameras':'inurl:"viewerframe?mode="','WordPress':'inurl:wp-config.php intext:DB_PASSWORD'}
    for k,v in dorks.items(): print(f"  {Y}[*]{RS} {W}{k}{RS}: {v}")

def menu():
    while True:
        os.system('cls' if IS_WINDOWS else 'clear')
        print(f"""{B}
  ╔═══════════════════════════════════════════════════════╗
  ║  {W}A2Tool - Information Gathering (OSINT){R}                {B}║
  ╠═══════════════════════════════════════════════════════╣
  ║  {W}[1] {R}WHOIS Lookup                                    {B}║
  ║  {W}[2] {R}DNS Enumeration                                 {B}║
  ║  {W}[3] {R}Port Scanner                                    {B}║
  ║  {W}[4] {R}Subdomain Enumeration                           {B}║
  ║  {W}[5] {R}GeoIP Lookup                                    {B}║
  ║  {W}[6] {R}Email Harvester                                 {B}║
  ║  {W}[7] {R}Google Dorks                                    {B}║
  ║  {W}[8] {R}Social Media Finder                             {B}║
  ║  {W}[9] {R}Certificate Transparency                        {B}║
  ║  {W}[0] {R}Back to Menu                                   {B}║
  ╚═══════════════════════════════════════════════════════╝
{RS}""")
        choice=input(f"{Y}  A2Tool[OSINT] » {RS}").strip()
        if choice=='0': break
        elif choice=='1': whois_lookup()
        elif choice=='2': dns_enum()
        elif choice=='3': port_scan()
        elif choice=='4': subdomain_enum()
        elif choice=='5': geoip()
        elif choice=='6': email_harvest()
        elif choice=='7': google_dork()
        elif choice=='8':
            u=input(Y+"  Username: "+RS).strip()
            if u:
                sites=['https://github.com/{u}','https://twitter.com/{u}','https://instagram.com/{u}','https://linkedin.com/in/{u}','https://facebook.com/{u}','https://reddit.com/user/{u}','https://t.me/{u}']
                for s in sites: print(f"  {C}[*]{RS} {s.replace('{u}',u)}")
        elif choice=='9':
            d=input(Y+"  Domain: "+RS).strip()
            if d:
                try:
                    data=json.loads(urllib.request.urlopen(f'https://crt.sh/?q={d}&output=json').read())
                    for e in data[:20]: print(f"  {G}[+]{RS} {e.get('name_value','')}")
                except: print(R+"[!] Failed"+RS)
        else: print(R"[!] Invalid"+RS); time.sleep(1)

if __name__=='__main__': menu()
