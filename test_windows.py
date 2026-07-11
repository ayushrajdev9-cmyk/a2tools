#!/usr/bin/env python3
"""Windows compatibility test for A2Tool"""
import sys, os, subprocess, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 55)
print("  A2Tool Windows Compatibility Test")
print("=" * 55)

# 1. Import all modules
print("\n[1/6] Testing module imports...")
try:
    from modules import wifi_tool, phishing, social_engineering, info_gathering, exploits, utils, payloads
    print("  [PASS] All 7 modules imported successfully")
except Exception as e:
    print(f"  [FAIL] Import error: {e}")

# 2. Test A2Tool main
print("\n[2/6] Testing A2Tool main module...")
try:
    import A2Tool
    print(f"  [PASS] Platform: {A2Tool.OS_NAME}")
    print(f"  [PASS] Windows detected: {A2Tool.IS_WINDOWS}")
except Exception as e:
    print(f"  [FAIL] {e}")

# 3. Test WiFi recovery on Windows
print("\n[3/6] Testing WiFi password recovery (Windows)...")
try:
    out = subprocess.check_output(
        ['netsh', 'wlan', 'show', 'profiles'],
        shell=True, stderr=subprocess.STDOUT, timeout=10
    ).decode('utf-8', errors='ignore')
    profiles = re.findall(r'All User Profile\s+:\s+(.+)', out)
    print(f"  [PASS] netsh wlan show profiles - Found {len(profiles)} saved networks")
    
    if profiles:
        # Test retrieving first profile password
        p = profiles[0].strip()
        detail = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profile', p, 'key=clear'],
            shell=True, stderr=subprocess.STDOUT, timeout=15
        ).decode('utf-8', errors='ignore')
        pwd_match = re.search(r'Key Content\s+:\s+(.+)', detail)
        status = "Password found" if pwd_match else "Open/No password"
        print(f"  [PASS] Profile '{p[:20]}...' - {status}")
except FileNotFoundError:
    print("  [SKIP] netsh not found (not Windows)")
except Exception as e:
    print(f"  [INFO] WiFi test: {e}")

# 4. Test phishing server
print("\n[4/6] Testing Phishing module...")
try:
    server = phishing.PhishingServer('facebook', '127.0.0.1', 9999)
    print("  [PASS] PhishingServer created (facebook template)")
    assert hasattr(server, 'start'), "Missing start method"
    assert hasattr(server, 'handle_request'), "Missing handle_request method"
    print("  [PASS] PhishingServer has all methods")
except Exception as e:
    print(f"  [FAIL] {e}")

# 5. Test all module menus exist
print("\n[5/6] Testing menu functions exist...")
modules_to_test = {
    'wifi_tool': wifi_tool,
    'phishing': phishing,
    'social_engineering': social_engineering,
    'info_gathering': info_gathering,
    'exploits': exploits,
    'payloads': payloads
}
all_ok = True
for name, mod in modules_to_test.items():
    if hasattr(mod, 'menu'):
        print(f"  [PASS] {name}.menu() exists")
    else:
        print(f"  [FAIL] {name}.menu() MISSING")
        all_ok = False

# 6. Test key functions
print("\n[6/6] Testing key platform functions...")
tests = [
    ("wifi_recover_windows", wifi_tool, True),
    ("wifi_scan_networks", wifi_tool, True),
    ("url_spoof", phishing, True),
    ("email_phishing", phishing, True),
    ("pretext_gen", social_engineering, True),
    ("whois_lookup", info_gathering, True),
    ("port_scan", info_gathering, True),
    ("generate_reverse_shell", payloads, True),
    ("crypto_tools", payloads, True),
    ("run_external_tool", utils, True),
    ("system_info_dump", utils, True),
]
for name, mod, expected in tests:
    actual = hasattr(mod, name)
    status = "[PASS]" if actual == expected else "[FAIL]"
    print(f"  {status} {name}: {actual}")

print("\n" + "=" * 55)
print("  TEST COMPLETE")
print("=" * 55)
