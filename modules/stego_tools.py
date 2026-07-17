#!/usr/bin/env python3
"""
A2Tool v4.0 - Steganography Tools Module (10 Tools)
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time, base64
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
        print(f"\n{C}╔══════════════════════════════════════════════════════════════╗{RS}")
        print(f"{C}║{W}                Steganography Tools Suite                   {C}║{RS}")
        print(f"{C}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{C}║{W} [01]{R}  Image Steganography (LSB Hide)                    {C}║{RS}")
        print(f"{C}║{W} [02]{R}  Image Steganography (LSB Extract)                 {C}║{RS}")
        print(f"{C}║{W} [03]{R}  Audio Steganography (Hide in WAV)                 {C}║{RS}")
        print(f"{C}║{W} [04]{R}  Audio Steganography (Extract from WAV)            {C}║{RS}")
        print(f"{C}║{W} [05]{R}  Text Steganography (Whitespace/ZWC)               {C}║{RS}")
        print(f"{C}║{W} [06]{R}  Text Steganography (Extract)                      {C}║{RS}")
        print(f"{C}║{W} [07]{R}  EXIF Metadata Viewer                             {C}║{RS}")
        print(f"{C}║{W} [08]{R}  EXIF Metadata Stripper                            {C}║{RS}")
        print(f"{C}║{W} [09]{R}  File Signature/Header Analyzer                    {C}║{RS}")
        print(f"{C}║{W} [10]{R}  Multi-File Steganography Scanner                  {C}║{RS}")
        print(f"{C}║{W} [0]{R}   Back to Main Menu                                  {C}║{RS}")
        print(f"{C}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[Stego] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': image_hide()
        elif ch == '2': image_extract()
        elif ch == '3': audio_hide()
        elif ch == '4': audio_extract()
        elif ch == '5': text_hide()
        elif ch == '6': text_extract()
        elif ch == '7': exif_view()
        elif ch == '8': exif_strip()
        elif ch == '9': file_analyze()
        elif ch == '10': stego_scan()
        else: print(f"{R}[!] Invalid option{RS}")

def image_hide():
    print(f"\n{G}[+] Image Steganography - Hide Data{RS}")
    image = input(f"  {W}[?] Cover image path: {RS}").strip()
    data_file = input(f"  {W}[?] Data to hide (file path or text): {RS}").strip()
    output = input(f"  {W}[?] Output image (default: stego_image.png): {RS}").strip() or 'stego_image.png'
    
    if not os.path.exists(image):
        print(f"{R}[-] Image not found{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    # Check if data is a file or text
    if os.path.exists(data_file):
        with open(data_file, 'rb') as f:
            secret_data = f.read()
        print(f"{G}[+] Reading data from file ({len(secret_data)} bytes){RS}")
    else:
        secret_data = data_file.encode()
        print(f"{G}[+] Using text data ({len(secret_data)} bytes){RS}")
    
    # Use steghide if available
    if data_file and os.path.exists(data_file):
        passphrase = input(f"  {W}[?] Passphrase (optional): {RS}").strip()
        cmd = f'steghide embed -cf {image} -ef {data_file} -sf {output}'
        if passphrase:
            cmd += f' -p "{passphrase}"'
        print(f"{G}[+] Running: {cmd}{RS}")
        out = _run(cmd)
        print(f"{Y}{out}{RS}")
        if os.path.exists(output):
            print(f"{G}[+] Stego image saved: {output}{RS}")
    else:
        # Use Python LSB fallback
        try:
            from PIL import Image
            import numpy as np
            
            img = Image.open(image)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            pixels = np.array(img)
            
            # Check capacity
            capacity = pixels.size // 8
            if len(secret_data) > capacity:
                print(f"{R}[-] Data too large (max {capacity} bytes){RS}")
                input(f"\n{Y}[+] Press Enter to continue...{RS}")
                return
            
            # Add length header
            data = len(secret_data).to_bytes(4, 'big') + secret_data
            data_bits = ''.join(format(byte, '08b') for byte in data)
            
            # LSB encoding
            flat = pixels.flatten()
            for i, bit in enumerate(data_bits):
                flat[i] = (flat[i] & 0xFE) | int(bit)
            
            result = flat.reshape(pixels.shape)
            result_img = Image.fromarray(result.astype('uint8'), 'RGB')
            result_img.save(output)
            print(f"{G}[+] Data hidden in {output}{RS}")
        except ImportError:
            print(f"{Y}[!] Install Pillow: pip install Pillow{RS}")
            print(f"{Y}[!] Or use steghide (apt install steghide){RS}")
        except Exception as e:
            print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def image_extract():
    print(f"\n{G}[+] Image Steganography - Extract Data{RS}")
    image = input(f"  {W}[?] Stego image path: {RS}").strip()
    
    if not os.path.exists(image):
        print(f"{R}[-] Image not found{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    # Try steghide first
    passphrase = input(f"  {W}[?] Passphrase (if used): {RS}").strip()
    out_file = input(f"  {W}[?] Output file (default: extracted_data): {RS}").strip() or 'extracted_data'
    
    cmd = f'steghide extract -sf {image} -xf {out_file}'
    if passphrase:
        cmd += f' -p "{passphrase}"'
    
    print(f"{G}[+] Running: {cmd}{RS}")
    out = _run(cmd)
    
    if 'could not' in out.lower() or 'error' in out.lower():
        print(f"{Y}[-] steghide failed. Trying LSB extraction...{RS}")
        
        try:
            from PIL import Image
            import numpy as np
            
            img = Image.open(image)
            pixels = np.array(img)
            flat = pixels.flatten()
            
            # Extract LSBs
            bits = ''.join(str(pixel & 1) for pixel in flat[:32])
            data_len = int(bits, 2) * 8
            
            if data_len > 0 and data_len < pixels.size:
                bits = ''.join(str(pixel & 1) for pixel in flat[32:32+data_len])
                data = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
                
                with open(out_file, 'wb') as f:
                    f.write(data)
                print(f"{G}[+] Data extracted: {out_file}{RS}")
                try:
                    print(f"{G}[+] Content: {data.decode('utf-8')[:200]}{RS}")
                except:
                    print(f"{G}[+] Binary data ({len(data)} bytes){RS}")
            else:
                print(f"{Y}[-] No hidden data found{RS}")
        except ImportError:
            print(f"{Y}[!] Install Pillow: pip install Pillow{RS}")
        except Exception as e:
            print(f"{R}[-] Error: {e}{RS}")
    else:
        print(f"{G}[+] Data extracted to: {out_file}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def audio_hide():
    print(f"\n{G}[+] Audio Steganography - Hide Data in WAV{RS}")
    audio = input(f"  {W}[?] Cover audio (WAV): {RS}").strip()
    data = input(f"  {W}[?] Data to hide: {RS}").strip()
    output = input(f"  {W}[?] Output (default: stego_audio.wav): {RS}").strip() or 'stego_audio.wav'
    
    if not os.path.exists(audio):
        print(f"{R}[-] Audio file not found{RS}")
        print(f"{Y}[!] Using Coagula/DeepSound or spectrogram tools{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    # Use audio steganography tools
    print(f"{Y}[!] Install stegotools or use spectrogram method{RS}")
    print(f"\n{W}Alternative methods:{RS}")
    print(f"  {W}•{RS} DeepSound (Windows)")
    print(f"  {W}•{RS} Coagula (Windows/Mac)")
    print(f"  {W}•{RS} Spectrogram analysis (Sonic Visualiser)")
    print(f"  {W}•{RS} WAV LSB encoding (similar to image LSB)")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def audio_extract():
    print(f"\n{G}[+] Audio Steganography - Extract Data{RS}")
    audio = input(f"  {W}[?] Stego audio file: {RS}").strip()
    
    if not os.path.exists(audio):
        print(f"{R}[-] Audio not found{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    print(f"{W}Extraction methods:{RS}")
    print(f"  1. DeepSound - Extract hidden files")
    print(f"  2. Sonic Visualiser - View spectrogram")
    print(f"  3. Audacity - Spectrum analysis")
    print(f"  4. WAV LSB extraction (Python)")
    
    method = input(f"\n{Y}  Choice: {RS}").strip()
    if method == '4':
        try:
            import wave
            import numpy as np
            
            with wave.open(audio, 'rb') as wav:
                frames = wav.readframes(wav.getnframes())
                samples = np.frombuffer(frames, dtype=np.int16)
                
                # Extract LSB
                bits = ''.join(str(s & 1) for s in samples[:32000])
                if len(bits) >= 32:
                    data_len = int(bits[:32], 2) * 8
                    if data_len > 0 and data_len + 32 <= len(bits):
                        data_bits = bits[32:32+data_len]
                        data = bytes(int(data_bits[i:i+8], 2) for i in range(0, len(data_bits), 8))
                        fname = f"extracted_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        with open(fname, 'wb') as f:
                            f.write(data)
                        print(f"{G}[+] Data extracted: {fname}{RS}")
                    else:
                        print(f"{Y}[-] No hidden data found{RS}")
        except Exception as e:
            print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def text_hide():
    print(f"\n{G}[+] Text Steganography - Hide in Text{RS}")
    cover_text = input(f"  {W}[?] Cover text: {RS}").strip()
    secret = input(f"  {W}[?] Secret message: {RS}").strip()
    
    if not cover_text or not secret:
        print(f"{R}[-] Both cover text and secret message required{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    print(f"\n{G}[+] Zero-Width Character Encoding:{RS}")
    
    # ZWC method
    zws = '\u200B'  # Zero-width space
    zwnj = '\u200C'  # Zero-width non-joiner
    zwj = '\u200D'  # Zero-width joiner
    
    # Encode secret as binary
    binary = ''.join(format(ord(c), '08b') for c in secret)
    
    # Replace bits with ZWC
    encoded = ''
    for bit in binary:
        if bit == '0':
            encoded += zws
        else:
            encoded += zwj
    
    # Stego text: hide between characters
    result = ''
    for i, ch in enumerate(cover_text):
        result += ch
        if i < len(encoded):
            result += encoded[i]
    
    print(f"\n  {W}Stego Text (may appear normal):{RS}")
    print(f"  {Y}{result}{RS}")
    
    fname = f"stego_text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"{G}[+] Saved to {fname}{RS}")
    
    print(f"\n{W}Alternative - First letter encoding:{RS}")
    result2 = ''
    for i, word in enumerate(cover_text.split()):
        if i < len(secret):
            result2 += secret[i] + word[1:] + ' '
        else:
            result2 += word + ' '
    print(f"  {Y}{result2.strip()}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def text_extract():
    print(f"\n{G}[+] Text Steganography - Extract Hidden Message{RS}")
    text = input(f"  {W}[?] Stego text: {RS}").strip()
    
    if not text:
        print(f"{R}[-] No text provided{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    print(f"\n{W}Extracting Zero-Width Characters...{RS}")
    zws = '\u200B'
    zwnj = '\u200C'
    zwj = '\u200D'
    
    binary = ''
    for ch in text:
        if ch == zws:
            binary += '0'
        elif ch == zwj:
            binary += '1'
    
    if binary:
        # Decode binary to text
        decoded = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                decoded += chr(int(byte, 2))
        if decoded:
            print(f"  {G}[+] Hidden message: {Y}{decoded}{RS}")
        else:
            print(f"  {Y}[-] Could not decode message{RS}")
    else:
        print(f"  {Y}[-] No zero-width characters found{RS}")
        
        # Try first-letter extraction
        words = text.split()
        first_letters = ''.join(w[0] for w in words if w)
        if first_letters:
            print(f"  {W}First-letter decode: {Y}{first_letters}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def exif_view():
    print(f"\n{G}[+] EXIF Metadata Viewer{RS}")
    image = input(f"  {W}[?] Image file: {RS}").strip()
    
    if not os.path.exists(image):
        print(f"{R}[-] File not found{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    print(f"\n{W}EXIF Data for {image}:{RS}")
    
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        
        img = Image.open(image)
        exif_data = img.getexif()
        
        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                print(f"  {C}{tag:<30}{RS} {Y}{value}{RS}")
        else:
            print(f"  {Y}[-] No EXIF data found{RS}")
    
    except ImportError:
        print(f"{Y}[!] Install Pillow: pip install Pillow{RS}")
        # Fallback to exiftool
        out = _run(f'exiftool {image} 2>/dev/null')
        print(f"{Y}{out[:1500]}{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    # Also check for GPS coordinates
    try:
        from PIL.ExifTags import GPSTAGS
        img = Image.open(image)
        exif = img.getexif()
        gps_info = exif.get(0x8825, {})
        if gps_info:
            print(f"\n  {W}GPS Coordinates:{RS}")
            for k, v in gps_info.items():
                print(f"    {GPSTAGS.get(k, k)}: {v}")
    except:
        pass
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def exif_strip():
    print(f"\n{G}[+] EXIF Metadata Stripper{RS}")
    image = input(f"  {W}[?] Image file: {RS}").strip()
    output = input(f"  {W}[?] Output file (default: clean.jpg): {RS}").strip() or 'clean.jpg'
    
    if not os.path.exists(image):
        print(f"{R}[-] File not found{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    print(f"{W}Stripping EXIF metadata...{RS}")
    
    try:
        from PIL import Image
        img = Image.open(image)
        
        # Copy image data without EXIF
        img.save(output, exif=b'')
        
        # Verify
        clean = Image.open(output)
        clean_exif = clean.getexif()
        
        if len(clean_exif) == 0:
            print(f"{G}[+] EXIF data stripped. Saved as {output}{RS}")
        else:
            print(f"{Y}[!] Some data may remain{RS}")
    except ImportError:
        print(f"{Y}[!] Using exiftool:{RS}")
        os.system(f'exiftool -all= {image} -o {output}')
        print(f"{G}[+] Done{RS}")
    except Exception as e:
        print(f"{R}[-] Error: {e}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def file_analyze():
    print(f"\n{G}[+] File Signature / Header Analyzer{RS}")
    file_path = input(f"  {W}[?] File to analyze: {RS}").strip()
    
    if not os.path.exists(file_path):
        print(f"{R}[-] File not found{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    size = os.path.getsize(file_path)
    print(f"\n  {C}File:{RS} {file_path}")
    print(f"  {C}Size:{RS} {size:,} bytes ({size/1024:.1f} KB)")
    
    # Read magic bytes
    with open(file_path, 'rb') as f:
        header = f.read(16)
    
    hex_header = ' '.join(f'{b:02x}' for b in header)
    print(f"  {C}Hex Header:{RS} {Y}{hex_header}{RS}")
    
    # Identify file type
    signatures = {
        b'\xff\xd8\xff': 'JPEG Image',
        b'\x89PNG\r\n\x1a\n': 'PNG Image',
        b'GIF8': 'GIF Image',
        b'BM': 'BMP Image',
        b'RIFF': 'AVI / WAV / WEBP',
        b'PK\x03\x04': 'ZIP / DOCX / XLSX',
        b'Rar!\x1a\x07': 'RAR Archive',
        b'\x1f\x8b\x08': 'GZIP Archive',
        b'\x42\x5a\x68': 'BZIP2 Archive',
        b'\x25PDF': 'PDF Document',
        b'\x7fELF': 'ELF (Linux Executable)',
        b'MZ': 'PE (Windows Executable)',
        b'\xca\xfe\xba\xbe': 'Java Class File',
        b'\x1a\x45\xdf\xa3': 'MKV / WebM',
        b'\x00\x01\x00\x00': 'ICO Icon',
        b'%PDF': 'PDF Document',
        b'{\\rtf': 'RTF Document',
    }
    
    print(f"\n  {W}Identified Types:{RS}")
    found = False
    for magic, desc in signatures.items():
        if header.startswith(magic):
            print(f"  {G}[✓]{RS} {desc}")
            found = True
    
    if not found:
        print(f"  {Y}[?]{RS} Unknown file type")
    
    # Check for embedded data
    print(f"\n  {W}Embedded File Check:{RS}")
    if b'PK' in header:
        print(f"  {Y}[!]{RS} ZIP data found in header (possible nested archive)")
    if b'IEND' in header:
        print(f"  {Y}[!]{RS} PNG IEND chunk found (possible appended data after)")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def stego_scan():
    print(f"\n{G}[+] Multi-File Steganography Scanner{RS}")
    directory = input(f"  {W}[?] Directory to scan: {RS}").strip() or '.'
    
    if not os.path.exists(directory):
        print(f"{R}[-] Directory not found{RS}")
        input(f"\n{Y}[+] Press Enter to continue...{RS}")
        return
    
    print(f"\n{W}Scanning {directory} for steganography indicators...{RS}")
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    audio_extensions = ['.wav', '.mp3', '.aac', '.flac']
    suspicious = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            
            if ext in image_extensions:
                size = os.path.getsize(filepath)
                # Check for unusually large files
                if size > 10 * 1024 * 1024:  # > 10MB
                    suspicious.append((filepath, f'Large image ({size/1024/1024:.1f} MB)'))
                    print(f"  {Y}[!]{RS} {filepath}: {R}Large image{RS}")
                
                # Check IEND position (PNG)
                try:
                    with open(filepath, 'rb') as f:
                        data = f.read()
                        if ext == '.png' and b'IEND' in data:
                            iend_pos = data.rfind(b'IEND') + 12
                            if iend_pos < len(data):
                                suspicious.append((filepath, f'Data after PNG IEND ({len(data)-iend_pos} bytes)'))
                                print(f"  {Y}[!]{RS} {filepath}: {R}Data after IEND{RS}")
                except: pass
            
            elif ext in audio_extensions:
                print(f"  {C}[?]{RS} {filepath}: Audio file (check spectrogram)")
            
            # Check for embedded archives
            try:
                with open(filepath, 'rb') as f:
                    header = f.read(4)
                    if header == b'PK\x03\x04' and ext not in ['.zip', '.docx', '.xlsx', '.pptx']:
                        suspicious.append((filepath, 'Embedded ZIP archive'))
                        print(f"  {Y}[!]{RS} {filepath}: {R}Embedded ZIP!{RS}")
            except: pass
    
    if not suspicious:
        print(f"\n{G}[+] No obvious steganography indicators found{RS}")
    else:
        print(f"\n{R}[!] Found {len(suspicious)} suspicious files{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
