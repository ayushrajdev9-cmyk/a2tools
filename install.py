#!/usr/bin/env python3
import os, sys, subprocess, platform

def main():
    print("=" * 60)
    print("  A2Tool v3.0 - Installation Script")
    print("  Author: Ayush Rajdev & Anzar Iqbal")
    print("=" * 60)
    
    # Install Python dependencies
    print("\n[*] Installing Python dependencies...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--quiet'], shell=True)
    
    print("\n[+] Installation complete!")
    print("[+] Run: python A2Tool.py")
    input("\nPress Enter to start A2Tool...")
    os.system('python A2Tool.py')

if __name__ == '__main__':
    main()
