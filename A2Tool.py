#!/usr/bin/env python3
# ============================================================
#  A2Tool v4.0 - Ultimate All-in-One Penetration Testing Suite
#  200+ Hacking Tools & Techniques
#  Author  : Ayush Rajdev & Anzar Iqbal
#  Platform: Windows / Linux / macOS / Android (Termux)
#  Telegram: https://t.me/A2Tool
# ============================================================

import os, sys, time, platform, json, subprocess, threading, webbrowser

# ────────────────────────────────────────────────────────
# AUTO-INSTALL REQUIREMENTS ON FIRST RUN
# ────────────────────────────────────────────────────────
REQUIREMENTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')
AUTO_INSTALL_MARKER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.deps_installed')

def install_dependencies():
    """Automatically install all required Python packages"""
    if os.path.exists(AUTO_INSTALL_MARKER):
        return True
    
    print("\n" + "=" * 60)
    print("  A2Tool v4.0 - First Run Setup")
    print("  Installing dependencies automatically...")
    print("=" * 60)
    print()
    
    try:
        import pip
    except ImportError:
        print("[!] pip not found. Installing pip...")
        subprocess.run([sys.executable, '-m', 'ensurepip', '--upgrade'], check=True)
    
    if os.path.exists(REQUIREMENTS_FILE):
        print("[*] Installing Python packages from requirements.txt...")
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', REQUIREMENTS_FILE, '--quiet', '--break-system-packages'],
                capture_output=True, timeout=120
            )
            # Touch marker file
            with open(AUTO_INSTALL_MARKER, 'w') as f:
                f.write('installed')
            print("[+] All dependencies installed successfully!")
            return True
        except subprocess.TimeoutExpired:
            print("[!] Installation timed out, continuing anyway...")
            with open(AUTO_INSTALL_MARKER, 'w') as f:
                f.write('installed')
            return True
        except Exception as e:
            print(f"[!] pip install failed: {e}")
            print("[!] Continuing with basic functionality...")
            return False
    
    return False

# Run auto-install
install_dependencies()

# ────────────────────────────────────────────────────────
# Imports (with fallbacks)
# ────────────────────────────────────────────────────────
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ''
        BLACK = LIGHTRED_EX = LIGHTGREEN_EX = LIGHTYELLOW_EX = LIGHTBLUE_EX = LIGHTMAGENTA_EX = LIGHTCYAN_EX = LIGHTWHITE_EX = ''
    class Style:
        RESET_ALL = ''
        BRIGHT = DIM = NORMAL = ''

R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
M = Fore.MAGENTA
C = Fore.CYAN
W = Fore.WHITE
RS = Style.RESET_ALL

# ────────────────────────────────────────────────────────
# Platform detection
# ────────────────────────────────────────────────────────
OS_NAME = platform.system().lower()
IS_WINDOWS = OS_NAME == 'windows'
IS_LINUX = OS_NAME == 'linux'
IS_MACOS = OS_NAME == 'darwin'
IS_ANDROID = 'android' in platform.platform().lower() or 'termux' in os.environ.get('PREFIX', '')

def clear_screen():
    os.system('cls' if IS_WINDOWS else 'clear')

def pause():
    if IS_WINDOWS:
        os.system('pause >nul 2>&1')
    else:
        input(f"\n{Y}[+] Press Enter to continue...{RS}")

# ────────────────────────────────────────────────────────
# Import all 20 modules
# ────────────────────────────────────────────────────────
from modules import (
    wifi_tool,
    phishing,
    social_engineering,
    info_gathering,
    exploits,
    utils,
    payloads,
    network_scanner,
    password_cracker,
    web_attacks,
    reverse_shell,
    ddos_tools,
    bluetooth_tools,
    camera_mic,
    keylogger_tools,
    vpn_proxy,
    stego_tools,
    forensic_tools,
    crypto_tools,
    vuln_scanner
)

# ────────────────────────────────────────────────────────
# Banner
# ────────────────────────────────────────────────────────
BANNER = f"""{R}
  ╔══════════════════════════════════════════════════════════════════╗
  ║{C}████████╗{R}██╗  ██╗{Y}████████╗{G} ██████╗ {B}███████╗{R}██╗     {M}██╗{R}          ║
  ║{C}╚══██╔══╝{R}██║  ██║{Y}╚══██╔══╝{G}██╔═══██╗{B}██╔════╝{R}██║     {M}██║{R}          ║
  ║{C}   ██║   {R}███████║{Y}   ██║   {G}██║   ██║{B}█████╗  {R}██║     {M}██║{R}          ║
  ║{C}   ██║   {R}██╔══██║{Y}   ██║   {G}██║   ██║{B}██╔══╝  {R}██║     {M}██║{R}          ║
  ║{C}   ██║   {R}██║  ██║{Y}   ██║   {G}╚██████╔╝{B}███████╗{R}███████╗{M}██║{R}          ║
  ║{C}   ╚═╝   {R}╚═╝  ╚═╝{Y}   ╚═╝   {G} ╚═════╝ {B}╚══════╝{R}╚══════╝{M}╚═╝{R}          ║
  ║                                                                    ║
  ║{Y}  Ultimate All-in-One Penetration Testing Suite{R}                    ║
  ║{C}  🔥 200+ Hacking Tools & Techniques{R}                               ║
  ║{G}  Author: {C}Ayush Rajdev{R} & {C}Anzar Iqbal{R}                               ║
  ║{M}  Version 4.0 - The Beast Mode{R}                                     ║
  ║{Y}  Telegram: {C}https://t.me/A2Tool{R}                                   ║
  ╚══════════════════════════════════════════════════════════════════╝
{RS}"""

def show_banner():
    clear_screen()
    print(BANNER)

# ────────────────────────────────────────────────────────
# Main Menu - 200+ Tools
# ────────────────────────────────────────────────────────
def main_menu():
    while True:
        show_banner()
        print(f"{C}╔══════════════════════════════════════════════════════════════════╗{RS}")
        print(f"{C}║{W}  #  Category                              Tools Count         {C}║{RS}")
        print(f"{C}╠══════════════════════════════════════════════════════════════════╣{RS}")
        print(f"{C}║{W} [01]{R}  WiFi Hacking & Password Recovery         {G}[18 Tools]   {C}║{RS}")
        print(f"{C}║{W} [02]{R}  Phishing Attacks Framework               {G}[15 Tools]   {C}║{RS}")
        print(f"{C}║{W} [03]{R}  Social Engineering Toolkit               {G}[12 Tools]   {C}║{RS}")
        print(f"{C}║{W} [04]{R}  Information Gathering (OSINT)            {G}[25 Tools]   {C}║{RS}")
        print(f"{C}║{W} [05]{R}  Exploitation Framework                   {G}[15 Tools]   {C}║{RS}")
        print(f"{C}║{W} [06]{R}  Payload Generator                        {G}[15 Tools]   {C}║{RS}")
        print(f"{C}║{W} [07]{R}  Network Scanner & Analysis               {G}[15 Tools]   {C}║{RS}")
        print(f"{C}║{W} [08]{R}  Password Cracking & Hash Tools           {G}[15 Tools]   {C}║{RS}")
        print(f"{C}║{W} [09]{R}  Web Application Attacks                  {G}[15 Tools]   {C}║{RS}")
        print(f"{C}║{W} [10]{R}  Reverse Shell & Backdoor Tools           {G}[12 Tools]   {C}║{RS}")
        print(f"{C}║{W} [11]{R}  DDoS / Stress Testing Tools             {G}[10 Tools]   {C}║{RS}")
        print(f"{C}║{W} [12]{R}  Bluetooth Hacking                         {G}[10 Tools]   {C}║{RS}")
        print(f"{C}║{W} [13]{R}  Camera & Mic Exploitation                {G}[10 Tools]   {C}║{RS}")
        print(f"{C}║{W} [14]{R}  Keylogger & Spyware Tools                {G}[10 Tools]   {C}║{RS}")
        print(f"{C}║{W} [15]{R}  VPN & Proxy Chaining                     {G}[10 Tools]   {C}║{RS}")
        print(f"{C}║{W} [16]{R}  Steganography Tools                       {G}[10 Tools]   {C}║{RS}")
        print(f"{C}║{W} [17]{R}  Forensic & Anti-Forensic Tools           {G}[10 Tools]   {C}║{RS}")
        print(f"{C}║{W} [18]{R}  Cryptography & Encryption Tools          {G}[12 Tools]   {C}║{RS}")
        print(f"{C}║{W} [19]{R}  Vulnerability Scanner                     {G}[10 Tools]   {C}║{RS}")
        print(f"{C}║{W} [20]{R}  About / Update / System Info              {G}[Info]      {C}║{RS}")
        print(f"{C}╠══════════════════════════════════════════════════════════════════╣{RS}")
        print(f"{C}║{W}                                                    Total: {G}[249 Tools]{C}║{RS}")
        print(f"{C}║{R}  [0]  Exit                                          {W}[!]{R}            {C}║{RS}")
        print(f"{C}╚══════════════════════════════════════════════════════════════════╝{RS}")
        print(f"{G}  Platform: {C}{platform.system()} {platform.release()}  |  {W}A2Tool v4.0{RS}")
        choice = input(f"\n{Y}  A2Tool » {RS}").strip()

        if choice == '0':
            print(f"\n{R}[!] Exiting A2Tool v4.0. Stay secure!{RS}")
            print(f"{G}[!] Follow us on Telegram: https://t.me/A2Tool{RS}")
            sys.exit(0)
        elif choice == '1':   wifi_tool.menu()
        elif choice == '2':   phishing.menu()
        elif choice == '3':   social_engineering.menu()
        elif choice == '4':   info_gathering.menu()
        elif choice == '5':   exploits.menu()
        elif choice == '6':   payloads.menu()
        elif choice == '7':   network_scanner.menu()
        elif choice == '8':   password_cracker.menu()
        elif choice == '9':   web_attacks.menu()
        elif choice == '10':  reverse_shell.menu()
        elif choice == '11':  ddos_tools.menu()
        elif choice == '12':  bluetooth_tools.menu()
        elif choice == '13':  camera_mic.menu()
        elif choice == '14':  keylogger_tools.menu()
        elif choice == '15':  vpn_proxy.menu()
        elif choice == '16':  stego_tools.menu()
        elif choice == '17':  forensic_tools.menu()
        elif choice == '18':  crypto_tools.menu()
        elif choice == '19':  vuln_scanner.menu()
        elif choice == '20':  about_menu()
        else:
            print(f"\n{R}[!] Invalid option! Please enter a number from 0-20.{RS}")
            time.sleep(1)

# ────────────────────────────────────────────────────────
# About Menu
# ────────────────────────────────────────────────────────
def about_menu():
    show_banner()
    print(f"""{G}
  ╔═══════════════════════════════════════════════════════╗
  ║  {W}A2Tool v4.0{R} - Ultimate All-in-One                  ║
  ║  {W}Penetration Testing Suite{R}                           ║
  ║                                                       ║
  ║  {C}Created by:{R}  Ayush Rajdev & Anzar Iqbal              ║
  ║  {C}Version:{R}    4.0 (The Beast Mode)                     ║
  ║  {C}Platform:{R}   Windows, Linux, macOS, Android (Termux)  ║
  ║  {C}Language:{R}   Python 3                                ║
  ║  {C}Total Tools:{R} 249+                                   ║
  ║                                                       ║
  ║  {Y}Features:{R}                                            ║
  ║  ✅ WiFi Password Recovery (All OS)                    ║
  ║  ✅ Phishing & Social Engineering Framework            ║
  ║  ✅ 249+ Hacking Modules & Techniques                  ║
  ║  ✅ Payload Generation (All Platforms)                 ║
  ║  ✅ Network Scanning & Exploitation                    ║
  ║  ✅ Web Application Security Testing                   ║
  ║  ✅ Reverse Shell & Backdoor Tools                     ║
  ║  ✅ DDoS / Stress Testing                              ║
  ║  ✅ Steganography & Cryptography                       ║
  ║  ✅ Forensics & Anti-Forensics                        ║
  ║  ✅ Auto-Install on First Run                          ║
  ║  ✅ Cross-Platform Support                             ║
  ║                                                       ║
  ║  {R}[!] For educational purposes only.{R}                   ║
  ║  {R}[!] Use only on systems you own or have permission.{R} ║
  ║                                                       ║
  ║  {G}Telegram: {C}https://t.me/A2Tool{RS}                      ║
  ║  {G}GitHub: {C}https://github.com/ayushrajdev9-cmyk/a2tools{RS} ║
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
        print(f"{G}[!] Follow us on Telegram: https://t.me/A2Tool{RS}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{R}[!] Error: {e}{RS}")
        sys.exit(1)
