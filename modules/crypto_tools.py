#!/usr/bin/env python3
"""
A2Tool v4.0 - Cryptography & Encryption Tools Module (12 Tools)
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time, base64, hashlib, binascii
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
        print(f"\n{Y}╔══════════════════════════════════════════════════════════════╗{RS}")
        print(f"{Y}║{W}           Cryptography & Encryption Tools                  {Y}║{RS}")
        print(f"{Y}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{Y}║{W} [01]{R}  AES Encrypt / Decrypt File                        {Y}║{RS}")
        print(f"{Y}║{W} [02]{R}  RSA Key Pair Generator                            {Y}║{RS}")
        print(f"{Y}║{W} [03]{R}  Base64 / Hex / ASCII Converter                    {Y}║{RS}")
        print(f"{Y}║{W} [04]{R}  Hash Generator (MD5/SHA1/SHA256/SHA512)          {Y}║{RS}")
        print(f"{Y}║{W} [05]{R}  Caesar / ROT13 Cipher                            {Y}║{RS}")
        print(f"{Y}║{W} [06]{R}  Vigenere Cipher                                  {Y}║{RS}")
        print(f"{Y}║{W} [07]{R}  XOR Encryption                                    {Y}║{RS}")
        print(f"{Y}║{W} [08]{R}  HMAC Generator                                    {Y}║{RS}")
        print(f"{Y}║{W} [09]{R}  Password Generator                                {Y}║{RS}")
        print(f"{Y}║{W} [10]{R}  File Checksum Verifier                           {Y}║{RS}")
        print(f"{Y}║{W} [11]{R}  GPG Encryption / Decryption                      {Y}║{RS}")
        print(f"{Y}║{W} [12]{R}  SSL Certificate Generator                        {Y}║{RS}")
        print(f"{Y}║{W} [0]{R}   Back to Main Menu                                  {Y}║{RS}")
        print(f"{Y}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[Crypto] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': aes_crypt()
        elif ch == '2': rsa_gen()
        elif ch == '3': converter()
        elif ch == '4': hash_gen()
        elif ch == '5': caesar_cipher()
        elif ch == '6': vigenere_cipher()
        elif ch == '7': xor_crypt()
        elif ch == '8': hmac_gen()
        elif ch == '9': password_gen()
        elif ch == '10': checksum_verify()
        elif ch == '11': gpg_crypt()
        elif ch == '12': ssl_cert_gen()
        else: print(f"{R}[!] Invalid option{RS}")

def aes_crypt():
    print(f"\n{G}[+] AES Encrypt/Decrypt File{RS}")
    file_path = input(f"  {W}[?] File path: {RS}").strip()
    
    if not os.path.exists(file_path):
        print(f"{R}[-] File not found{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    mode = input(f"  {W}[?] Mode (encrypt/decrypt): {RS}").strip().lower() or 'encrypt'
    password = input(f"  {W}[?] Password: {RS}").strip()
    
    if not password:
        print(f"{R}[-] Password required{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    try:
        from Crypto.Cipher import AES
        from Crypto.Protocol.KDF import PBKDF2
        import os as _os
        
        if mode == 'encrypt':
            salt = _os.urandom(16)
            key = PBKDF2(password, salt, dkLen=32, count=100000)
            cipher = AES.new(key, AES.MODE_GCM)
            
            with open(file_path, 'rb') as f:
                plaintext = f.read()
            
            ciphertext, tag = cipher.encrypt_and_digest(plaintext)
            
            output = file_path + '.enc'
            with open(output, 'wb') as f:
                f.write(salt + cipher.nonce + tag + ciphertext)
            
            print(f"{G}[+] Encrypted: {output}{RS}")
            
        elif mode == 'decrypt':
            with open(file_path, 'rb') as f:
                salt = f.read(16)
                nonce = f.read(16)
                tag = f.read(16)
                ciphertext = f.read()
            
            key = PBKDF2(password, salt, dkLen=32, count=100000)
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            
            try:
                plaintext = cipher.decrypt_and_verify(ciphertext, tag)
                output = file_path.replace('.enc', '.dec') if file_path.endswith('.enc') else file_path + '.dec'
                with open(output, 'wb') as f:
                    f.write(plaintext)
                print(f"{G}[+] Decrypted: {output}{RS}")
            except:
                print(f"{R}[-] Decryption failed (wrong password or corrupted data){RS}")
    
    except ImportError:
        print(f"{Y}[!] Install pycryptodome: pip install pycryptodome{RS}")
        print(f"{Y}[!] Using openssl instead:{RS}")
        if mode == 'encrypt':
            os.system(f'openssl enc -aes-256-cbc -salt -in {file_path} -out {file_path}.enc -pass pass:{password}')
        else:
            os.system(f'openssl enc -d -aes-256-cbc -in {file_path} -out {file_path}.dec -pass pass:{password}')
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def rsa_gen():
    print(f"\n{G}[+] RSA Key Pair Generator{RS}")
    bits = int(input(f"  {W}[?] Key size (1024/2048/4096, default 2048): {RS}").strip() or '2048')
    
    print(f"{G}[+] Generating {bits}-bit RSA key pair...{RS}")
    
    try:
        from Crypto.PublicKey import RSA
        
        key = RSA.generate(bits)
        
        private_key = key.export_key('PEM')
        public_key = key.publickey().export_key('PEM')
        
        with open('private_key.pem', 'wb') as f:
            f.write(private_key)
        with open('public_key.pem', 'wb') as f:
            f.write(public_key)
        
        print(f"{G}[+] Private key: private_key.pem{RS}")
        print(f"{G}[+] Public key: public_key.pem{RS}")
        print(f"\n{W}Public Key:{RS}")
        print(f"  {Y}{public_key.decode()[:100]}...{RS}")
    
    except ImportError:
        print(f"{Y}[!] Install pycryptodome: pip install pycryptodome{RS}")
        print(f"{Y}[!] Using openssl:{RS}")
        os.system(f'openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:{bits}')
        os.system(f'openssl rsa -pubout -in private_key.pem -out public_key.pem')
        print(f"{G}[+] Keys generated with OpenSSL{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def converter():
    print(f"\n{G}[+] Base64 / Hex / ASCII / Binary Converter{RS}")
    
    input_str = input(f"  {W}[?] Input string: {RS}").strip()
    if not input_str:
        input_str = "Hello World"
    
    print(f"\n{W}Conversions for: {Y}{input_str}{RS}\n")
    
    # Base64
    b64_enc = base64.b64encode(input_str.encode()).decode()
    print(f"  {C}Base64 Encode:{RS} {Y}{b64_enc}{RS}")
    try:
        b64_dec = base64.b64decode(input_str).decode('utf-8', errors='ignore')
        print(f"  {C}Base64 Decode:{RS} {Y}{b64_dec}{RS}")
    except:
        pass
    
    # Hex
    hex_enc = input_str.encode().hex()
    print(f"  {C}Hex Encode:{RS} {Y}{hex_enc}{RS}")
    try:
        hex_dec = bytes.fromhex(input_str).decode('utf-8', errors='ignore')
        print(f"  {C}Hex Decode:{RS} {Y}{hex_dec}{RS}")
    except:
        pass
    
    # Binary
    binary = ' '.join(format(ord(c), '08b') for c in input_str)
    print(f"  {C}Binary:{RS} {Y}{binary[:80]}...{RS}")
    
    try:
        binary_chars = input_str.replace(' ', '')
        dec = int(binary_chars, 2)
        print(f"  {C}Binary to ASCII:{RS} {Y}{dec.to_bytes((dec.bit_length()+7)//8, 'big').decode()}{RS}")
    except:
        pass
    
    # URL encoding
    import urllib.parse
    url_enc = urllib.parse.quote(input_str)
    print(f"  {C}URL Encode:{RS} {Y}{url_enc}{RS}")
    url_dec = urllib.parse.unquote(input_str)
    if url_dec != input_str:
        print(f"  {C}URL Decode:{RS} {Y}{url_dec}{RS}")
    
    # ROT13
    rot13 = input_str.translate(str.maketrans(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM'
    ))
    print(f"  {C}ROT13:{RS} {Y}{rot13}{RS}")
    
    # Reverse
    print(f"  {C}Reverse:{RS} {Y}{input_str[::-1]}{RS}")
    
    # Character codes
    codes = ' '.join(str(ord(c)) for c in input_str[:20])
    print(f"  {C}ASCII Codes:{RS} {Y}{codes}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def hash_gen():
    print(f"\n{G}[+] Hash Generator{RS}")
    input_str = input(f"  {W}[?] Input text or file path: {RS}").strip()
    
    if os.path.exists(input_str):
        with open(input_str, 'rb') as f:
            data = f.read()
        print(f"{G}[+] Hashing file: {input_str} ({len(data)} bytes){RS}")
    else:
        data = input_str.encode()
    
    print(f"\n{W}Hash Values:{RS}")
    print(f"  {C}MD5:{RS} {Y}{hashlib.md5(data).hexdigest()}{RS}")
    print(f"  {C}SHA-1:{RS} {Y}{hashlib.sha1(data).hexdigest()}{RS}")
    print(f"  {C}SHA-224:{RS} {Y}{hashlib.sha224(data).hexdigest()}{RS}")
    print(f"  {C}SHA-256:{RS} {Y}{hashlib.sha256(data).hexdigest()}{RS}")
    print(f"  {C}SHA-384:{RS} {Y}{hashlib.sha384(data).hexdigest()}{RS}")
    print(f"  {C}SHA-512:{RS} {Y}{hashlib.sha512(data).hexdigest()}{RS}")
    print(f"  {C}Blake2b:{RS} {Y}{hashlib.blake2b(data).hexdigest()[:64]}{RS}")
    print(f"  {C}Blake2s:{RS} {Y}{hashlib.blake2s(data).hexdigest()}{RS}")
    
    if os.path.exists(input_str):
        fname = f"hashes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(fname, 'w') as f:
            f.write(f"File: {input_str}\n")
            f.write(f"MD5: {hashlib.md5(data).hexdigest()}\n")
            f.write(f"SHA1: {hashlib.sha1(data).hexdigest()}\n")
            f.write(f"SHA256: {hashlib.sha256(data).hexdigest()}\n")
            f.write(f"SHA512: {hashlib.sha512(data).hexdigest()}\n")
        print(f"\n{G}[+] Saved to {fname}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def caesar_cipher():
    print(f"\n{G}[+] Caesar / ROT13 Cipher{RS}")
    text = input(f"  {W}[?] Text: {RS}").strip()
    
    if not text:
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    shift_input = input(f"  {W}[?] Shift (default 13): {RS}").strip() or '13'
    shift = int(shift_input)
    
    print(f"\n{W}Results (shift={shift}):{RS}")
    
    # Encrypt
    result = ''
    for c in text:
        if c.isalpha():
            ascii_offset = 65 if c.isupper() else 97
            result += chr((ord(c) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += c
    
    print(f"  {C}Output:{RS} {Y}{result}{RS}")
    
    # Brute force all shifts
    if input(f"\n{Y}[?] Show all shifts? (y/n): {RS}").strip().lower() == 'y':
        print(f"\n{W}All ROT shifts:{RS}")
        for s in range(1, 26):
            decoded = ''
            for c in text:
                if c.isalpha():
                    offset = 65 if c.isupper() else 97
                    decoded += chr((ord(c) - offset + s) % 26 + offset)
                else:
                    decoded += c
            print(f"  {C}ROT-{s:02d}:{RS} {Y}{decoded[:60]}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def vigenere_cipher():
    print(f"\n{G}[+] Vigenere Cipher{RS}")
    text = input(f"  {W}[?] Text: {RS}").strip()
    key = input(f"  {W}[?] Key: {RS}").strip()
    
    if not text or not key:
        print(f"{R}[-] Text and key required{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    mode = input(f"  {W}[?] Mode (encrypt/decrypt): {RS}").strip().lower() or 'encrypt'
    
    def vigenere(text, key, decrypt=False):
        result = ''
        key_idx = 0
        for c in text:
            if c.isalpha():
                offset = 65 if c.isupper() else 97
                key_char = key[key_idx % len(key)]
                key_shift = ord(key_char.lower()) - 97
                if decrypt:
                    key_shift = -key_shift
                result += chr((ord(c) - offset + key_shift) % 26 + offset)
                key_idx += 1
            else:
                result += c
        return result
    
    output = vigenere(text, key, mode == 'decrypt')
    print(f"\n  {C}Result:{RS} {Y}{output}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def xor_crypt():
    print(f"\n{G}[+] XOR Encryption{RS}")
    text = input(f"  {W}[?] Text: {RS}").strip()
    key = input(f"  {W}[?] XOR Key (character): {RS}").strip() or 'K'
    
    if not text:
        print(f"{R}[-] Text required{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    key_ord = ord(key[0])
    
    # XOR encrypt
    xored = ''.join(chr(ord(c) ^ key_ord) for c in text)
    
    print(f"\n{W}XOR Results (key='{key}', 0x{key_ord:02x}):{RS}")
    print(f"  {C}XOR Text:{RS} {Y}{repr(xored)[:80]}{RS}")
    print(f"  {C}XOR Hex:{RS} {Y}{' '.join(f'{ord(c):02x}' for c in xored[:20])}{RS}")
    print(f"  {C}XOR Base64:{RS} {Y}{base64.b64encode(xored.encode('latin-1')).decode()}{RS}")
    
    # Multi-byte XOR
    key_multi = input(f"\n  {W}[?] Multi-byte key (press Enter to skip): {RS}").strip()
    if key_multi:
        xored_multi = ''
        for i, c in enumerate(text):
            k = ord(key_multi[i % len(key_multi)])
            xored_multi += chr(ord(c) ^ k)
        print(f"\n  {C}Multi-byte XOR ({key_multi}):{RS}")
        print(f"  {Y}{base64.b64encode(xored_multi.encode('latin-1')).decode()}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def hmac_gen():
    print(f"\n{G}[+] HMAC Generator{RS}")
    message = input(f"  {W}[?] Message: {RS}").strip()
    secret = input(f"  {W}[?] Secret key: {RS}").strip()
    
    if not message:
        print(f"{R}[-] Message required{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    import hmac as _hmac
    
    if not secret:
        secret = 'a2tool_secret'
        print(f"  {Y}[!] Using default secret: {secret}{RS}")
    
    print(f"\n{W}HMAC Values:{RS}")
    print(f"  {C}HMAC-MD5:{RS} {Y}_hmac.new(secret.encode(), message.encode(), hashlib.md5).hexdigest(){RS}")
    print(f"  {C}HMAC-SHA1:{RS} {Y}_hmac.new(secret.encode(), message.encode(), hashlib.sha1).hexdigest(){RS}")
    print(f"  {C}HMAC-SHA256:{RS} {Y}_hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest(){RS}")
    print(f"  {C}HMAC-SHA512:{RS} {Y}_hmac.new(secret.encode(), message.encode(), hashlib.sha512).hexdigest(){RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def password_gen():
    print(f"\n{G}[+] Password Generator{RS}")
    
    length = int(input(f"  {W}[?] Length (default 16): {RS}").strip() or '16')
    use_upper = input(f"  {W}[?] Include uppercase? (y/n, default y): {RS}").strip().lower() != 'n'
    use_digits = input(f"  {W}[?] Include digits? (y/n, default y): {RS}").strip().lower() != 'n'
    use_special = input(f"  {W}[?] Include special chars? (y/n, default y): {RS}").strip().lower() != 'n'
    count = int(input(f"  {W}[?] Number of passwords (default 5): {RS}").strip() or '5')
    
    import random, string
    chars = string.ascii_lowercase
    if use_upper: chars += string.ascii_uppercase
    if use_digits: chars += string.digits
    if use_special: chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    print(f"\n{G}[+] Generated Password{'' if count == 1 else 's'}:{RS}\n")
    for i in range(count):
        pwd = ''.join(random.choice(chars) for _ in range(length))
        # Calculate strength
        has_upper = any(c.isupper() for c in pwd)
        has_digit = any(c.isdigit() for c in pwd)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pwd)
        score = sum([len(pwd) >= 12, has_upper and has_digit, has_special, len(pwd) >= 16])
        strength = ['Very Weak', 'Weak', 'Fair', 'Strong', 'Very Strong'][min(score, 4)]
        
        print(f"  {Y}{pwd}{RS}  {W}[{strength}]{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def checksum_verify():
    print(f"\n{G}[+] File Checksum Verifier{RS}")
    file_path = input(f"  {W}[?] File path: {RS}").strip()
    
    if not os.path.exists(file_path):
        print(f"{R}[-] File not found{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    expected = input(f"  {W}[?] Expected hash (press Enter to skip): {RS}").strip()
    algo = input(f"  {W}[?] Algorithm (md5/sha1/sha256, default sha256): {RS}").strip() or 'sha256'
    
    print(f"\n{G}[+] Calculating {algo.upper()} checksum...{RS}")
    
    h = hashlib.new(algo)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    
    file_hash = h.hexdigest()
    print(f"  {C}{algo.upper()}:{RS} {Y}{file_hash}{RS}")
    
    if expected:
        if file_hash == expected.lower():
            print(f"  {G}[✓] Hash MATCHES! File is authentic.{RS}")
        else:
            print(f"  {R}[✗] Hash MISMATCH! File may be corrupted or tampered.{RS}")
    
    # Save hash
    if input(f"\n{Y}[?] Save hash to file? (y/n): {RS}").strip().lower() == 'y':
        hash_file = file_path + '.' + algo
        with open(hash_file, 'w') as f:
            f.write(f"{file_hash}  {os.path.basename(file_path)}")
        print(f"{G}[+] Hash saved to {hash_file}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def gpg_crypt():
    print(f"\n{G}[+] GPG Encryption / Decryption{RS}")
    
    print(f"\n{W}GPG Operations:{RS}")
    print(f"  1. Encrypt file")
    print(f"  2. Decrypt file")
    print(f"  3. Generate GPG key")
    print(f"  4. List keys")
    
    ch = input(f"\n{Y}  Choice: {RS}").strip()
    
    if ch == '1':
        file_path = input(f"  {W}[?] File to encrypt: {RS}").strip()
        recipient = input(f"  {W}[?] Recipient (email or key ID): {RS}").strip()
        if file_path and recipient:
            os.system(f'gpg --encrypt --recipient {recipient} {file_path}')
            print(f"{G}[+] Encrypted: {file_path}.gpg{RS}")
    
    elif ch == '2':
        file_path = input(f"  {W}[?] File to decrypt: {RS}").strip()
        if file_path:
            os.system(f'gpg --decrypt {file_path}')
    
    elif ch == '3':
        name = input(f"  {W}[?] Your name: {RS}").strip()
        email = input(f"  {W}[?] Your email: {RS}").strip()
        if name and email:
            os.system(f'gpg --batch --gen-key 2>/dev/null')
            print(f"{G}[+] GPG key generated{RS}")
    
    elif ch == '4':
        os.system('gpg --list-keys')
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def ssl_cert_gen():
    print(f"\n{G}[+] SSL Certificate Generator (Self-Signed){RS}")
    
    print(f"{W}Generating self-signed SSL certificate...{RS}")
    
    # Generate using OpenSSL
    cmd = '''openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"'''
    
    print(f"{G}[+] Command: {cmd}{RS}")
    os.system(cmd)
    
    if os.path.exists('cert.pem') and os.path.exists('key.pem'):
        print(f"{G}[+] Certificate generated:{RS}")
        print(f"  {C}Cert:{RS} cert.pem")
        print(f"  {C}Key:{RS} key.pem")
        print(f"  {C}Expires:{RS} 365 days")
        
        # Display certificate info
        os.system('openssl x509 -in cert.pem -text -noout | head -20')
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
