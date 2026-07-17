#!/usr/bin/env python3
"""
A2Tool v4.0 - Password Cracking & Hash Tools Module (15 Tools)
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time, hashlib, base64, binascii, random, string
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
        print(f"{M}║{W}          Password Cracking & Hash Tools Suite              {M}║{RS}")
        print(f"{M}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{M}║{W} [01]{R}  Hash Identifier                                   {M}║{RS}")
        print(f"{M}║{W} [02]{R}  MD5 Hash Cracker                                  {M}║{RS}")
        print(f"{M}║{W} [03]{R}  SHA-1/256/512 Hash Cracker                        {M}║{RS}")
        print(f"{M}║{W} [04]{R}  NTLM Hash Cracker                                 {M}║{RS}")
        print(f"{M}║{W} [05]{R}  bcrypt Hash Cracker                               {M}║{RS}")
        print(f"{M}║{W} [06]{R}  ZIP/RAR Password Cracker                          {M}║{RS}")
        print(f"{M}║{W} [07]{R}  PDF Password Cracker                              {M}║{RS}")
        print(f"{M}║{W} [08]{R}  Wordlist Generator (Custom)                       {M}║{RS}")
        print(f"{M}║{W} [09]{R}  Online Hash Lookup (API)                          {M}║{RS}")
        print(f"{M}║{W} [10]{R}  Password Strength Analyzer                        {M}║{RS}")
        print(f"{M}║{W} [11]{R}  Brute Force Attack (Local)                        {M}║{RS}")
        print(f"{M}║{W} [12]{R}  Rainbow Table Generator                           {M}║{RS}")
        print(f"{M}║{W} [13]{R}  Hashcat Wrapper                                   {M}║{RS}")
        print(f"{M}║{W} [14]{R}  John the Ripper Wrapper                           {M}║{RS}")
        print(f"{M}║{W} [15]{R}  Credential Stuffing Check                         {M}║{RS}")
        print(f"{M}║{W} [0]{R}   Back to Main Menu                                  {M}║{RS}")
        print(f"{M}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[Crack] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': hash_identifier()
        elif ch == '2': md5_crack()
        elif ch == '3': sha_crack()
        elif ch == '4': ntlm_crack()
        elif ch == '5': bcrypt_crack()
        elif ch == '6': zip_crack()
        elif ch == '7': pdf_crack()
        elif ch == '8': wordlist_gen()
        elif ch == '9': online_hash_lookup()
        elif ch == '10': password_strength()
        elif ch == '11': brute_force()
        elif ch == '12': rainbow_table()
        elif ch == '13': hashcat_wrapper()
        elif ch == '14': john_wrapper()
        elif ch == '15': cred_stuffing()
        else: print(f"{R}[!] Invalid option{RS}")

def hash_identifier():
    """Tool 1: Hash Identifier"""
    hash_str = input(f"  {W}[?] Enter hash to identify: {RS}").strip()
    
    print(f"\n{G}[+] Analyzing hash: {Y}{hash_str}{RS}\n")
    
    length = len(hash_str)
    print(f"  {C}Length:{RS} {length} characters")
    print(f"  {C}Format:{RS} {'Hex' if all(c in '0123456789abcdefABCDEF' for c in hash_str) else 'Alphanumeric/Other'}")
    
    # Hash identification rules
    identifications = []
    
    if length == 32 and all(c in '0123456789abcdef' for c in hash_str.lower()):
        identifications.append("MD5")
    if length == 40 and all(c in '0123456789abcdef' for c in hash_str.lower()):
        identifications.append("SHA-1 / SHA-160")
    if length == 16 and all(c in '0123456789abcdef' for c in hash_str.lower()):
        identifications.append("MySQL v3.23 / NTLM")
    if length == 56 and all(c in '0123456789abcdef' for c in hash_str.lower()):
        identifications.append("SHA-224")
    if length == 64 and all(c in '0123456789abcdef' for c in hash_str.lower()):
        identifications.append("SHA-256")
    if length == 96 and all(c in '0123456789abcdef' for c in hash_str.lower()):
        identifications.append("SHA-384")
    if length == 128 and all(c in '0123456789abcdef' for c in hash_str.lower()):
        identifications.append("SHA-512")
    if hash_str.startswith('$2y$') or hash_str.startswith('$2a$') or hash_str.startswith('$2b$'):
        identifications.append("bcrypt ($2y$/$2a$/$2b$)")
    if hash_str.startswith('$5$'):
        identifications.append("SHA-256 Crypt")
    if hash_str.startswith('$6$'):
        identifications.append("SHA-512 Crypt")
    if hash_str.startswith('$1$'):
        identifications.append("MD5 Crypt")
    if ':' in hash_str and len(hash_str.split(':')[0]) == 32:
        identifications.append("NTLM (format: hash:username)")
    if len(hash_str) == 32 and hash_str.isupper():
        identifications.append("MD5 (uppercase) / NTLM")
    
    # Base64 check
    try:
        decoded = base64.b64decode(hash_str)
        if len(decoded) in [16, 20, 32, 64]:
            identifications.append(f"Base64 encoded ({len(decoded)} bytes)")
    except:
        pass
    
    if identifications:
        print(f"\n  {W}Possible hash types:{RS}")
        for i, ident in enumerate(identifications, 1):
            print(f"  {G}[{i}]{RS} {Y}{ident}{RS}")
    else:
        print(f"  {Y}[-] Unknown hash type{RS}")
    
    print(f"\n{W}Recommended hashcat mode:{RS}")
    hashcat_modes = {
        32: '0 (MD5)', 40: '100 (SHA1)', 56: '1300 (SHA2-224)', 
        64: '1400 (SHA2-256)', 96: '10800 (SHA2-384)', 128: '1700 (SHA2-512)'
    }
    mode = hashcat_modes.get(length, 'Unknown')
    print(f"  hashcat -m {mode}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def md5_crack():
    """Tool 2: MD5 Hash Cracker"""
    hash_str = input(f"  {W}[?] MD5 hash: {RS}").strip()
    wordlist = input(f"  {W}[?] Wordlist path (default: rockyou.txt): {RS}").strip() or 'rockyou.txt'
    
    print(f"\n{G}[+] Cracking MD5: {hash_str}{RS}")
    
    if not os.path.exists(wordlist):
        print(f"{Y}[-] Wordlist {wordlist} not found{RS}")
        print(f"{Y}[!] Use hashcat: hashcat -m 0 -a 0 {hash_str} {wordlist}{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    found = False
    try:
        with open(wordlist, 'r', errors='ignore') as f:
            for line in f:
                pwd = line.strip()
                if hashlib.md5(pwd.encode()).hexdigest() == hash_str.lower():
                    print(f"\n{G}[+] PASSWORD FOUND: {Y}{pwd}{RS}")
                    found = True
                    break
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    if not found:
        print(f"{Y}[-] Password not found in wordlist{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def sha_crack():
    """Tool 3: SHA Hash Cracker"""
    hash_str = input(f"  {W}[?] SHA hash: {RS}").strip()
    algo = input(f"  {W}[?] Algorithm (sha1/sha256/sha512): {RS}").strip() or 'sha256'
    wordlist = input(f"  {W}[?] Wordlist path: {RS}").strip() or 'rockyou.txt'
    
    print(f"\n{G}[+] Cracking {algo.upper()}: {hash_str}{RS}")
    
    if not os.path.exists(wordlist):
        print(f"{Y}[!] Use hashcat: hashcat -m {hashcat_modes[algo]} {hash_str} {wordlist}{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    hash_fn = hashlib.new(algo)
    
    try:
        with open(wordlist, 'r', errors='ignore') as f:
            for line in f:
                pwd = line.strip()
                h = hashlib.new(algo)
                h.update(pwd.encode())
                if h.hexdigest() == hash_str.lower():
                    print(f"\n{G}[+] PASSWORD FOUND: {Y}{pwd}{RS}")
                    break
            else:
                print(f"{Y}[-] Password not found in wordlist{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def ntlm_crack():
    """Tool 4: NTLM Hash Cracker"""
    hash_str = input(f"  {W}[?] NTLM hash: {RS}").strip()
    wordlist = input(f"  {W}[?] Wordlist path: {RS}").strip() or 'rockyou.txt'
    
    print(f"\n{G}[+] Cracking NTLM: {hash_str}{RS}")
    
    try:
        # Clean hash
        if ':' in hash_str:
            hash_str = hash_str.split(':')[1] if len(hash_str.split(':')) > 1 else hash_str.split(':')[0]
        hash_str = hash_str.strip().lower()
        
        if not os.path.exists(wordlist):
            print(f"{Y}[!] Use hashcat: hashcat -m 1000 -a 0 {hash_str} {wordlist}{RS}")
            input(f"\n{Y}[+] Press Enter to continue...{RS}")
            return
        
        with open(wordlist, 'r', errors='ignore') as f:
            for line in f:
                pwd = line.strip()
                ntlm = hashlib.new('md4', pwd.encode('utf-16le')).hexdigest()
                if ntlm == hash_str:
                    print(f"\n{G}[+] PASSWORD FOUND: {Y}{pwd}{RS}")
                    break
            else:
                print(f"{Y}[-] Password not found{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def bcrypt_crack():
    """Tool 5: bcrypt Hash Cracker"""
    hash_str = input(f"  {W}[?] bcrypt hash: {RS}").strip()
    wordlist = input(f"  {W}[?] Wordlist path: {RS}").strip() or 'rockyou.txt'
    
    print(f"\n{G}[+] Cracking bcrypt: {hash_str[:30]}...{RS}")
    print(f"{Y}[!] bcrypt is slow - use hashcat: hashcat -m 3200 -a 0 {hash_str} {wordlist}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def zip_crack():
    """Tool 6: ZIP/RAR Password Cracker"""
    zip_path = input(f"  {W}[?] Path to ZIP/RAR file: {RS}").strip()
    wordlist = input(f"  {W}[?] Wordlist path: {RS}").strip() or 'rockyou.txt'
    
    print(f"\n{G}[+] Cracking {zip_path}...{RS}")
    
    if zip_path.endswith('.zip'):
        cmd = f'fcrackzip -u -D -p {wordlist} {zip_path} 2>/dev/null || john {zip_path} --wordlist={wordlist} 2>/dev/null'
    elif zip_path.endswith('.rar'):
        cmd = f'rarcrack {zip_path} --wordlist {wordlist} 2>/dev/null'
    else:
        cmd = f'fcrackzip -u -D -p {wordlist} {zip_path} 2>/dev/null'
    
    out = _run(cmd)
    print(f"{Y}{out[:1000]}{RS}")
    
    print(f"\n{W}Alternative:{RS}")
    print(f"  zip2john {zip_path} > hash.txt && john hash.txt --wordlist={wordlist}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def pdf_crack():
    """Tool 7: PDF Password Cracker"""
    pdf_path = input(f"  {W}[?] Path to PDF file: {RS}").strip()
    wordlist = input(f"  {W}[?] Wordlist path: {RS}").strip() or 'rockyou.txt'
    
    print(f"\n{G}[+] Cracking PDF: {pdf_path}{RS}")
    
    print(f"{W}Using pdfcrack:{RS}")
    print(f"  pdfcrack -f {pdf_path} -w {wordlist}")
    
    print(f"\n{W}Using John:{RS}")
    print(f"  pdf2john {pdf_path} > pdf_hash.txt")
    print(f"  john pdf_hash.txt --wordlist={wordlist}")
    
    run_now = input(f"\n{Y}[?] Run pdfcrack now? (y/n): {RS}").strip().lower()
    if run_now == 'y':
        os.system(f'pdfcrack -f {pdf_path} -w {wordlist} 2>/dev/null')
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def wordlist_gen():
    """Tool 8: Wordlist Generator"""
    print(f"\n{G}[+] Custom Wordlist Generator{RS}")
    base_words = input(f"  {W}[?] Base words (comma-separated, e.g., admin,password): {RS}").strip()
    years = input(f"  {W}[?] Include years? (y/n): {RS}").strip().lower() == 'y'
    nums = input(f"  {W}[?] Include numbers 0-999? (y/n): {RS}").strip().lower() == 'y'
    special = input(f"  {W}[?] Include special chars? (!@#$): {RS}").strip().lower() == 'y'
    leet = input(f"  {W}[?] Include leet speak substitutions? (y/n): {RS}").strip().lower() == 'y'
    output = input(f"  {W}[?] Output filename (default: wordlist.txt): {RS}").strip() or 'wordlist.txt'
    
    words = [w.strip() for w in base_words.split(',') if w.strip()]
    
    print(f"\n{G}[+] Generating wordlist based on {len(words)} base words...{RS}")
    
    generated = set()
    
    for word in words:
        generated.add(word)
        generated.add(word.lower())
        generated.add(word.upper())
        generated.add(word.capitalize())
        
        if nums:
            for i in range(100):
                generated.add(f"{word}{i}")
                generated.add(f"{word}{i:02d}")
                generated.add(f"{word}{i:03d}")
        
        if years:
            for y in range(1980, 2030):
                generated.add(f"{word}{y}")
                generated.add(f"{word}{str(y)[2:]}")
        
        if special:
            for s in ['!', '@', '#', '$', '%', '&', '*']:
                generated.add(f"{word}{s}")
                generated.add(f"{s}{word}")
                generated.add(f"{word}{s}1")
        
        if leet:
            leet_map = {'a':'4','e':'3','i':'1','o':'0','s':'5','t':'7','b':'8','g':'9'}
            leet_word = ''.join(leet_map.get(c, c) for c in word.lower())
            generated.add(leet_word)
            generated.add(leet_word.upper())
            if nums:
                for i in range(100):
                    generated.add(f"{leet_word}{i}")
    
    # Save
    with open(output, 'w') as f:
        f.write('\n'.join(sorted(generated)))
    
    print(f"{G}[+] Generated {len(generated)} passwords → {output}{RS}")
    print(f"{Y}[!] File size: {os.path.getsize(output)/1024:.1f} KB{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def online_hash_lookup():
    """Tool 9: Online Hash Lookup"""
    hash_str = input(f"  {W}[?] Hash to lookup: {RS}").strip()
    
    print(f"\n{G}[+] Looking up {hash_str} in online databases...{RS}")
    
    sites = [
        f"https://crackstation.net/",
        f"https://md5decrypt.net/",
        f"https://hashes.org/",
        f"https://hashkiller.io/",
        f"https://nitrxgen.net/",
        f"https://md5online.org/",
        f"https://hashes.com/en/decrypt/hash",
    ]
    
    for url in sites:
        print(f"  {C}[+]{RS} {url}")
    
    # Try API lookup
    try:
        import requests
        r = requests.get(f'https://www.md5online.org/md5-decrypt.html', timeout=10)
        if r.status_code == 200:
            print(f"\n{G}[+] Manual check: Google the hash{RS}")
    except:
        pass
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def password_strength():
    """Tool 10: Password Strength Analyzer"""
    password = input(f"  {W}[?] Enter password to analyze: {RS}").strip()
    
    print(f"\n{G}[+] Password Strength Analysis{RS}")
    print(f"\n  {C}Password:{RS} {'*' * len(password)}")
    print(f"  {C}Length:{RS} {len(password)} characters")
    
    score = 0
    feedback = []
    
    # Length checks
    if len(password) >= 8: score += 1
    else: feedback.append("Should be at least 8 characters")
    if len(password) >= 12: score += 1
    if len(password) >= 16: score += 1
    
    # Character diversity
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
    
    if has_lower: score += 1
    else: feedback.append("Add lowercase letters")
    if has_upper: score += 1
    else: feedback.append("Add uppercase letters")
    if has_digit: score += 1
    else: feedback.append("Add numbers")
    if has_special: score += 1
    else: feedback.append("Add special characters")
    
    # Pattern checks
    if re.search(r'(.)\1{2,}', password):
        feedback.append("Avoid repeated characters (e.g., 'aaa')")
        score -= 1
    if re.search(r'(123|abc|qwerty|password|admin|letmein)', password.lower()):
        feedback.append("Avoid common patterns/words")
        score -= 1
    if re.search(r'(19|20)\d{2}', password):
        feedback.append("Avoid years")
        score -= 1
    
    # Entropy estimation
    charset = 0
    if has_lower: charset += 26
    if has_upper: charset += 26
    if has_digit: charset += 10
    if has_special: charset += 32
    entropy = len(password) * (charset.bit_length() if charset > 0 else 0)
    
    # Rating
    score = max(0, min(10, score))
    if score >= 9:
        rating = f"{G}Very Strong{RS}"
    elif score >= 7:
        rating = f"{C}Strong{RS}"
    elif score >= 5:
        rating = f"{Y}Moderate{RS}"
    elif score >= 3:
        rating = f"{M}Weak{RS}"
    else:
        rating = f"{R}Very Weak{RS}"
    
    # Time to crack estimates
    crack_times = {
        10: "instant",
        20: "a few seconds",
        30: "a few minutes",
        40: "a few hours",
        50: "a few days",
        60: "a few months",
        70: "a few years",
        80: "centuries",
    }
    
    crack_time = "unknown"
    for bits, time_str in crack_times.items():
        if entropy <= bits:
            crack_time = time_str
            break
    
    print(f"  {C}Score:{RS} {score}/10 - {rating}")
    print(f"  {C}Entropy:{RS} ~{max(entropy, 0)} bits")
    print(f"  {C}Crack Time:{RS} ~{crack_time}")
    
    # Character diversity bar
    print(f"\n  {W}Character Distribution:{RS}")
    print(f"  {G}Upper:{RS} {'█' * sum(1 for c in password if c.isupper())}")
    print(f"  {C}Lower:{RS} {'█' * sum(1 for c in password if c.islower())}")
    print(f"  {Y}Digit:{RS} {'█' * sum(1 for c in password if c.isdigit())}")
    print(f"  {M}Special:{RS} {'█' * sum(1 for c in password if not c.isalnum())}")
    
    if feedback:
        print(f"\n  {W}Improvements:{RS}")
        for f in feedback:
            print(f"  {Y}• {f}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def brute_force():
    """Tool 11: Brute Force Attack"""
    print(f"\n{Y}[!] Brute Force Attack Tool{RS}")
    hash_str = input(f"  {W}[?] Hash to crack: {RS}").strip()
    algo = input(f"  {W}[?] Algorithm (md5/sha1/sha256): {RS}").strip() or 'md5'
    charset = input(f"  {W}[?] Charset (e.g., abc123, default: lowercase+digits): {RS}").strip() or string.ascii_lowercase + string.digits
    max_len = int(input(f"  {W}[?] Maximum length (default: 4): {RS}").strip() or '4')
    
    print(f"\n{G}[+] Starting brute force... (max length: {max_len}, charset: {charset[:20]}...){RS}")
    print(f"{Y}[!] This may take a VERY long time. Press Ctrl+C to stop.{RS}")
    
    found = False
    try:
        for length in range(1, max_len + 1):
            print(f"\n  {W}Trying length {length}...{RS}")
            count = 0
            for combo in map(''.join, __import__('itertools').product(charset, repeat=length)):
                h = hashlib.new(algo)
                h.update(combo.encode())
                if h.hexdigest() == hash_str.lower():
                    print(f"\n{G}[+] PASSWORD FOUND: {Y}{combo}{RS}")
                    found = True
                    break
                count += 1
                if count % 100000 == 0:
                    print(f"  {C}Checked {count} passwords...{RS}", end='\r')
            if found:
                break
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Brute force interrupted{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    if not found:
        print(f"{Y}[-] Password not found within parameters{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def rainbow_table():
    """Tool 12: Rainbow Table Generator"""
    print(f"\n{G}[+] Rainbow Table Generator{RS}")
    print(f"{Y}[!] Rainbow tables pre-generate hash chains for fast lookup{RS}")
    
    algo = input(f"  {W}[?] Algorithm (md5/sha1/ntlm): {RS}").strip() or 'md5'
    wordlist = input(f"  {W}[?] Source wordlist path: {RS}").strip()
    output = input(f"  {W}[?] Output file (default: rainbow.txt): {RS}").strip() or 'rainbow.txt'
    
    if not wordlist or not os.path.exists(wordlist):
        print(f"{Y}[-] Wordlist not found{RS}")
        print(f"{Y}[!] Generating demo rainbow table with 100 passwords...{RS}")
        
        demo_passwords = ['password','123456','admin','letmein','qwerty','monkey','dragon',
                         'master','hello','shadow','sunshine','princess','football','passw0rd']
        
        with open(output, 'w') as f:
            for pwd in demo_passwords:
                h = hashlib.new(algo)
                h.update(pwd.encode())
                f.write(f"{h.hexdigest()}:{pwd}\n")
        
        print(f"{G}[+] Demo rainbow table generated: {output} ({len(demo_passwords)} entries){RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    print(f"\n{G}[+] Generating rainbow table...{RS}")
    try:
        count = 0
        with open(wordlist, 'r', errors='ignore') as f_in, open(output, 'w') as f_out:
            for line in f_in:
                pwd = line.strip()
                if pwd:
                    h = hashlib.new(algo)
                    h.update(pwd.encode())
                    f_out.write(f"{h.hexdigest()}:{pwd}\n")
                    count += 1
                    if count % 10000 == 0:
                        print(f"  {C}Processed {count} passwords...{RS}", end='\r')
        
        size = os.path.getsize(output) / (1024*1024)
        print(f"\n{G}[+] Rainbow table generated: {output} ({count} entries, {size:.1f} MB){RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def hashcat_wrapper():
    """Tool 13: Hashcat Wrapper"""
    print(f"\n{G}[+] Hashcat Wrapper{RS}")
    hash_file = input(f"  {W}[?] Hash file path: {RS}").strip()
    wordlist = input(f"  {W}[?] Wordlist path: {RS}").strip() or 'rockyou.txt'
    
    print(f"\n{W}Select hash type:{RS}")
    modes = [
        ('0', 'MD5'),
        ('100', 'SHA1'),
        ('1400', 'SHA256'),
        ('1700', 'SHA512'),
        ('1000', 'NTLM'),
        ('3200', 'bcrypt'),
        ('5500', 'NetNTLMv1'),
        ('5600', 'NetNTLMv2'),
        ('13100', 'Kerberos 5 TGS-REP'),
        ('18200', 'Kerberos 5 AS-REP'),
    ]
    
    for code, name in modes:
        print(f"  {W}[{code}]{RS} {name}")
    
    mode = input(f"\n{Y}  Mode: {RS}").strip() or '0'
    attack = input(f"  {W}[?] Attack mode (0=wordlist, 3=brute-force): {RS}").strip() or '0'
    
    cmd = f'hashcat -m {mode} -a {attack} {hash_file} {wordlist} --force'
    if attack == '3':
        mask = input(f"  {W}[?] Mask (e.g., ?l?l?l?d?d): {RS}").strip() or '?l?l?l?l'
        cmd = f'hashcat -m {mode} -a 3 {hash_file} {mask} --force'
    
    print(f"\n{G}[+] Command: {cmd}{RS}")
    run_now = input(f"{Y}[?] Run hashcat now? (y/n): {RS}").strip().lower()
    if run_now == 'y':
        os.system(cmd)
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def john_wrapper():
    """Tool 14: John the Ripper Wrapper"""
    print(f"\n{G}[+] John the Ripper Wrapper{RS}")
    hash_file = input(f"  {W}[?] Hash file path: {RS}").strip()
    wordlist = input(f"  {W}[?] Wordlist path (default: rockyou.txt): {RS}").strip() or 'rockyou.txt'
    
    print(f"\n{Y}[!] First convert hash to John format using john2zip/pdf2john/etc{RS}")
    print(f"\n{W}Common conversions:{RS}")
    print(f"  zip2john file.zip > hash.txt")
    print(f"  pdf2john file.pdf > hash.txt")
    print(f"  ssh2john id_rsa > hash.txt")
    print(f"  office2john file.docx > hash.txt")
    print(f"  unshadow passwd shadow > hash.txt")
    
    if os.path.exists(hash_file):
        cmd = f'john --wordlist={wordlist} {hash_file}'
        print(f"\n{G}[+] Command: {cmd}{RS}")
        run_now = input(f"{Y}[?] Run John now? (y/n): {RS}").strip().lower()
        if run_now == 'y':
            os.system(cmd)
            print(f"\n{G}[+] Cracked passwords:{RS}")
            os.system(f'john --show {hash_file}')
    else:
        print(f"{Y}[-] Hash file not found{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def cred_stuffing():
    """Tool 15: Credential Stuffing Check"""
    print(f"\n{G}[+] Credential Stuffing Check{RS}")
    email = input(f"  {W}[?] Email to check: {RS}").strip()
    
    print(f"\n{Y}[!] Checking if {email} has been exposed in breaches...{RS}")
    
    # Check haveibeenpwned
    try:
        import requests
        sha1 = hashlib.sha1(email.encode()).hexdigest().upper()
        prefix = sha1[:5]
        suffix = sha1[5:]
        
        r = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}', timeout=10)
        if r.status_code == 200:
            hashes = [line.split(':') for line in r.text.splitlines()]
            for h, count in hashes:
                if h == suffix:
                    print(f"  {R}[!] Email found in breaches! Seen {count} times{RS}")
                    break
            else:
                print(f"  {G}[+] Email not found in known breaches{RS}")
        else:
            print(f"  {Y}[-] Cannot check API{RS}")
    except:
        print(f"  {Y}[-] Cannot check breaches (no internet){RS}")
    
    print(f"\n{W}Manual checks:{RS}")
    print(f"  https://haveibeenpwned.com/account/{email}")
    print(f"  https://leakcheck.io/")
    print(f"  https://dehashed.com/")
    print(f"  https://scylla.so/")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
