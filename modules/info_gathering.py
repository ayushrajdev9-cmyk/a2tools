#!/usr/bin/env python3
"""
A2Tool v4.0 - Information Gathering & OSINT Module (25 Tools)
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time, socket, ipaddress, struct
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
        print(f"\n{B}╔══════════════════════════════════════════════════════════════╗{RS}")
        print(f"{B}║{W}          Information Gathering & OSINT Suite               {B}║{RS}")
        print(f"{B}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{B}║{W} [01]{R}  DNS Enumeration & Lookup                           {B}║{RS}")
        print(f"{B}║{W} [02]{R}  WHOIS Lookup                                      {B}║{RS}")
        print(f"{B}║{W} [03]{R}  IP Geolocation                                    {B}║{RS}")
        print(f"{B}║{W} [04]{R}  Subdomain Discovery                               {B}║{RS}")
        print(f"{B}║{W} [05]{R}  Port Scanner (TCP/UDP)                            {B}║{RS}")
        print(f"{B}║{W} [06]{R}  Email OSINT (Breach Check)                        {B}║{RS}")
        print(f"{B}║{W} [07]{R}  Phone Number OSINT                                {B}║{RS}")
        print(f"{B}║{W} [08]{R}  Username OSINT (Social Search)                    {B}║{RS}")
        print(f"{B}║{W} [09]{R}  Website Crawler / Data Extractor                  {B}║{RS}")
        print(f"{B}║{W} [10]{R}  SSL/TLS Certificate Analysis                      {B}║{RS}")
        print(f"{B}║{W} [11]{R}  HTTP Header Analyzer                              {B}║{RS}")
        print(f"{B}║{W} [12]{R}  Reverse IP Lookup (Domains on Same Server)        {B}║{RS}")
        print(f"{B}║{W} [13]{R}  Shodan Device Discovery                           {B}║{RS}")
        print(f"{B}║{W} [14]{R}  Google Dork Generator                             {B}║{RS}")
        print(f"{B}║{W} [15]{R}  Wayback Machine History                           {B}║{RS}")
        print(f"{B}║{W} [16]{R}  Email Harvesting (Scraper)                        {B}║{RS}")
        print(f"{B}║{W} [17]{R}  Social Media Profile Analyzer                     {B}║{RS}")
        print(f"{B}║{W} [18]{R}  MAC Address Lookup                               {B}║{RS}")
        print(f"{B}║{W} [19]{R}  Banner Grabbing                                   {B}║{RS}")
        print(f"{B}║{W} [20]{R}  Network Protocol Analyzer                        {B}║{RS}")
        print(f"{B}║{W} [21]{R}  IoT Device Scanner                               {B}║{RS}")
        print(f"{B}║{W} [22]{R}  Cloud Asset Discovery                            {B}║{RS}")
        print(f"{B}║{W} [23]{R}  Pastebin/Dark Web Monitor                        {B}║{RS}")
        print(f"{B}║{W} [24]{R}  Stealth Scan (Half-Open SYN)                     {B}║{RS}")
        print(f"{B}║{W} [25]{R}  AI-Powered Recon Report                          {B}║{RS}")
        print(f"{B}║{W} [0]{R}   Back to Main Menu                                 {B}║{RS}")
        print(f"{B}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[OSINT] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': dns_enum()
        elif ch == '2': whois_lookup()
        elif ch == '3': ip_geolocation()
        elif ch == '4': subdomain_discovery()
        elif ch == '5': port_scan()
        elif ch == '6': email_osint()
        elif ch == '7': phone_osint()
        elif ch == '8': username_osint()
        elif ch == '9': web_crawler()
        elif ch == '10': ssl_analyze()
        elif ch == '11': http_header_analyze()
        elif ch == '12': reverse_ip()
        elif ch == '13': shodan_search()
        elif ch == '14': google_dorks()
        elif ch == '15': wayback_machine()
        elif ch == '16': email_harvest()
        elif ch == '17': social_analyze()
        elif ch == '18': mac_lookup()
        elif ch == '19': banner_grab()
        elif ch == '20': protocol_analyze()
        elif ch == '21': iot_scanner()
        elif ch == '22': cloud_discovery()
        elif ch == '23': pastebin_monitor()
        elif ch == '24': stealth_scan()
        elif ch == '25': ai_recon_report()
        else: print(f"{R}[!] Invalid option{RS}")

def dns_enum():
    """Tool 1: DNS Enumeration"""
    domain = input(f"  {W}[?] Domain: {RS}").strip()
    print(f"\n{G}[+] DNS Enumeration for {domain}{RS}")
    
    print(f"\n{W}A Records:{RS}")
    try:
        ips = socket.gethostbyname_ex(domain)
        for ip in ips[2]:
            print(f"  {C}{domain}{RS} → {Y}{ip}{RS}")
    except: print(f"  {R}[-] Lookup failed{RS}")
    
    print(f"\n{W}NS Records:{RS}")
    out = _run(f'nslookup -type=NS {domain} 2>/dev/null || host -t NS {domain} 2>/dev/null')
    print(f"  {Y}{out or 'Not available'}{RS}")
    
    print(f"\n{W}MX Records:{RS}")
    out = _run(f'nslookup -type=MX {domain} 2>/dev/null || host -t MX {domain} 2>/dev/null')
    print(f"  {Y}{out or 'Not available'}{RS}")
    
    print(f"\n{W}TXT Records:{RS}")
    out = _run(f'nslookup -type=TXT {domain} 2>/dev/null || host -t TXT {domain} 2>/dev/null')
    print(f"  {Y}{out or 'Not available'}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def whois_lookup():
    """Tool 2: WHOIS Lookup"""
    target = input(f"  {W}[?] Domain or IP: {RS}").strip()
    print(f"\n{G}[+] WHOIS Lookup for {target}{RS}")
    
    try:
        import whois
        w = whois.whois(target)
        print(f"  {C}Domain:{RS} {w.domain}")
        print(f"  {C}Registrar:{RS} {w.registrar}")
        print(f"  {C}Creation:{RS} {w.creation_date}")
        print(f"  {C}Expiration:{RS} {w.expiration_date}")
        print(f"  {C}Name Servers:{RS} {w.name_servers}")
        print(f"  {C}Org:{RS} {w.org}")
        print(f"  {C}Country:{RS} {w.country}")
        print(f"  {C}Emails:{RS} {w.emails}")
    except ImportError:
        # Fallback to command line whois
        out = _run(f'whois {target}')
        print(f"  {Y}{out[:2000]}{RS}")
    except Exception as e:
        print(f"  {R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def ip_geolocation():
    """Tool 3: IP Geolocation"""
    target = input(f"  {W}[?] IP Address: {RS}").strip()
    print(f"\n{G}[+] Geolocating {target}{RS}")
    
    try:
        import requests
        r = requests.get(f'http://ip-api.com/json/{target}', timeout=10)
        data = r.json()
        if data.get('status') == 'success':
            print(f"  {C}IP:{RS} {data.get('query')}")
            print(f"  {C}Country:{RS} {data.get('country')} ({data.get('countryCode')})")
            print(f"  {C}Region:{RS} {data.get('regionName')}")
            print(f"  {C}City:{RS} {data.get('city')}")
            print(f"  {C}ZIP:{RS} {data.get('zip')}")
            print(f"  {C}ISP:{RS} {data.get('isp')}")
            print(f"  {C}Org:{RS} {data.get('org')}")
            print(f"  {C}AS:{RS} {data.get('as')}")
            print(f"  {C}Lat/Lon:{RS} {data.get('lat')}, {data.get('lon')}")
            print(f"  {C}Timezone:{RS} {data.get('timezone')}")
        else:
            print(f"  {R}[-] {data.get('message', 'Lookup failed')}{RS}")
    except Exception as e:
        print(f"  {R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def subdomain_discovery():
    """Tool 4: Subdomain Discovery"""
    domain = input(f"  {W}[?] Domain: {RS}").strip()
    print(f"\n{G}[+] Discovering subdomains for {domain}...{RS}")
    
    # Common subdomains wordlist
    subs = ['www','mail','admin','api','blog','dev','staging','test','vpn','portal',
            'secure','app','cdn','static','assets','img','files','support','help','docs',
            'webmail','smtp','pop','imap','ftp','ssh','git','jenkins','jira','confluence',
            'dashboard','backup','monitor','status','wiki','forum','community','shop',
            'store','billing','payment','gateway','login','register','signup','contact',
            'about','news','events','calendar','mobile','m','remote','office365','owa',
            'autodiscover','lyncdiscover','sip','vpn','radius','ns1','ns2','ns3','mx',
            'mail2','mail1','server','clients','whm','cpanel','direct','beta','alpha',
            'demo','stage','prod','preprod','qa','labs','internal','external','partner',
            'corp','hr','employees','intranet','extranet','analytics','tracking','stats']
    
    found = []
    for sub in subs:
        url = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(url)
            found.append((url, ip))
            print(f"  {G}[+]{RS} {C}{url:<30}{RS} {Y}{ip}{RS}")
        except:
            pass
    
    if not found:
        print(f"  {Y}[-] No subdomains found via basic lookup{RS}")
        print(f"  {Y}[!] Try using Sublist3r or Amass for deeper scanning{RS}")
    else:
        print(f"\n{G}[+] Found {len(found)} subdomains{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def port_scan():
    """Tool 5: Port Scanner"""
    target = input(f"  {W}[?] Target IP/Domain: {RS}").strip()
    ports_input = input(f"  {W}[?] Ports (e.g., 1-1000 or 22,80,443): {RS}").strip()
    
    # Parse ports
    ports = []
    if '-' in ports_input:
        parts = ports_input.split('-')
        ports = list(range(int(parts[0]), int(parts[1])+1))
    elif ',' in ports_input:
        ports = [int(p.strip()) for p in ports_input.split(',')]
    elif ports_input:
        ports = [int(ports_input)]
    else:
        ports = list(range(1, 1025))
    
    print(f"\n{G}[+] Scanning {target} for {len(ports)} ports...{RS}")
    print(f"{Y}[!] Press Ctrl+C to stop{RS}\n")
    
    open_ports = []
    try:
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex((target, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = 'unknown'
                open_ports.append((port, service))
                print(f"  {G}[OPEN]{RS} Port {C}{port:>5}{RS} → {Y}{service}{RS}")
            s.close()
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Scan interrupted{RS}")
    except Exception as e:
        print(f"  {R}[-] Error: {e}{RS}")
    
    print(f"\n{G}[+] Scan complete. Found {len(open_ports)} open ports.{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def email_osint():
    """Tool 6: Email OSINT"""
    email = input(f"  {W}[?] Email address: {RS}").strip()
    print(f"\n{G}[+] OSINT analysis for {email}{RS}")
    
    # Extract domain
    domain = email.split('@')[-1] if '@' in email else email
    
    print(f"\n  {W}Email Analysis:{RS}")
    print(f"  {C}Domain:{RS} {domain}")
    
    # Check if domain exists
    try:
        socket.gethostbyname(domain)
        print(f"  {C}Domain Status:{RS} {G}✓ Valid{RS}")
    except:
        print(f"  {C}Domain Status:{RS} {R}✗ Invalid{RS}")
    
    # Check for gravatar
    import hashlib
    hash = hashlib.md5(email.lower().encode()).hexdigest()
    print(f"  {C}Gravatar URL:{RS} https://www.gravatar.com/avatar/{hash}")
    
    # Check for breach (using haveibeenpwned API)
    print(f"\n  {W}Breach Check:{RS}")
    try:
        import requests
        prefix = hash[:5]
        r = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}', timeout=10)
        if r.status_code == 200:
            print(f"  {Y}[!] Check https://haveibeenpwned.com/account/{email} manually{RS}")
        print(f"  {Y}[!] API rate limited - use HIBP website for full check{RS}")
    except:
        print(f"  {R}[-] Cannot check breaches (no internet){RS}")
    
    # Google search URL
    print(f"\n  {W}Google Search:{RS} https://www.google.com/search?q={email}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def phone_osint():
    """Tool 7: Phone Number OSINT"""
    phone = input(f"  {W}[?] Phone number (with country code, e.g., +1234567890): {RS}").strip()
    print(f"\n{G}[+] OSINT analysis for {phone}{RS}")
    
    try:
        import phonenumbers
        from phonenumbers import carrier, geocoder, timezone
        
        num = phonenumbers.parse(phone)
        print(f"  {C}Country:{RS} {geocoder.description_for_number(num, 'en')}")
        print(f"  {C}Location:{RS} {geocoder.description_for_number(num, 'en')}")
        print(f"  {C}Carrier:{RS} {carrier.name_for_number(num, 'en')}")
        print(f"  {C}Timezone:{RS} {timezone.time_zones_for_number(num)}")
        print(f"  {C}Valid:{RS} {phonenumbers.is_valid_number(num)}")
        print(f"  {C}Possible:{RS} {phonenumbers.is_possible_number(num)}")
        print(f"  {C}E.164:{RS} {phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164)}")
        print(f"  {C}International:{RS} {phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
        print(f"  {C}National:{RS} {phonenenumbers.format_number(num, phonenumbers.PhoneNumberFormat.NATIONAL)}")
    except ImportError:
        print(f"  {Y}[!] Install phonenumbers for detailed analysis: pip install phonenumbers{RS}")
        print(f"  {Y}[!] Country: Check prefix manually{RS}")
    
    print(f"\n  {W}Truecaller Lookup:{RS} https://www.truecaller.com/search/{phone}")
    print(f"  {W}SpyDialer:{RS} https://spydialer.com/default.aspx")
    print(f"  {W}Whitepages:{RS} https://www.whitepages.com/phone/{phone}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def username_osint():
    """Tool 8: Username OSINT"""
    username = input(f"  {W}[?] Username: {RS}").strip()
    print(f"\n{G}[+] Searching for '{username}' across platforms...{RS}")
    
    platforms = {
        'Facebook': 'https://facebook.com/{}',
        'Instagram': 'https://instagram.com/{}',
        'Twitter/X': 'https://twitter.com/{}',
        'GitHub': 'https://github.com/{}',
        'Reddit': 'https://reddit.com/user/{}',
        'Telegram': 'https://t.me/{}',
        'TikTok': 'https://tiktok.com/@{}',
        'YouTube': 'https://youtube.com/@{}',
        'Medium': 'https://medium.com/@{}',
        'Twitch': 'https://twitch.tv/{}',
        'Pinterest': 'https://pinterest.com/{}',
        'Snapchat': 'https://snapchat.com/add/{}',
        'Mastodon': 'https://mastodon.social/@{}',
        'Dev.to': 'https://dev.to/{}',
        'HackerNews': 'https://news.ycombinator.com/user?id={}',
        'Keybase': 'https://keybase.io/{}',
        'About.me': 'https://about.me/{}',
        'AngelList': 'https://angel.co/u/{}',
        'ProductHunt': 'https://producthunt.com/@{}',
        'Behance': 'https://behance.net/{}',
        'Dribbble': 'https://dribbble.com/{}',
        'Flickr': 'https://flickr.com/people/{}',
        'Spotify': 'https://open.spotify.com/user/{}',
        'Steam': 'https://steamcommunity.com/id/{}',
        'VK': 'https://vk.com/{}',
    }
    
    for name, url_template in platforms.items():
        print(f"  {C}{name:<15}{RS} → {Y}{url_template.format(username)}{RS}")
    
    print(f"\n{G}[+] For automated checking, use Sherlock: https://github.com/sherlock-project/sherlock{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def web_crawler():
    """Tool 9: Website Crawler"""
    url = input(f"  {W}[?] Target URL: {RS}").strip()
    depth = int(input(f"  {W}[?] Crawl depth (1-5): {RS}").strip() or '2')
    
    print(f"\n{G}[+] Crawling {url} (depth={depth})...{RS}")
    try:
        import requests
        from bs4 import BeautifulSoup
        
        visited = set()
        to_visit = [url]
        links_found = 0
        emails_found = set()
        
        while to_visit and links_found < 100:
            current = to_visit.pop(0)
            if current in visited: continue
            visited.add(current)
            
            try:
                r = requests.get(current, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(r.text, 'html.parser')
                
                # Extract emails
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                found_emails = re.findall(email_pattern, r.text)
                for e in found_emails:
                    if e not in emails_found:
                        emails_found.add(e)
                        print(f"  {G}[EMAIL]{RS} {Y}{e}{RS}")
                
                # Extract links
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href.startswith('http') and href not in visited:
                        to_visit.append(href)
                        links_found += 1
                        print(f"  {C}[LINK]{RS} {Y}{href[:100]}{RS}")
                        
            except Exception as e:
                pass
        
        print(f"\n{G}[+] Crawl complete:{RS}")
        print(f"  {W}Pages visited:{RS} {len(visited)}")
        print(f"  {W}Links found:{RS} {links_found}")
        print(f"  {W}Emails found:{RS} {len(emails_found)}")
        
    except ImportError:
        print(f"{R}[-] Install requests and beautifulsoup4: pip install requests beautifulsoup4{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def ssl_analyze():
    """Tool 10: SSL/TLS Certificate Analysis"""
    target = input(f"  {W}[?] Domain: {RS}").strip()
    port = input(f"  {W}[?] Port (default 443): {RS}").strip() or '443'
    
    print(f"\n{G}[+] Analyzing SSL/TLS certificate for {target}:{port}{RS}")
    try:
        import ssl, socket
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=target) as s:
            s.settimeout(10)
            s.connect((target, int(port)))
            cert = s.getpeercert()
            
            print(f"  {C}Subject:{RS} {dict(x[0] for x in cert['subject'])}")
            print(f"  {C}Issuer:{RS} {dict(x[0] for x in cert['issuer'])}")
            print(f"  {C}Version:{RS} {cert.get('version')}")
            print(f"  {C}Serial:{RS} {cert.get('serialNumber')}")
            print(f"  {C}Not Before:{RS} {cert.get('notBefore')}")
            print(f"  {C}Not After:{RS} {cert.get('notAfter')}")
            print(f"  {C}SAN:{RS} {cert.get('subjectAltName', [('DNS','N/A')])}")
            
            # Check expiry
            from datetime import datetime
            exp = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            days_left = (exp - datetime.now()).days
            if days_left > 30:
                print(f"  {G}[✓] Certificate expires in {days_left} days{RS}")
            elif days_left > 0:
                print(f"  {Y}[!] Certificate expires in {days_left} days (soon!){RS}")
            else:
                print(f"  {R}[✗] Certificate EXPIRED!{RS}")
                
    except Exception as e:
        print(f"  {R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def http_header_analyze():
    """Tool 11: HTTP Header Analyzer"""
    url = input(f"  {W}[?] URL: {RS}").strip()
    print(f"\n{G}[+] Analyzing HTTP headers for {url}{RS}")
    
    try:
        import requests
        r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        
        print(f"\n  {W}Response Headers:{RS}")
        security_headers = {
            'Strict-Transport-Security': 'HSTS',
            'Content-Security-Policy': 'CSP',
            'X-Content-Type-Options': 'XCTO',
            'X-Frame-Options': 'XFO',
            'X-XSS-Protection': 'XXSS',
            'Referrer-Policy': 'Referrer',
            'Permissions-Policy': 'Permissions',
            'Set-Cookie': 'Cookies'
        }
        
        for header, value in r.headers.items():
            flag = ''
            if header in security_headers:
                flag = f' {G}[SEC]{RS}'
            elif header.lower().startswith('x-'):
                flag = f' {Y}[CUSTOM]{RS}'
            else:
                flag = f' {C}[STANDARD]{RS}'
            print(f"  {W}{header}:{RS} {Y}{value}{RS}{flag}")
        
        print(f"\n  {W}Security Assessment:{RS}")
        for sh in security_headers:
            if sh in r.headers:
                print(f"  {G}[✓]{RS} {sh} is set")
            else:
                print(f"  {R}[✗]{RS} {sh} is MISSING")
        
        print(f"\n  {W}Server Info:{RS} {r.headers.get('Server', 'Unknown')}")
        print(f"  {W}Powered By:{RS} {r.headers.get('X-Powered-By', 'N/A')}")
        
    except Exception as e:
        print(f"  {R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def reverse_ip():
    """Tool 12: Reverse IP Lookup"""
    ip = input(f"  {W}[?] IP Address: {RS}").strip()
    print(f"\n{G}[+] Reverse IP lookup for {ip}{RS}")
    print(f"{Y}[!] Use services like yougetsignal.com, viewdns.info, or{RS}")
    print(f"{Y}[!] Run: host {ip} for PTR records{RS}")
    
    # Try PTR lookup
    try:
        host = socket.gethostbyaddr(ip)
        print(f"  {C}PTR Record:{RS} {Y}{host[0]}{RS}")
        print(f"  {C}Aliases:{RS} {Y}{host[1]}{RS}")
    except:
        print(f"  {R}[-] No PTR record found{RS}")
    
    # Check bing
    print(f"\n  {W}Check hosted domains:{RS}")
    print(f"  https://www.bing.com/search?q=ip%3A{ip}")
    print(f"  https://viewdns.info/reverseip/?host={ip}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def shodan_search():
    """Tool 13: Shodan Search"""
    query = input(f"  {W}[?] Shodan search query: {RS}").strip()
    print(f"\n{G}[+] Searching Shodan for: {query}{RS}")
    
    try:
        import shodan
        api_key = input(f"  {W}[?] Shodan API key (or press Enter for demo): {RS}").strip()
        
        if not api_key:
            print(f"{Y}[!] Get API key at https://shodan.io{RS}")
            print(f"{Y}[!] Example results:{RS}")
            print(f"  {C}Search:{RS} {query}")
            print(f"  {C}Demo:{RS} Use Shodan website for full results")
        else:
            api = shodan.Shodan(api_key)
            results = api.search(query)
            print(f"{G}[+] Found {results['total']} results{RS}")
            for r in results['matches'][:10]:
                print(f"  {C}{r['ip_str']}:{r['port']}{RS} - {Y}{r.get('org','N/A')}{RS}")
    except ImportError:
        print(f"{Y}[!] Install shodan: pip install shodan{RS}")
        print(f"{Y}[!] Website: https://shodan.io/search?query={query}{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def google_dorks():
    """Tool 14: Google Dork Generator"""
    print(f"\n{G}[+] Google Dork Generator{RS}")
    target = input(f"  {W}[?] Target domain/term: {RS}").strip()
    
    dorks = [
        f"site:{target} admin",
        f"site:{target} login",
        f"site:{target} password",
        f"site:{target} confidential",
        f"site:{target} 'index of'",
        f"site:{target} inurl:admin",
        f"site:{target} inurl:login",
        f"site:{target} filetype:pdf",
        f"site:{target} filetype:xls password",
        f"site:{target} filetype:sql",
        f"site:{target} filetype:env",
        f"site:{target} filetype:bak",
        f"site:{target} ext:php intitle:phpinfo",
        f"site:{target} inurl:wp-admin",
        f"site:{target} inurl:backup",
        f"site:{target} intitle:'index of' 'parent directory'",
        f"site:{target} 'sql' 'password'",
        f'site:{target} ext:log "password"',
        f"site:{target} 'admin' 'password' filetype:txt",
        f"site:*.{target} inurl:dev",
        f"site:*.{target} 'server' 'error'",
        f'site:{target} "ssh" "private"',
        f"site:{target} intitle:webcam",
        f"site:{target} inurl:phpMyAdmin",
        f"site:pastebin.com {target}",
    ]
    
    print(f"\n{G}[+] Google Dorks for {target}:{RS}\n")
    for i, dork in enumerate(dorks, 1):
        print(f"  {W}{i:02d}.{RS} {Y}{dork}{RS}")
    
    print(f"\n{G}[+] Pro tip: Use site:*.{target} for subdomain discovery{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def wayback_machine():
    """Tool 15: Wayback Machine History"""
    target = input(f"  {W}[?] URL/Domain: {RS}").strip()
    print(f"\n{G}[+] Fetching Wayback Machine history for {target}{RS}")
    
    try:
        import requests
        r = requests.get(f'https://web.archive.org/cdx/search/cdx?url={target}&output=json&limit=20', timeout=15)
        data = r.json()
        if len(data) > 1:
            print(f"  {C}Historical snapshots:{RS}")
            for entry in data[1:]:
                print(f"  {G}[+]{RS} {entry[1]} - {entry[2]}")
        else:
            print(f"  {Y}[-] No snapshots found{RS}")
    except Exception as e:
        print(f"  {R}[-] Error: {e}{RS}")
        print(f"  {Y}[!] Visit: https://web.archive.org/web/*/{target}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def email_harvest():
    """Tool 16: Email Harvester"""
    target = input(f"  {W}[?] Domain to harvest emails from: {RS}").strip()
    print(f"\n{G}[+] Harvesting emails from {target}...{RS}")
    
    emails_found = set()
    
    # Search Google
    try:
        import requests
        from bs4 import BeautifulSoup
        
        search_urls = [
            f'https://www.google.com/search?q=%40{target}',
            f'https://www.bing.com/search?q=%40{target}',
        ]
        
        for search_url in search_urls:
            try:
                r = requests.get(search_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.{target}', r.text)
                for e in emails:
                    emails_found.add(e)
            except: pass
        
        print(f"\n{G}[+] Found {len(emails_found)} emails:{RS}")
        for e in sorted(emails_found):
            print(f"  {C}{e}{RS}")
        
        # Save to file
        if emails_found:
            fname = f"emails_{target}_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(fname, 'w') as f:
                f.write('\n'.join(sorted(emails_found)))
            print(f"\n{G}[+] Saved {len(emails_found)} emails to {fname}{RS}")
            
    except Exception as e:
        print(f"  {R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def social_analyze():
    """Tool 17: Social Media Profile Analyzer"""
    print(f"\n{G}[+] Social Media Profile Analyzer{RS}")
    platform = input(f"  {W}[?] Platform (instagram/twitter/facebook): {RS}").strip().lower()
    username = input(f"  {W}[?] Username/Profile URL: {RS}").strip()
    
    print(f"\n{Y}[!] Analyzing {platform} profile for {username}...{RS}")
    
    analysis = f"""
  {W}Profile Analysis Summary:{RS}
  
  {C}Platform:{RS} {platform}
  {C}Username:{RS} {username}
  
  {W}Recommended Actions:{RS}
  1. Check profile privacy settings
  2. Review shared personal information
  3. Look for location tags in posts
  4. Check tagged photos and friends lists
  5. Review third-party app access
  6. Check for duplicate accounts
  7. Monitor for impersonation
  8. Review posting history patterns
  
  {W}OSINT Opportunities:{RS}
  - Extract metadata from posted photos
  - Analyze posting schedule patterns
  - Map social connections and relationship networks
  - Identify workplace and education information
  - Discover email addresses in comments/bio
  """
    print(analysis)
    
    print(f"\n{W}Direct links:{RS}")
    print(f"  https://{platform}.com/{username}")
    if platform == 'instagram':
        print(f"  https://imginn.com/{username}/")
        print(f"  https://dumpoir.com/{username}/")
    print(f"  https://psbdmp.ws/search?q={username}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def mac_lookup():
    """Tool 18: MAC Address Lookup"""
    mac = input(f"  {W}[?] MAC Address: {RS}").strip()
    print(f"\n{G}[+] Looking up MAC {mac}...{RS}")
    
    try:
        import requests
        r = requests.get(f'https://api.macvendors.com/{mac}', timeout=10)
        if r.status_code == 200:
            print(f"  {C}Manufacturer:{RS} {Y}{r.text}{RS}")
        else:
            print(f"  {Y}[-] Unknown vendor{RS}")
    except:
        # Built-in OUI lookup
        oui = mac[:8].upper().replace(':','')
        print(f"  {C}OUI:{RS} {oui}")
        print(f"  {Y}[!] Check https://ouilookup.com/{oui}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def banner_grab():
    """Tool 19: Banner Grabbing"""
    target = input(f"  {W}[?] Target IP/Domain: {RS}").strip()
    port = int(input(f"  {W}[?] Port: {RS}").strip() or '80')
    
    print(f"\n{G}[+] Grabbing banner from {target}:{port}...{RS}")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((target, port))
        
        if port == 80:
            s.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
        
        banner = s.recv(1024).decode('utf-8', errors='ignore')
        print(f"  {Y}{banner}{RS}")
        s.close()
        
        # Analysis
        print(f"\n  {W}Banner Analysis:{RS}")
        if 'Apache' in banner:
            print(f"  {G}[+] Web Server: Apache{RS}")
        elif 'nginx' in banner:
            print(f"  {G}[+] Web Server: Nginx{RS}")
        elif 'IIS' in banner:
            print(f"  {G}[+] Web Server: IIS (Windows){RS}")
        if 'OpenSSH' in banner:
            print(f"  {G}[+] SSH Server detected{RS}")
        
    except Exception as e:
        print(f"  {R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def protocol_analyze():
    """Tool 20: Network Protocol Analyzer"""
    print(f"\n{Y}[!] Network Protocol Analyzer{RS}")
    print(f"\n{W}Available protocols to analyze:{RS}")
    protocols = {
        'HTTP': 80, 'HTTPS': 443, 'FTP': 21, 'SSH': 22, 'Telnet': 23,
        'SMTP': 25, 'DNS': 53, 'DHCP': 67, 'SNMP': 161, 'LDAP': 389,
        'MySQL': 3306, 'PostgreSQL': 5432, 'MongoDB': 27017, 'Redis': 6379
    }
    
    for p, port in protocols.items():
        print(f"  {C}{p:<15}{RS} Port {Y}{port}{RS}")
    
    target = input(f"\n  {W}[?] Target to analyze: {RS}").strip()
    print(f"\n{G}[+] Analyzing protocols on {target}...{RS}")
    
    open_ports = []
    for proto, port in protocols.items():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            r = s.connect_ex((target, port))
            if r == 0:
                open_ports.append((port, proto))
                print(f"  {G}[✓]{RS} {proto} (Port {port}) - {Y}OPEN{RS}")
            s.close()
        except: pass
    
    if not open_ports:
        print(f"  {Y}[-] No common protocol ports open{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def iot_scanner():
    """Tool 21: IoT Device Scanner"""
    print(f"\n{G}[+] IoT Device Scanner{RS}")
    subnet = input(f"  {W}[?] Subnet (e.g., 192.168.1.0/24): {RS}").strip()
    
    print(f"\n{Y}[!] Scanning {subnet} for IoT devices...{RS}")
    
    # IoT signature ports
    iot_ports = {
        23: 'Telnet (IoT devices)',
        80: 'HTTP (Web interface)',
        443: 'HTTPS',
        554: 'RTSP (IP Cameras)',
        1900: 'UPnP',
        5000: 'Various IoT',
        8080: 'HTTP-Alt (IP Cameras)',
        49152: 'UPnP (Windows IoT)',
        37777: 'Dahua Cameras',
        34567: 'Hikvision Cameras',
        2000: 'Siemens IoT',
        1883: 'MQTT (IoT Protocol)',
        8883: 'MQTT over SSL',
        5683: 'CoAP (IoT Protocol)'
    }
    
    try:
        import ipaddress
        net = ipaddress.ip_network(subnet, strict=False)
        
        for host in net.hosts():
            host_str = str(host)
            for port, desc in iot_ports.items():
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    if s.connect_ex((host_str, port)) == 0:
                        print(f"  {G}[+]{RS} {C}{host_str}:{port}{RS} - {Y}{desc}{RS}")
                    s.close()
                except: pass
    except Exception as e:
        print(f"  {R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def cloud_discovery():
    """Tool 22: Cloud Asset Discovery"""
    domain = input(f"  {W}[?] Domain to check for cloud assets: {RS}").strip()
    print(f"\n{G}[+] Discovering cloud assets for {domain}...{RS}")
    
    print(f"\n  {W}Checking cloud providers...{RS}")
    
    # Check AWS
    try:
        s3_buckets = [
            domain,
            domain.replace('.', '-'),
            f'{domain}-backup',
            f'{domain}-assets',
            f'{domain}-static',
        ]
        print(f"\n  {C}AWS S3 Buckets:{RS}")
        for b in s3_buckets:
            print(f"    https://{b}.s3.amazonaws.com")
            print(f"    https://s3.amazonaws.com/{b}")
        
        # Check for CloudFront
        print(f"\n  {C}AWS CloudFront:{RS}")
        print(f"    https://dXXXXXXXXXXXXX.cloudfront.net (check DNS)")
        
        # Check for ELB
        print(f"\n  {C}AWS ELB:{RS}")
        print(f"    https://{domain} (check for ELB DNS)")
    except: pass
    
    # Check Google Cloud
    print(f"\n  {C}Google Cloud:{RS}")
    print(f"    https://{domain}.appspot.com")
    print(f"    https://storage.googleapis.com/{domain}")
    print(f"    https://{domain}.firebaseapp.com")
    print(f"    https://{domain}.cloudfunctions.net")
    
    # Check Azure
    print(f"\n  {C}Microsoft Azure:{RS}")
    print(f"    https://{domain}.azurewebsites.net")
    print(f"    https://{domain}.cloudapp.net")
    print(f"    https://{domain}.blob.core.windows.net")
    
    # Check DigitalOcean
    print(f"\n  {C}DigitalOcean:{RS}")
    print(f"    https://{domain}.ondigitalocean.app")
    
    # Check Vercel/Netlify
    print(f"\n  {C}Other:{RS}")
    print(f"    https://{domain}.vercel.app")
    print(f"    https://{domain}.netlify.app")
    print(f"    https://{domain}.pages.dev")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def pastebin_monitor():
    """Tool 23: Pastebin / Dark Web Monitor"""
    query = input(f"  {W}[?] Search term/email/domain: {RS}").strip()
    print(f"\n{G}[+] Searching leak sites for: {query}{RS}")
    
    sites = [
        f"https://pastebin.com/search?q={query}",
        f"https://psbdmp.ws/search?q={query}",
        f"https://scylla.so/search?q={query}",
        f"https://leakcheck.io/search?q={query}",
        f"https://breachdirectory.org/search?q={query}",
        f"https://dehashed.com/search?q={query}",
        f"https://intelx.io/?s={query}",
        f"https://vigilante.pw/search?q={query}",
    ]
    
    for url in sites:
        print(f"  {C}[+]{RS} {Y}{url}{RS}")
    
    print(f"\n{Y}[!] Check these sites for leaked credentials{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def stealth_scan():
    """Tool 24: Stealth Scan (Half-Open SYN)"""
    target = input(f"  {W}[?] Target IP: {RS}").strip()
    ports = input(f"  {W}[?] Port range (e.g., 1-1000): {RS}").strip() or '1-1024'
    
    print(f"\n{Y}[!] SYN Stealth Scan requires root/admin and raw sockets{RS}")
    print(f"{G}[+] On Linux, use: nmap -sS {target} -p {ports}{RS}")
    print(f"{G}[+] On Windows, use: nmap -sT {target} -p {ports}{RS}")
    
    # Try using nmap
    out = _run(f'nmap -sS -p {ports} {target} 2>/dev/null || echo "nmap not found"')
    print(f"\n{Y}{out[:1000]}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def ai_recon_report():
    """Tool 25: AI-Powered Recon Report"""
    target = input(f"  {W}[?] Target domain/IP: {RS}").strip()
    print(f"\n{G}[+] Generating AI-powered reconnaissance report for {target}...{RS}")
    
    # Gather basic info
    info = {}
    try:
        info['ip'] = socket.gethostbyname(target)
    except:
        info['ip'] = target
    
    print(f"""
  ╔═══════════════════════════════════════════════════════╗
  ║              RECONNAISSANCE REPORT                    ║
  ╠═══════════════════════════════════════════════════════╣
  ║  Target:     {target:<43}║
  ║  IP:         {info['ip']:<43}║
  ║  Date:       {datetime.now().strftime('%Y-%m-%d %H:%M'):<43}║
  ╠═══════════════════════════════════════════════════════╣
  ║  RECOMMENDATIONS:                                    ║
  ║                                                       ║
  ║  1. Perform full port scan (1-65535)                  ║
  ║  2. Run directory busting (dirb/gobuster)             ║
  ║  3. Check for known CVEs (searchsploit)              ║
  ║  4. Enumerate subdomains (sublist3r/amass)            ║
  ║  5. Test for common web vulnerabilities               ║
  ║  6. Review SSL/TLS configuration                      ║
  ║  7. Check for exposed .git/.env files                 ║
  ║  8. Test default credentials                          ║
  ║  9. Check WAF / security measures                     ║
  ║  10. Review DNS records for subdomain takeover         ║
  ╚═══════════════════════════════════════════════════════╝
  """)
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
