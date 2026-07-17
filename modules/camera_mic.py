#!/usr/bin/env python3
"""
A2Tool v4.0 - Camera & Mic Exploitation Module (10 Tools)
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
        print(f"\n{M}╔══════════════════════════════════════════════════════════════╗{RS}")
        print(f"{M}║{W}           Camera & Microphone Exploitation                 {M}║{RS}")
        print(f"{M}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{M}║{W} [01]{R}  Webcam Snapshot (Local)                           {M}║{RS}")
        print(f"{M}║{W} [02]{R}  Webcam Stream (Local)                             {M}║{RS}")
        print(f"{M}║{W} [03]{R}  Microphone Record (Local)                         {M}║{RS}")
        print(f"{M}║{W} [04]{R}  IP Camera Scanner (Default Creds)                 {M}║{RS}")
        print(f"{M}║{W} [05]{R}  Remote Camera Access (Via RAT)                    {M}║{RS}")
        print(f"{M}║{W} [06]{R}  Screen Capture                                    {M}║{RS}")
        print(f"{M}║{W} [07]{R}  Webcam Loopback Exploit                           {M}║{RS}")
        print(f"{M}║{W} [08]{R}  Audio Spy (Live Mic Monitor)                      {M}║{RS}")
        print(f"{M}║{W} [09]{R}  Camera Recording (Video Capture)                  {M}║{RS}")
        print(f"{M}║{W} [10]{R}  Motion Detection Setup                            {M}║{RS}")
        print(f"{M}║{W} [0]{R}   Back to Main Menu                                  {M}║{RS}")
        print(f"{M}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[CamMic] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': cam_snapshot()
        elif ch == '2': cam_stream()
        elif ch == '3': mic_record()
        elif ch == '4': ip_cam_scan()
        elif ch == '5': remote_cam()
        elif ch == '6': screen_capture()
        elif ch == '7': webcam_loopback()
        elif ch == '8': audio_spy()
        elif ch == '9': cam_record()
        elif ch == '10': motion_detect()
        else: print(f"{R}[!] Invalid option{RS}")

def cam_snapshot():
    print(f"\n{G}[+] Capturing webcam snapshot...{RS}")
    try:
        import cv2
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            print(f"{R}[-] Cannot access webcam{RS}")
            input(f"\n{Y}[+] Press Enter to continue...{RS}")
            return
        ret, frame = cam.read()
        if ret:
            fname = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(fname, frame)
            print(f"{G}[+] Snapshot saved: {fname}{RS}")
        else:
            print(f"{R}[-] Failed to capture image{RS}")
        cam.release()
    except ImportError:
        print(f"{Y}[!] OpenCV not installed. Install: pip install opencv-python{RS}")
        print(f"{Y}[!] On Linux: fswebcam snapshot.jpg{RS}")
        os.system('fswebcam snapshot.jpg 2>/dev/null')
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def cam_stream():
    print(f"\n{G}[+] Starting webcam stream (press 'q' to quit)...{RS}")
    try:
        import cv2
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            print(f"{R}[-] Cannot access webcam{RS}")
            input(f"\n{Y}[+] Press Enter to continue...{RS}")
            return
        while True:
            ret, frame = cam.read()
            if not ret: break
            cv2.imshow('A2Tool Webcam Stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cam.release()
        cv2.destroyAllWindows()
    except ImportError:
        print(f"{Y}[!] OpenCV not installed{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def mic_record():
    print(f"\n{G}[+] Microphone Recorder{RS}")
    duration = int(input(f"  {W}[?] Recording duration (seconds): {RS}").strip() or '5')
    
    try:
        import sounddevice as sd
        import soundfile as sf
        import numpy as np
        
        print(f"{Y}[!] Recording for {duration} seconds...{RS}")
        fs = 44100
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        
        fname = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        sf.write(fname, recording, fs)
        print(f"{G}[+] Recording saved: {fname}{RS}")
    except ImportError:
        print(f"{Y}[!] Install: pip install sounddevice soundfile{RS}")
        print(f"{Y}[!] On Linux: arecord -d {duration} -f cd recording.wav{RS}")
        os.system(f'arecord -d {duration} -f cd recording.wav 2>/dev/null')
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def ip_cam_scan():
    print(f"\n{G}[+] IP Camera Scanner (Default Credentials){RS}")
    subnet = input(f"  {W}[?] Subnet to scan (e.g., 192.168.1.0/24): {RS}").strip() or '192.168.1.0/24'
    
    print(f"{Y}[!] Scanning {subnet} for IP cameras...{RS}")
    out = _run(f'nmap -p 80,554,8080,37777,34567 --open {subnet} -oG - 2>/dev/null')
    if out:
        ips = re.findall(r'Host: (\S+)', out)
        for ip in ips:
            print(f"  {G}[+]{RS} {C}{ip}{RS} - {Y}Camera port open{RS}")
            # Check default creds
            print(f"    {W}Try:{RS} admin/admin, admin/12345, admin/1111, root/vizxv")
    else:
        print(f"{Y}[-] nmap not found or no cameras detected{RS}")
        print(f"{Y}[!] Install nmap for better scanning{RS}")
    
    print(f"\n{W}Common default credentials:{RS}")
    print(f"  {W}•{RS} admin:admin (Hikvision, Dahua)")
    print(f"  {W}•{RS} admin:12345 (D-Link)")
    print(f"  {W}•{RS} admin: (Foscam)")
    print(f"  {W}•{RS} root:vizxv (Various Chinese cams)")
    print(f"  {W}•{RS} admin:1111 (Trendnet)")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def remote_cam():
    print(f"\n{Y}[!] Remote Camera Access Guide{RS}")
    target = input(f"  {W}[?] Target IP: {RS}").strip()
    print(f"\n{W}Remote camera access methods:{RS}")
    print(f"  1. IP Camera - http://{target}:80")
    print(f"  2. RTSP Stream - rtsp://{target}:554/stream")
    print(f"  3. MJPG Stream - http://{target}:8080/?action=stream")
    print(f"  4. VLC: vlc rtsp://{target}:554/stream")
    print(f"  5. FFmpeg: ffplay rtsp://{target}:554/stream")
    
    if input(f"\n{Y}[?] Attempt to open in browser? (y/n): {RS}").strip().lower() == 'y':
        import webbrowser
        webbrowser.open(f'http://{target}')
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def screen_capture():
    print(f"\n{G}[+] Screen Capture Tool{RS}")
    try:
        import mss
        with mss.mss() as sct:
            fname = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            sct.shot(output=fname)
            print(f"{G}[+] Screenshot saved: {fname}{RS}")
            
            if input(f"{Y}[?] Show display info? (y/n): {RS}").strip().lower() == 'y':
                for i, m in enumerate(sct.monitors):
                    print(f"  {W}Monitor {i}:{RS} {m}")
    except ImportError:
        print(f"{Y}[!] Install mss: pip install mss{RS}")
        # Fallback
        if os.name == 'nt':
            os.system('powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait(\'{PRTSC}\')"')
        else:
            os.system('gnome-screenshot -f screenshot.png 2>/dev/null || import -window root screenshot.png 2>/dev/null')
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def webcam_loopback():
    print(f"\n{Y}[!] Webcam Loopback Exploit (Virtual Camera){RS}")
    print(f"{W}This creates a virtual camera that feeds controlled video{RS}")
    print(f"\n{W}Using OBS Virtual Camera:{RS}")
    print(f"  1. Install OBS Studio")
    print(f"  2. Install obs-virtual-cam plugin")
    print(f"  3. Start OBS with custom scene")
    print(f"  4. Tools → Virtual Cam → Start")
    
    print(f"\n{W}Using v4l2loopback (Linux):{RS}")
    print(f"  sudo modprobe v4l2loopback")
    print(f"  ffmpeg -re -i input.mp4 -f v4l2 /dev/video1")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def audio_spy():
    print(f"\n{G}[+] Live Audio Monitor (Audio Spy){RS}")
    duration = int(input(f"  {W}[?] Monitor duration (seconds, 0=continuous): {RS}").strip() or '10')
    
    def monitor():
        try:
            import sounddevice as sd
            import numpy as np
            print(f"{Y}[!] Listening... (speak to see audio levels){RS}")
            
            def callback(indata, frames, time, status):
                level = np.linalg.norm(indata) * 10
                bars = '█' * int(min(level, 50)) + '░' * max(0, 50 - int(min(level, 50)))
                print(f"\r  {G}[{bars}]{RS} Level: {level:.1f}", end='')
            
            with sd.InputStream(callback=callback):
                if duration > 0:
                    sd.sleep(duration * 1000)
                else:
                    input(f"\n{Y}[!] Press Enter to stop{RS}")
        except ImportError:
            print(f"{Y}[!] Install: pip install sounddevice numpy{RS}")
        except Exception as e:
            print(f"{R}[-] Error: {e}{RS}")
    
    monitor()
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def cam_record():
    print(f"\n{G}[+] Video Recording (Webcam){RS}")
    duration = int(input(f"  {W}[?] Recording duration (seconds): {RS}").strip() or '10')
    
    try:
        import cv2
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            print(f"{R}[-] Cannot access webcam{RS}")
            input(f"\n{Y}[+] Press Enter to continue...{RS}")
            return
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fname = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
        out = cv2.VideoWriter(fname, fourcc, 20.0, (640, 480))
        
        print(f"{Y}[!] Recording for {duration}s...{RS}")
        start = time.time()
        while time.time() - start < duration:
            ret, frame = cam.read()
            if ret:
                out.write(frame)
        
        cam.release()
        out.release()
        print(f"{G}[+] Video saved: {fname}{RS}")
    except ImportError:
        print(f"{Y}[!] OpenCV not installed{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def motion_detect():
    print(f"\n{G}[+] Motion Detection System{RS}")
    threshold = int(input(f"  {W}[?] Sensitivity (1-100, default 25): {RS}").strip() or '25')
    
    try:
        import cv2
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            print(f"{R}[-] Cannot access webcam{RS}")
            input(f"\n{Y}[+] Press Enter to continue...{RS}")
            return
        
        ret, frame1 = cam.read()
        ret, frame2 = cam.read()
        
        print(f"{Y}[!] Motion detection active. Press 'q' to quit.{RS}")
        motion_count = 0
        
        while True:
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            _, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                if cv2.contourArea(contour) < 5000:
                    continue
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                motion_count += 1
                if motion_count > 5:
                    fname = f"motion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    cv2.imwrite(fname, frame1)
                    print(f"  {G}[!]{RS} Motion detected! Saved {fname}")
                    motion_count = 0
            
            cv2.imshow('A2Tool Motion Detection', frame1)
            frame1 = frame2
            ret, frame2 = cam.read()
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cam.release()
        cv2.destroyAllWindows()
    except ImportError:
        print(f"{Y}[!] OpenCV not installed{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
