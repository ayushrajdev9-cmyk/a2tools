#!/usr/bin/env python3
"""
A2Tool v4.0 - Social Engineering Toolkit (12 Tools)
Author: Ayush Rajdev & Anzar Iqbal
"""

import os, sys, subprocess, re, json, time, random
from datetime import datetime
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except:
    class Fore: RED=GREEN=YELLOW=BLUE=MAGENTA=CYAN=WHITE='';RESET=''
    class Style: RESET_ALL='';BRIGHT='';DIM='';NORMAL=''

R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; B=Fore.BLUE
M=Fore.MAGENTA; C=Fore.CYAN; W=Fore.WHITE; RS=Style.RESET_ALL

PRETEXT_SCENARIOS = {
    'tech_support': [
        "Hi, I'm calling from Microsoft Windows Support. We've detected a virus on your computer.",
        "This is your ISP's technical department. We're seeing unusual activity from your connection.",
        "I'm from the IT Security team. We need you to verify your credentials immediately."
    ],
    'bank_fraud': [
        "This is your bank's fraud department. We noticed suspicious transactions on your account.",
        "We need to verify your card details due to a security breach. Please confirm your PIN.",
        "Your account has been temporarily locked. Click the link to restore access."
    ],
    'hr_recruiter': [
        "We saw your profile and think you'd be perfect for a senior position at our company.",
        "I'm a recruiter from a top tech firm. Can you verify your employment history?",
        "Congratulations! You've been shortlisted for an interview. Please confirm your details."
    ],
    'government': [
        "This is the Tax Department. You have an outstanding balance that needs immediate payment.",
        "Court notice: You are required to appear for a hearing. Click here for details.",
        "Social Security Alert: Your benefits have been suspended. Update your information."
    ],
    'delivery': [
        "Your package could not be delivered. Reschedule delivery here.",
        "Customs holds your shipment. Pay the clearance fee to release it.",
        "Your Amazon order has been shipped! Track your package here."
    ],
    'emergency': [
        "This is [Name] from the hospital. Your family member has been in an accident.",
        "Urgent: I'm stranded and need money. Please send help immediately.",
        "Your child's school is calling about an emergency. Please respond right away."
    ]
}

def menu():
    while True:
        print(f"\n{Y}╔══════════════════════════════════════════════════════════════╗{RS}")
        print(f"{Y}║{W}            Social Engineering Toolkit                       {Y}║{RS}")
        print(f"{Y}╠══════════════════════════════════════════════════════════════╣{RS}")
        print(f"{Y}║{W} [01]{R}  Pretext Generator (Call Scripts)                   {Y}║{RS}")
        print(f"{Y}║{W} [02]{R}  Fake Identity Generator                            {Y}║{RS}")
        print(f"{Y}║{W} [03]{R}  Fake Email Address Generator                       {Y}║{RS}")
        print(f"{Y}║{W} [04]{R}  Fake Social Media Profile Builder                  {Y}║{RS}")
        print(f"{Y}║{W} [05]{R}  Phone Number Spoofing Guide                        {Y}║{RS}")
        print(f"{Y}║{W} [06]{R}  Caller ID Spoofing                                {Y}║{RS}")
        print(f"{Y}║{W} [07]{R}  Social Media OSINT Recon                          {Y}║{RS}")
        print(f"{Y}║{W} [08]{R}  Psychological Manipulation Scripts                 {Y}║{RS}")
        print(f"{Y}║{W} [09]{R}  USB Drop Attack Auto-Generator                     {Y}║{RS}")
        print(f"{Y}║{W} [10]{R}  Fake Job Posting Generator                         {Y}║{RS}")
        print(f"{Y}║{W} [11]{R}  Impersonation Checklist Generator                  {Y}║{RS}")
        print(f"{Y}║{W} [12]{R}  Vishing (Voice Phishing) Scripts                  {Y}║{RS}")
        print(f"{Y}║{W} [0]{R}   Back to Main Menu                                  {Y}║{RS}")
        print(f"{Y}╚══════════════════════════════════════════════════════════════╝{RS}")
        ch = input(f"\n{Y}  A2Tool[SE] » {RS}").strip()
        if ch == '0': break
        elif ch == '1': pretext_gen()
        elif ch == '2': fake_identity()
        elif ch == '3': fake_email()
        elif ch == '4': fake_social_profile()
        elif ch == '5': phone_spoof_guide()
        elif ch == '6': callerid_spoof()
        elif ch == '7': social_osint()
        elif ch == '8': psych_scripts()
        elif ch == '9': usb_drop()
        elif ch == '10': fake_job()
        elif ch == '11': impersonation_checklist()
        elif ch == '12': vishing_scripts()
        else: print(f"{R}[!] Invalid option{RS}")

def pretext_gen():
    """Tool 1: Pretext Generator"""
    print(f"\n{G}[+] Pretext Script Generator{RS}")
    print(f"\n{W}Select scenario:{RS}")
    scenarios = list(PRETEXT_SCENARIOS.keys())
    for i, s in enumerate(scenarios, 1):
        print(f"  {W}[{i}]{RS} {s.replace('_',' ').title()}")
    print(f"  {W}[0]{RS} Custom")
    
    ch = input(f"\n{Y}  Choice: {RS}").strip()
    if ch == '0':
        custom = input(f"  {W}[?] Enter custom scenario: {RS}").strip()
        print(f"\n{G}[+] Custom Pretext:{RS}")
        print(f"  {Y}{custom}{RS}")
    elif ch.isdigit() and 1 <= int(ch) <= len(scenarios):
        s = scenarios[int(ch)-1]
        scripts = PRETEXT_SCENARIOS[s]
        print(f"\n{G}[+] Pretext Scripts for {s.replace('_',' ').title()}:{RS}")
        for i, script in enumerate(scripts, 1):
            print(f"\n  {W}[Script {i}]{RS}")
            print(f"  {Y}{script}{RS}")
    
    print(f"\n{W}Tips for convincing pretexts:{RS}")
    print(f"  {W}•{RS} Use authoritative tone")
    print(f"  {W}•{RS} Create urgency or fear")
    print(f"  {W}•{RS} Ask for verification/action")
    print(f"  {W}•{RS} Sound confident and professional")
    print(f"  {W}•{RS} Have answers ready for common objections")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def fake_identity():
    """Tool 2: Fake Identity Generator"""
    print(f"\n{G}[+] Fake Identity Generator{RS}")
    
    first_names = ['James','Mary','John','Patricia','Robert','Jennifer','Michael','Linda','David','Elizabeth',
                   'William','Barbara','Richard','Susan','Joseph','Jessica','Thomas','Sarah','Christopher','Karen',
                   'Alex','Emma','Ryan','Olivia','Tyler','Sophia','Daniel','Isabella','Matthew','Mia']
    
    last_names = ['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Rodriguez','Martinez',
                  'Hernandez','Lopez','Gonzalez','Wilson','Anderson','Thomas','Taylor','Moore','Jackson','Martin',
                  'Lee','Perez','Thompson','White','Harris','Sanchez','Clark','Ramirez','Lewis','Robinson']
    
    streets = ['Oak St','Elm St','Main St','Pine Rd','Maple Ave','Cedar Ln','Birch Blvd','Walnut Dr','Cherry Ct','Willow Way']
    cities = ['New York','Los Angeles','Chicago','Houston','Phoenix','Philadelphia','San Antonio','San Diego','Dallas','Austin']
    states = ['NY','CA','IL','TX','AZ','PA','TX','CA','TX','TX']
    zips = [f'{random.randint(10000,99999)}' for _ in range(10)]
    
    count = int(input(f"  {W}[?] How many identities to generate? (1-50): {RS}").strip() or '5')
    count = min(max(count, 1), 50)
    
    print(f"\n{G}[+] Generated Identities:{RS}")
    print(f"  {'='*70}")
    
    for i in range(count):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        idx = random.randint(0,9)
        dob = f"{random.randint(1,12):02d}/{random.randint(1,28):02d}/{random.randint(1960,2000)}"
        phone = f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
        email = f"{fn.lower()}.{ln.lower()}{random.randint(1,99)}@gmail.com"
        ssn = f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}"
        
        print(f"\n  {W}[Identity {i+1}]{RS}")
        print(f"  {C}Name:{RS} {fn} {ln}")
        print(f"  {C}DOB:{RS} {dob}")
        print(f"  {C}Address:{RS} {random.randint(100,9999)} {random.choice(streets)}, {cities[idx]}, {states[idx]} {zips[idx]}")
        print(f"  {C}Phone:{RS} {phone}")
        print(f"  {C}Email:{RS} {email}")
        print(f"  {C}SSN:{RS} {ssn}")
        print(f"  {C}Username:{RS} {fn.lower()}_{ln.lower()}{random.randint(1,99)}")
        print(f"  {C}Password:{RS} {''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%') for _ in range(12))}")
    
    save = input(f"\n{Y}[?] Save to file? (y/n): {RS}").strip().lower()
    if save == 'y':
        fname = f"identities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(fname, 'w') as f:
            for i in range(count):
                f.write(f"Identity {i+1}: {random.choice(first_names)} {random.choice(last_names)}\n")
        print(f"{G}[+] Saved to {fname}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def fake_email():
    """Tool 3: Fake Email Generator"""
    print(f"\n{G}[+] Disposable Email Address Generator{RS}")
    domains = ['tempmail.com','10minutemail.com','guerrillamail.com','mailinator.com',
               'yopmail.com','throwaway.email','trashmail.com','sharklasers.com']
    name = input(f"  {W}[?] Desired username (or random): {RS}").strip()
    if not name:
        name = ''.join(random.choices(string.ascii_lowercase, k=10))
    
    print(f"\n{G}[+] Generated Email Addresses:{RS}")
    for d in domains:
        print(f"  {C}{name}@{d}{RS}")
    
    print(f"\n{Y}[!] Use guerillamail.com API for inbox access{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def fake_social_profile():
    """Tool 4: Fake Social Media Profile"""
    print(f"\n{G}[+] Fake Social Media Profile Builder{RS}")
    platform = input(f"  {W}[?] Platform (facebook/instagram/linkedin/twitter): {RS}").strip().lower()
    name = input(f"  {W}[?] Profile name: {RS}").strip()
    bio = input(f"  {W}[?] Bio/Description: {RS}").strip()
    
    print(f"\n{G}[+] Profile generated for {platform}:{RS}")
    print(f"  {W}Name:{RS} {name}")
    print(f"  {W}Bio:{RS} {bio}")
    print(f"  {W}Followers:{RS} {random.randint(100,50000)}")
    print(f"  {W}Following:{RS} {random.randint(50,2000)}")
    print(f"  {W}Posts:{RS} {random.randint(10,500)}")
    print(f"  {W}Joined:{RS} {random.randint(2010,2024)}")
    
    # Generate realistic-looking posts
    print(f"\n{W}Sample Posts:{RS}")
    posts = [
        f"Just had an amazing day at {random.choice(['the beach','work','the gym','a conference','home'])}! #blessed",
        f"New blog post: Why {random.choice(['technology','health','finance','education','travel'])} is changing everything",
        f"Grateful for all the support from my followers. {random.randint(10,999)}K and growing! 🙏",
        f"Check out my latest project! Link in bio. #innovation #{random.choice(['tech','art','business','design'])}"
    ]
    for p in posts:
        print(f"  {Y}📝 {p}{RS}")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def phone_spoof_guide():
    """Tool 5: Phone Number Spoofing Guide"""
    print(f"\n{Y}[!] Phone Number Spoofing Guide{RS}")
    print(f"\n{W}Methods to spoof caller ID:{RS}")
    print(f"  {W}1.{RS} VoIP Services (SIP Trunking) - Set any caller ID")
    print(f"  {W}2.{RS} SpoofCard / SpoofApp - Commercial services")
    print(f"  {W}3.{RS} Twilio - Programmatic caller ID spoofing")
    print(f"  {W}4.{RS} Google Voice - Outbound caller ID selection")
    print(f"  {W}5.{RS} PBX Systems - Asterisk/FreePBX with trunk providers")
    print(f"  {W}6.{RS} Burner Phones - Prepaid numbers")
    print(f"  {W}7.{RS} SIP Protocol Manipulation")
    print(f"\n{R}[!] Note: Caller ID spoofing may be illegal in your jurisdiction{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def callerid_spoof():
    """Tool 6: Caller ID Spoofing"""
    print(f"\n{Y}[!] Caller ID Spoofing Tool{RS}")
    target = input(f"  {W}[?] Target phone number: {RS}").strip()
    spoofed = input(f"  {W}[?] Spoofed caller ID number: {RS}").strip()
    message = input(f"  {W}[?] Voice message (or 'record' for custom): {RS}").strip()
    
    print(f"\n{G}[+] Call configured:{RS}")
    print(f"  {C}Target:{RS} {target}")
    print(f"  {C}Spoofed As:{RS} {spoofed}")
    print(f"  {C}Message:{RS} {message}")
    print(f"\n{Y}[!] Requires SIP trunk or VoIP provider with outbound calling{RS}")
    print(f"{Y}[!] Use Twilio, Plivo, or Asterisk for actual implementation{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def social_osint():
    """Tool 7: Social Media OSINT Recon"""
    print(f"\n{G}[+] Social Media OSINT Reconnaissance{RS}")
    username = input(f"  {W}[?] Target username (for all platforms): {RS}").strip()
    
    platforms = {
        'Facebook': f'https://facebook.com/{username}',
        'Instagram': f'https://instagram.com/{username}',
        'Twitter/X': f'https://twitter.com/{username}',
        'LinkedIn': f'https://linkedin.com/in/{username}',
        'GitHub': f'https://github.com/{username}',
        'Reddit': f'https://reddit.com/u/{username}',
        'Telegram': f'https://t.me/{username}',
        'TikTok': f'https://tiktok.com/@{username}',
        'YouTube': f'https://youtube.com/@{username}',
        'Snapchat': f'https://snapchat.com/add/{username}',
        'Pinterest': f'https://pinterest.com/{username}',
        'Tumblr': f'https://{username}.tumblr.com',
        'Medium': f'https://medium.com/@{username}',
        'Twitch': f'https://twitch.tv/{username}',
        'Discord': f'https://discord.com/users/{username}',
        'WhatsApp': f'https://wa.me/{username}',
        'Signal': f'Username: {username} (invite required)',
        'WeChat': f'ID: {username}',
        'VK': f'https://vk.com/{username}',
        'Mastodon': f'https://mastodon.social/@{username}',
    }
    
    print(f"\n{G}[+] Searching for '{username}' across platforms:{RS}")
    for platform, url in platforms.items():
        print(f"  {C}{platform:<15}{RS} → {Y}{url}{RS}")
    
    print(f"\n{G}[+] Recommended OSINT tools for social media:{RS}")
    print(f"  {W}•{RS} Sherlock (github.com/sherlock-project/sherlock)")
    print(f"  {W}•{RS} Social-analyzer")
    print(f"  {W}•{RS} theHarvester")
    print(f"  {W}•{RS} Maigret")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def psych_scripts():
    """Tool 8: Psychological Manipulation Scripts"""
    print(f"\n{Y}[!] Psychological Manipulation Techniques{RS}")
    print(f"\n{W}Common manipulation tactics:{RS}")
    tactics = [
        ("Authority", "Imply you have authority or represent an official organization"),
        ("Urgency", "Create time pressure to force quick decisions"),
        ("Scarcity", "Claim limited availability or opportunity"),
        ("Social Proof", "Mention others who have already complied"),
        ("Reciprocity", "Offer something small before asking for something big"),
        ("Liking", "Build rapport and find common ground"),
        ("Commitment", "Start with small requests, then escalate"),
        ("Fear", "Threaten negative consequences for non-compliance"),
        ("Curiosity", "Pique interest with intriguing offers or information"),
        ("Distraction", "Overwhelm with information to prevent critical thinking")
    ]
    
    for i, (name, desc) in enumerate(tactics, 1):
        print(f"  {W}{i:02d}. {name:<15}{RS} {Y}{desc}{RS}")
    
    print(f"\n{W}Sample manipulation script:{RS}")
    print(f"""\n  {Y}"Hello, this is [Authority Figure] from [Organization].
  We've detected [Urgency/Security Issue] with your account.
  If not resolved within [Time Pressure], your account will be [Negative Consequence].
  Many of our customers have already [Social Proof] resolved this.
  To help you, we'll [Reciprocity] provide a free security check.
  Can you confirm your account details so we can proceed?"{RS}""")
    
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def usb_drop():
    """Tool 9: USB Drop Attack Auto-Generator"""
    print(f"\n{Y}[!] USB Drop Attack Generator{RS}")
    payload_type = input(f"  {W}[?] Payload type (reverse_shell/keylogger/credential_dump): {RS}").strip()
    ip = input(f"  {W}[?] Listener IP: {RS}").strip()
    port = input(f"  {W}[?] Listener Port: {RS}").strip()
    
    print(f"\n{G}[+] USB Drop Configuration:{RS}")
    print(f"  {C}Payload:{RS} {payload_type}")
    print(f"  {C}Callback:{RS} {ip}:{port}")
    
    # Generate autorun.inf
    print(f"\n{W}autorun.inf content:{RS}")
    print(f"""  [Autorun]
  open=payload.exe
  icon=folder.ico
  action=Open folder to view files""")
    
    print(f"\n{W}Recommended USB Rubber Ducky / Bash Bunny scripts are in /modules/payloads{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def fake_job():
    """Tool 10: Fake Job Posting Generator"""
    print(f"\n{G}[+] Fake Job Posting Generator{RS}")
    companies = ['TechCorp','DataFlow','CloudNine','Apex Systems','NexGen','Quantum Labs',
                 'FusionTech','Pinnacle','Stellar AI','OmniData','CyberSec Inc','Alpha Dev']
    positions = ['Senior Developer','Data Scientist','Security Analyst','DevOps Engineer',
                 'ML Engineer','Cloud Architect','Penetration Tester','SOC Analyst',
                 'Full Stack Developer','AI Researcher','Network Engineer','CTO']
    
    company = random.choice(companies)
    position = random.choice(positions)
    salary = random.randint(80000, 250000)
    location = random.choice(['Remote','New York','San Francisco','Austin','London','Berlin','Singapore'])
    
    print(f"\n{G}[+] Generated Job Posting:{RS}")
    print(f"""\n  {W}Company:{RS} {company}
  {W}Position:{RS} {position}
  {W}Salary:{RS} ${salary}/year
  {W}Location:{RS} {location}
  {W}Type:{RS} Full-time
  
  {W}Description:{RS}
  We are looking for a talented {position} to join our fast-growing team at {company}.
  You will work on cutting-edge projects using the latest technologies.
  
  {W}Requirements:{RS}
  - 3+ years of experience in {random.choice(['Python','Java','Go','Rust','C++'])}
  - Strong problem-solving skills
  - Experience with {random.choice(['AWS','Azure','GCP','Kubernetes','Docker'])}
  - Excellent communication skills
  
  {W}How to Apply:{RS}
  Send your resume to careers@{company.lower().replace(' ','')}.com
  Include "Application - {position}" in the subject line.""")
    
    print(f"\n{Y}[!] Use this for phishing campaigns targeting job seekers{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def impersonation_checklist():
    """Tool 11: Impersonation Checklist Generator"""
    print(f"\n{G}[+] Impersonation Preparation Checklist{RS}")
    target_role = input(f"  {W}[?] Role to impersonate (e.g., IT Support, Bank Manager): {RS}").strip()
    
    print(f"\n{G}[+] Checklist for impersonating {target_role}:{RS}")
    checklist = [
        f"Research {target_role} terminology and jargon",
        f"Prepare a believable backstory",
        f"Get appropriate contact information (spoofed number/email)",
        f"Practice tone of voice and speaking patterns",
        f"Prepare answers for common questions",
        f"Have documentation or fake credentials ready",
        f"Know the organization's internal structure",
        f"Prepare urgency hooks (security breach, account issue)",
        f"Set up callback number or voicemail",
        f"Plan exit strategy if detected",
        f"Prepare data collection mechanism",
        f"Test the scenario with a colleague first"
    ]
    for i, item in enumerate(checklist, 1):
        print(f"  {W}{i:02d}.{RS} {Y}☐ {item}{RS}")
    
    print(f"\n{Y}[!] Always have a cover story ready if questioned{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")

def vishing_scripts():
    """Tool 12: Vishing (Voice Phishing) Scripts"""
    print(f"\n{G}[+] Vishing Call Scripts{RS}")
    print(f"\n{W}Select scenario:{RS}")
    print(f"  {W}[1]{RS} Bank Security Alert")
    print(f"  {W}[2]{RS} IRS/Tax Scam")
    print(f"  {W}[3]{RS} Tech Support Scam")
    print(f"  {W}[4]{RS} Lottery/Prize Scam")
    print(f"  {W}[5]{RS} Romance Scam")
    print(f"  {W}[6]{RS} Grandparent Scam")
    
    ch = input(f"\n{Y}  Choice: {RS}").strip()
    
    scripts = {
        '1': f'''{Y}Bank Security Alert Vishing Script:{RS}
  
  Agent: "Hello, this is {random.choice(['John','Sarah','Mike','Emily'])} from {random.choice(['Chase','Bank of America','Wells Fargo','Citi'])} Fraud Department.
  We've detected unusual activity on your account. A transaction of ${random.randint(100,5000)} was attempted from {random.choice(['Russia','Nigeria','Brazil','India','China'])}.
  To verify your identity, can you please confirm your account number and the last 4 digits of your SSN?"
  
  If target hesitates:
  "I understand your concern. You can call us back at the number on your card, but this matter needs immediate attention to prevent fund loss."
  ''',
        '2': f'''{Y}IRS Tax Scam Script:{RS}
  
  Agent: "This is Officer {random.choice(['Williams','Anderson','Roberts'])} from the IRS Tax Collection Department.
  Our records show you have an unpaid tax balance of ${random.randint(1000,15000)} from {random.randint(2019,2023)}.
  A warrant for your arrest has been issued. To avoid immediate detention, you must pay the balance using a wire transfer or gift cards."
  ''',
        '3': f'''{Y}Tech Support Scam Script:{RS}
  
  Agent: "Hi, I'm {random.choice(['David','Lisa','Tom'])} from Microsoft Windows Support.
  We've detected {random.randint(10,500)} critical errors on your computer. Your IP address has been compromised.
  Let me show you how to fix this. First, open the Event Viewer... I'll guide you through the process.
  Our security package is ${random.randint(99,499)} for a 3-year license."
  ''',
        '4': f'''{Y}Lottery Scam Script:{RS}
  
  Agent: "Congratulations! You've won ${random.randint(10000,5000000)} in the {random.choice(['Publishers Clearing House','International Lottery','Google Sweepstakes','Facebook Lottery'])}!
  To claim your prize, you need to pay a processing fee of ${random.randint(50,500)} via wire transfer or gift card.
  The prize will be delivered within 24 hours of payment confirmation."
  ''',
        '5': f'''{Y}Romance Scam Script:{RS}
  
  Agent: "Hi beautiful/handsome, I saw your profile and couldn't resist messaging you.
  I'm a {random.choice(['military officer','oil rig worker','doctor','engineer'])} currently stationed in {random.choice(['Syria','Yemen','Afghanistan','offshore rig'])}.
  I'd love to get to know you better. Can we chat on WhatsApp/Telegram?
  (After building relationship for weeks) I need help with {random.choice(['a medical emergency','travel fees to visit you','customs charges for a gift'])}..."
  ''',
        '6': f'''{Y}Grandparent Scam Script:{RS}
  
  Agent: "Grandma/Grandpa? It's me, {random.choice(['your grandson','your granddaughter','Tommy','Sarah'])}.
  I'm in trouble! I was in a car accident / arrested / robbed in {random.choice(['Canada','Mexico','another state'])}.
  I need ${random.randint(1000,10000)} for {random.choice(['bail','hospital bills','a repair','a lawyer'])}.
  Please don't tell mom and dad - they'll be so angry. Can you wire the money? I'll pay you back."
  '''
    }
    
    if ch in scripts:
        print(scripts[ch])
    else:
        print(f"{R}[-] Unknown scenario{RS}")
    
    print(f"\n{R}[!] Vishing is illegal without consent. For educational purposes only.{RS}")
    input(f"\n{Y}[+] Press Enter to continue...{RS}")
