#!/usr/bin/env python3
# ============================================================
#  A2Tool v3.0 - Advanced All-in-One Penetration Testing Suite
#  Author  : Ayush Rajdev & Anzar Iqbal
#  Platform: Windows / Linux / macOS / Android (Termux)
# ============================================================

import os, sys, time, platform, json, subprocess, threading, webbrowser

# Ensure colorama is available
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    # Fallback if colorama not installed
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ''
    Style = Fore

# ANSI color helpers
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
M = Fore.MAGENTA
C = Fore.CYAN
W = Fore.WHITE
RS = Style.RESET_ALL

# ────────────────────────────────────────────────────────
# Banner
# ────────────────────────────────────────────────────────
BANNER = f"""{R}
  ╔═══════════════════════════════════════════════════════╗
  ║    {C}████████╗{R}██╗  ██╗{Y}████████╗{G} ██████╗ {B}███████╗{R}██╗     {M}██╗{R}  ║
  ║    {C}╚══██╔══╝{R}██║  ██║{Y}╚══██╔══╝{G}██╔═══██╗{B}██╔════╝{R}██║     {M}██║{R}  ║
  ║    {C}   ██║   {R}███████║{Y}   ██║   {G}██║   ██║{B}█████╗  {R}██║     {M}██║{R}  ║
  ║    {C}   ██║   {R}██╔══██║{Y}   ██║   {G}██║   ██║{B}██╔══╝  {R}██║     {M}██║{R}  ║
  ║    {C}   ██║   {R}██║  ██║{Y}   ██║   {G}╚██████╔╝{B}███████╗{R}███████╗{M}██║{R}  ║
  ║    {C}   ╚═╝   {R}╚═╝  ╚═╝{Y}   ╚═╝   {G} ╚═════╝ {B}╚══════╝{R}╚══════╝{M}╚═╝{R}  ║
  ║                                                       ║
  ║  {Y}Advanced All-in-One Penetration Testing Suite{R}       ║
  ║  {C}Author: Ayush Rajdev & Anzar Iqbal{R}                ║
  ║  {G}Version 3.0 - Zero to Hero{R}                        ║
  ╚═══════════════════════════════════════════════════════╝
{RS}"""

# ────────────────────────────────────────────────────────
# Platform detection
# ────────────────────────────────────────────────────────
OS_NAME = platform.system().lower()  # 'windows', 'linux', 'darwin'
IS_WINDOWS = OS_NAME == 'windows'
IS_LINUX   = OS_NAME == 'linux'
IS_MACOS   = OS_NAME == 'darwin'
IS_ANDROID = 'android' in platform.platform().lower() or 'termux' in os.environ.get('PREFIX', '')

def clear_screen():
    os.system('cls' if IS_WINDOWS else 'clear')

def pause():
    if IS_WINDOWS:
        os.system('pause')
    else:
        input(f"\n{Y}[+] Press Enter to continue...{RS}")

# ────────────────────────────────────────────────────────
# Import internal modules
# ────────────────────────────────────────────────────────
from modules import (
    wifi_tool,
    phishing,
    social_engineering,
    info_gathering,
    exploits,
    utils,
    payloads
)

# ────────────────────────────────────────────────────────
# Menu system
# ────────────────────────────────────────────────────────
def show_banner():
    clear_screen()
    print(BANNER)

def main_menu():
    while True:
        show_banner()
        print(f"{C}╔═══════════════════════════════════════════════════════╗")
        print(f"║  {W}[01]{R}  WiFi Hacking & Password Recovery             {C}║")
        print(f"║  {W}[02]{R}  Phishing Attacks Framework                    {C}║")
        print(f"║  {W}[03]{R}  Social Engineering Toolkit                    {C}║")
        print(f"║  {W}[04]{R}  Information Gathering (OSINT)                {C}║")
        print(f"║  {W}[05]{R}  Exploitation Framework                        {C}║")
        print(f"║  {W}[06]{R}  Payload Generator                             {C}║")
        print(f"║  {W}[07]{R}  Network Scanner & Analysis                    {C}║")
        print(f"║  {W}[08]{R}  Password Cracking & Hash Tools                {C}║")
        print(f"║  {W}[09]{R}  Web Application Attacks                       {C}║")
        print(f"║  {W}[10]{R}  Reverse Shell & Backdoor Tools               {C}║")
        print(f"║  {W}[11]{R}  DDoS / Stress Testing Tools                   {C}║")
        print(f"║  {W}[12]{R}  Bluetooth Hacking                             {C}║")
        print(f"║  {W}[13]{R}  Camera / Mic Exploitation                     {C}║")
        print(f"║  {W}[14]{R}  Keylogger & Spyware Tools                     {C}║")
        print(f"║  {W}[15]{R}  VPN & Proxy Chaining                          {C}║")
        print(f"║  {W}[16]{R}  Steganography Tools                           {C}║")
        print(f"║  {W}[17]{R}  Forensic & Anti-Forensic Tools               {C}║")
        print(f"║  {W}[18]{R}  Cryptography & Encryption Tools              {C}║")
        print(f"║  {W}[19]{R}  System Info & Vulnerability Scanner          {C}║")
        print(f"║  {W}[20]{R}  About / Update                               {C}║")
        print(f"║  {W}[0]{R}   Exit                                         {C}║")
        print(f"╚═══════════════════════════════════════════════════════╝")
        print(f"{G}  Platform: {C}{platform.system()} {platform.release()}{RS}")
        choice = input(f"\n{Y}  A2Tool » {RS}").strip()

        if choice == '0':
            print(f"\n{R}[!] Exiting A2Tool. Stay secure!{RS}")
            sys.exit(0)
        elif choice == '1':   wifi_tool.menu()
        elif choice == '2':   phishing.menu()
        elif choice == '3':   social_engineering.menu()
        elif choice == '4':   info_gathering.menu()
        elif choice == '5':   exploits.menu()
        elif choice == '6':   payloads.menu()
        elif choice == '7':   network_scanner_menu()
        elif choice == '8':   password_cracking_menu()
        elif choice == '9':   web_attack_menu()
        elif choice == '10':  reverse_shell_menu()
        elif choice == '11':  ddos_menu()
        elif choice == '12':  bluetooth_menu()
        elif choice == '13':  camera_mic_menu()
        elif choice == '14':  keylogger_menu()
        elif choice == '15':  vpn_proxy_menu()
        elif choice == '16':  stego_menu()
        elif choice == '17':  forensic_menu()
        elif choice == '18':  crypto_menu()
        elif choice == '19':  vuln_scan_menu()
        elif choice == '20':  about_menu()
        else:
            print(f"\n{R}[!] Invalid option!{RS}")
            time.sleep(1)

# ────────────────────────────────────────────────────────
# Sub-menus (remaining modules)
# ────────────────────────────────────────────────────────
def network_scanner_menu():
    show_banner()
    print(f"{B}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}Network Scanner & Analysis{R}                          {B}║")
    print(f"╠═══════════════════════════════════════════════════════╣")
    print(f"║  {W}[1]{R}  ARP Scan - Discover Live Hosts                  {B}║")
    print(f"║  {W}[2]{R}  Port Scan (TCP/UDP)                            {B}║")
    print(f"║  {W}[3]{R}  Service Version Detection                      {B}║")
    print(f"║  {W}[4]{R}  OS Fingerprinting                              {B}║")
    print(f"║  {W}[5]{R}  Network Mapping (Topology)                     {B}║")
    print(f"║  {W}[6]{R}  Bandwidth & Latency Test                       {B}║")
    print(f"║  {W}[0]{R}  Back to Main Menu                              {B}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    choice = input(f"\n{Y}  A2Tool[Network] » {RS}").strip()
    if choice == '0': return
    utils.run_external_tool('nmap', choice, 'network')

def password_cracking_menu():
    show_banner()
    print(f"{M}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}Password Cracking & Hash Tools{R}                     {M}║")
    print(f"╠═══════════════════════════════════════════════════════╣")
    print(f"║  {W}[1]{R}  Brute Force - ZIP / RAR                        {M}║")
    print(f"║  {W}[2]{R}  Hashcat Wrapper                                {M}║")
    print(f"║  {W}[3]{R}  John the Ripper Wrapper                        {M}║")
    print(f"║  {W}[4]{R}  Wordlist Generator                             {M}║")
    print(f"║  {W}[5]{R}  Online Hash Lookup (CrackStation)             {M}║")
    print(f"║  {W}[6]{R}  PDF Password Cracker                           {M}║")
    print(f"║  {W}[0]{R}  Back to Main Menu                              {M}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    choice = input(f"\n{Y}  A2Tool[Crack] » {RS}").strip()
    if choice == '0': return
    utils.run_external_tool('hashcat' if choice in ['2'] else 'john', choice, 'crack')

def web_attack_menu():
    show_banner()
    print(f"{G}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}Web Application Attacks{R}                            {G}║")
    print(f"╠═══════════════════════════════════════════════════════╣")
    print(f"║  {W}[1]{R}  SQL Injection Scanner                          {G}║")
    print(f"║  {W}[2]{R}  XSS (Cross-Site Scripting)                    {G}║")
    print(f"║  {W}[3]{R}  LFI / RFI Scanner                             {G}║")
    print(f"║  {W}[4]{R}  Directory Bruteforce                          {G}║")
    print(f"║  {W}[5]{R}  Command Injection                             {G}║")
    print(f"║  {W}[6]{R}  CSRF Testing                                  {G}║")
    print(f"║  {W}[7]{R}  CMS Scanner (WordPress/Joomla/Drupal)         {G}║")
    print(f"║  {W}[8]{R}  Subdomain Enumeration                         {G}║")
    print(f"║  {W}[0]{R}  Back to Main Menu                              {G}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    choice = input(f"\n{Y}  A2Tool[Web] » {RS}").strip()
    if choice == '0': return
    utils.run_external_tool('sqlmap', choice, 'web')

def reverse_shell_menu():
    show_banner()
    print(f"{R}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}Reverse Shell & Backdoor Tools{R}                     {R}║")
    print(f"╠═══════════════════════════════════════════════════════╣")
    print(f"║  {W}[1]{R}  Netcat Listener Setup                          {R}║")
    print(f"║  {W}[2]{R}  PHP Reverse Shell Generator                   {R}║")
    print(f"║  {W}[3]{R}  Python Reverse Shell Generator                 {R}║")
    print(f"║  {W}[4]{R}  Bash Reverse Shell Generator                   {R}║")
    print(f"║  {W}[5]{R}  PowerShell Reverse Shell Generator             {R}║")
    print(f"║  {W}[6]{R}  Metasploit Multi/Handler Wrapper               {R}║")
    print(f"║  {W}[7]{R}  Bind Shell Generator                           {R}║")
    print(f"║  {W}[0]{R}  Back to Main Menu                              {R}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    choice = input(f"\n{Y}  A2Tool[Shell] » {RS}").strip()
    if choice == '0': return
    payloads.generate_reverse_shell(choice)

def ddos_menu():
    show_banner()
    print(f"{Y}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}DDoS / Stress Testing Tools{R}                        {Y}║")
    print(f"╠═══════════════════════════════════════════════════════╣")
    print(f"║  {W}[1]{R}  SYN Flood Attack                              {Y}║")
    print(f"║  {W}[2]{R}  UDP Flood Attack                              {Y}║")
    print(f"║  {W}[3]{R}  HTTP GET/POST Flood                           {Y}║")
    print(f"║  {W}[4]{R}  Slowloris (Slow HTTP Attack)                  {Y}║")
    print(f"║  {W}[5]{R}  ICMP (Ping of Death)                          {Y}║")
    print(f"║  {W}[6]{R}  DNS Amplification                             {Y}║")
    print(f"║  {W}[0]{R}  Back to Main Menu                              {Y}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    choice = input(f"\n{Y}  A2Tool[DDoS] » {RS}").strip()
    if choice == '0': return
    utils.run_external_tool('hping3', choice, 'ddos')

def bluetooth_menu():
    show_banner()
    print(f"{C}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}Bluetooth Hacking Tools{R}                            {C}║")
    print(f"╠═══════════════════════════════════════════════════════╣")
    print(f"║  {W}[1]{R}  Bluetooth Device Scan                          {C}║")
    print(f"║  {W}[2]{R}  Bluetooth Service Discovery                    {C}║")
    print(f"║  {W}[3]{R}  Bluetooth Spam / Flood                         {C}║")
    print(f"║  {W}[4]{R}  Bluetooth MAC Spoofing                         {C}║")
    print(f"║  {W}[5]{R}  Bluetooth Pairing Attack                       {C}║")
    print(f"║  {W}[0]{R}  Back to Main Menu                              {C}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    choice = input(f"\n{Y}  A2Tool[BT] » {RS}").strip()
    if choice == '0': return
    utils.run_external_tool('bluetoothctl', choice, 'bluetooth')

def camera_mic_menu():
    show_banner()
    print(f"{M}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}Camera / Mic Exploitation{R}                          {M}║")
    print(f"╠═══════════════════════════════════════════════════════╣")
    print(f"║  {W}[1]{R}  Webcam Snapshot (Local)                      {M}║")
    print(f"║  {W}[2]{R}  Microphone Record (Local)                    {M}║")
    print(f"║  {W}[3]{R}  Remote Camera Access (via RAT)               {M}║")
    print(f"║  {W}[4]{R}  IP Camera Scanner (Default Creds)            {M}║")
    print(f"║  {W}[5]{R}  Screen Capture                               {M}║")
    print(f"║  {W}[0]{R}  Back to Main Menu                            {M}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    choice = input(f"\n{Y}  A2Tool[Cam] » {RS}").strip()
    if choice == '0': return
    payloads.camera_exploit(choice)

def keylogger_menu():
    show_banner()
    print(f"{R}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}Keylogger & Spyware Tools{R}                          {R}║")
    print(f"╠═══════════════════════════════════════════════════════╣")
    print(f"║  {W}[1]{R}  Python Keylogger (Local Demo)                {R}║")
    print(f"║  {W}[2]{R}  Email Exfiltration Keylogger                  {R}║")
    print(f"║  {W}[3]{R}  FTP Exfiltration Keylogger                    {R}║")
    print(f"║  {W}[4]{R}  Clipboard Logger                              {R}║")
    print(f"║  {W}[5]{R}  Browser Credential Dumper                     {R}║")
    print(f"║  {W}[6]{R}  Screen Activity Recorder                      {R}║")
    print(f"║  {W}[0]{R}  Back to Main Menu                            {R}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    choice = input(f"\n{Y}  A2Tool[Key] » {RS}").strip()
    if choice == '0': return
    payloads.keylogger_tool(choice)

def vpn_proxy_menu():
    show_banner()
    print(f"{G}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}VPN & Proxy Chaining{R}                               {G}║")
    print(f"╠═══════════════════════════════════════════════════════╣")
    print(f"║  {W}[1]{R}  Proxy List Scraper                            {G}║")
    print(f"║  {W}[2]{R}  Proxy Chain Tester                            {G}║")
    print(f"║  {W}[3]{R}  Tor Integration (Anonymize)                   {G}║")
    print(f"║  {W}[4]{R}  VPN Auto-Connect                              {G}║")
    print(f"║  {W}[5]{R}  DNS Leak Test                                 {G}║")
    print(f"║  {W}[6]{R}  Mac Changer                                   {G}║")
    print(f"║  {W}[0]{R}  Back to Main Menu                            {G}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    choice = input(f"\n{Y}  A2Tool[Proxy] » {RS}").strip()
    if choice == '0': return
    utils.run_external_tool('tor', choice, 'proxy')

def stego_menu():
    show_banner()
    print(f"{C}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}Steganography Tools{R}                                {C}║")
    print(f"╠═══════════════════════════════════════════════════════╣")
    print(f"║  {W}[1]{R}  Image Steganography (Hide Data in Image)     {C}║")
    print(f"║  {W}[2]{R}  Audio Steganography                           {C}║")
    print(f"║  {W}[3]{R}  Video Steganography                           {C}║")
    print(f"║  {W}[4]{R}  Extract Hidden Data from Image                {C}║")
    print(f"║  {W}[5]{R}  Metadata Viewer (EXIF)                       {C}║")
    print(f"║  {W}[0]{R}  Back to Main Menu                            {C}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    choice = input(f"\n{Y}  A2Tool[Stego] » {RS}").strip()
    if choice == '0': return
    utils.run_external_tool('steghide', choice, 'stego')

def forensic_menu():
    show_banner()
    print(f"{M}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}Forensic & Anti-Forensic Tools{R}                    {M}║")
    print(f"╠═══════════════════════════════════════════════════════╣")
    print(f"║  {W}[1]{R}  Disk / Partition Analysis                     {M}║")
    print(f"║  {W}[2]{R}  Recover Deleted Files                         {M}║")
    print(f"║  {W}[3]{R}  Memory Dump Analysis                          {M}║")
    print(f"║  {W}[4]{R}  Log Wiping                                    {M}║")
    print(f"║  {W}[5]{R}  File Shredder (Secure Delete)                 {M}║")
    print(f"║  {W}[6]{R}  Timestamp Manipulation                        {M}║")
    print(f"║  {W}[0]{R}  Back to Main Menu                            {M}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    choice = input(f"\n{Y}  A2Tool[Forensic] » {RS}").strip()
    if choice == '0': return
    utils.run_external_tool('foremost', choice, 'forensic')

def crypto_menu():
    show_banner()
    print(f"{Y}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}Cryptography & Encryption Tools{R}                   {Y}║")
    print(f"╠═══════════════════════════════════════════════════════╣")
    print(f"║  {W}[1]{R}  AES Encrypt / Decrypt File                    {Y}║")
    print(f"║  {W}[2]{R}  RSA Key Pair Generator                        {Y}║")
    print(f"║  {W}[3]{R}  Base64 / Hex / ASCII Converter                {Y}║")
    print(f"║  {W}[4]{R}  Hash Generator (MD5/SHA1/SHA256)             {Y}║")
    print(f"║  {W}[5]{R}  Caesar / Vigenere Cipher                     {Y}║")
    print(f"║  {W}[6]{R}  XOR Encryption                                {Y}║")
    print(f"║  {W}[0]{R}  Back to Main Menu                            {Y}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    choice = input(f"\n{Y}  A2Tool[Crypto] » {RS}").strip()
    if choice == '0': return
    payloads.crypto_tools(choice)

def vuln_scan_menu():
    show_banner()
    print(f"{R}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}System Info & Vulnerability Scanner{R}               {R}║")
    print(f"╠═══════════════════════════════════════════════════════╣")
    print(f"║  {W}[1]{R}  System Information Dump                        {R}║")
    print(f"║  {W}[2]{R}  Running Services & Ports                       {R}║")
    print(f"║  {W}[3]{R}  Installed Software Audit                       {R}║")
    print(f"║  {W}[4]{R}  CVE Database Lookup                            {R}║")
    print(f"║  {W}[5]{R}  Open Vulnerability Scanner (Local)             {R}║")
    print(f"║  {W}[6]{R}  SUID / SGID / Sticky Bit Check                {R}║")
    print(f"║  {W}[0]{R}  Back to Main Menu                            {R}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    choice = input(f"\n{Y}  A2Tool[Vuln] » {RS}").strip()
    if choice == '0': return
    utils.system_info_dump(choice)

def about_menu():
    show_banner()
    print(f"""{G}
  ╔═══════════════════════════════════════════════════════╗
  ║  {W}A2Tool v3.0{R} - Advanced All-in-One Penetration      ║
  ║  {W}Testing Suite{R}                                       ║
  ║                                                       ║
  ║  {C}Created by:{R}  Ayush Rajdev & Anzar Iqbal              ║
  ║  {C}Version:{R}    3.0 (Zero to Hero)                      ║
  ║  {C}Platform:{R}   Windows, Linux, macOS, Android           ║
  ║  {C}Language:{R}   Python 3                                ║
  ║                                                       ║
  ║  {Y}Features:{R}                                            ║
  ║  - WiFi Password Recovery (All OS)                     ║
  ║  - Phishing & Social Engineering Framework             ║
  ║  - 50+ Hacking Modules & Techniques                    ║
  ║  - Payload Generation (All Platforms)                  ║
  ║  - Network Scanning & Exploitation                     ║
  ║  - Web Application Security Testing                    ║
  ║  - Reverse Shell & Backdoor Tools                      ║
  ║                                                       ║
  ║  {R}[!] For educational purposes only.{R}                   ║
  ║  {R}[!] Use only on systems you own or have permission.{R} ║
  ║                                                       ║
  ║  {G}Press Enter to return to main menu...{RS}                  ║
  ╚═══════════════════════════════════════════════════════╝
{RS}""")
    input()

# ────────────────────────────────────────────────────────
# Entry point
# ────────────────────────────────────────────────────────
if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Interrupted. Exiting...{RS}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{R}[!] Error: {e}{RS}")
        sys.exit(1)
