#!/usr/bin/env python3
import os, sys, time, random
from colorama import Fore, Style, init; init(autoreset=True)
R=Fore.RED;G=Fore.GREEN;Y=Fore.YELLOW;B=Fore.BLUE;M=Fore.MAGENTA;C=Fore.CYAN;W=Fore.WHITE;RS=Style.RESET_ALL
IS_WINDOWS=os.name=='nt'

def pretext_gen():
    print(f"\n{Y}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}Pretext Generator{R}                                    {Y}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    pretexts={
        'IT Support':'Calling from IT support. We detected a virus. Need to install remote access tool.',
        'HR Manager':'This is HR. Updating portal. Verify credentials for bonus processing.',
        'CEO':'This is CEO. Urgent meeting. Need you to transfer funds immediately.',
        'Receptionist':'Delivery driver lost. Need building access for package drop.',
        'System Admin':'Security audit. Need network credentials for access verification.',
        'Help Desk':'Account locked. Need identity verification to unlock.',
        'Security Guard':'Fire inspection. Need server room access.',
    }
    target=random.choice(list(pretexts.keys()))
    pretext=pretexts[target]
    print(f"\n{G}[+] Target Role: {W}{target}{RS}")
    print(f"{G}[+] Pretext: {W}{pretext}{RS}")
    name=input(f"\n{Y}  Target Name: {RS}").strip()
    if name:
        pretext=pretext.replace('[Target Name]',name).replace('[CEO Name]',name)
    print(f"\n{G}[+] Customized:\n{W}{pretext}{RS}")
    input(f"\n{Y}[+] Press Enter...{RS}")

def osint_prep():
    print(f"\n{Y}╔═══════════════════════════════════════════════════════╗")
    print(f"║  {W}OSINT Prep{R}                                           {Y}║")
    print(f"╚═══════════════════════════════════════════════════════╝{RS}")
    target=input(f"{Y}  Target: {RS}").strip()
    if target:
        print(f"\n{G}[+] OSINT on {target}{RS}")
        for i in ['Email','Social media','Phone','Address','Job','Interests']:
            print(f"  {Y}->{RS} Check {i}")
        if '@' in target:
            print(f"  {W}theHarvester: theharvester -d {target.split('@')[-1]} -b google{RS}")
        print(f"  {W}Sherlock: sherlock {target}{RS}")
    input(f"\n{Y}[+] Press Enter...{RS}")

def menu():
    while True:
        os.system('cls' if IS_WINDOWS else 'clear')
        print(f"""{M}
  ╔═══════════════════════════════════════════════════════╗
  ║  {W}A2Tool - Social Engineering{R}                         {M}║
  ╠═══════════════════════════════════════════════════════╣
  ║  {W}[1] {R}Pretext Generator                                {M}║
  ║  {W}[2] {R}Call Scripts                                     {M}║
  ║  {W}[3] {R}OSINT Prep                                       {M}║
  ║  {W}[4] {R}Delivery Methods                                 {M}║
  ║  {W}[5] {R}USB Drop Attack Guide                            {M}║
  ║  {W}[6] {R}Quid Pro Quo Guide                               {M}║
  ║  {W}[7] {R}Tailgating Guide                                 {M}║
  ║  {W}[8] {R}Impersonation Checklist                          {M}║
  ║  {W}[0] {R}Back to Main                                    {M}║
  ╚═══════════════════════════════════════════════════════╝
{RS}""")
        choice=input(f"{Y}  A2Tool[SE] » {RS}").strip()
        if choice=='0': break
        elif choice=='1': pretext_gen()
        elif choice=='2':
            print(f"\n{C}[*] Call Scripts:{RS}")
            print(f"  {W}Tech Support:{RS} Claim virus. Guide to install remote tool.")
            print(f"  {W}HR:{RS} Payroll update. Ask for employee ID, DOB, bank details.")
            print(f"  {W}Vendor:{RS} Invoice issue. Ask for banking details.")
            print(f"  {W}Security:{RS} Breach detected. Ask for credentials.")
            print(f"  {W}Survey:{RS} Offer gift card. Ask for personal info.")
            input(f"\n{Y}[+] Press Enter...{RS}")
        elif choice=='3': osint_prep()
        elif choice=='4':
            print(f"\n{C}[*] Delivery Methods:{RS}")
            methods=[('USB Drop','Leave infected USB drives labeled Confidential near entrance'),
                     ('Email','Phishing with macro-enabled document'),
                     ('Watering Hole','Compromise a website target visits'),
                     ('Fake Update','Serve fake Flash/Chrome update popup'),
                     ('SMS Link','Send malicious link via SMS'),
                     ('QR Code','Place malicious QR on posters')]
            for i,(n,d) in enumerate(methods,1):
                print(f"  {Y}[{i}]{RS} {W}{n}{RS} - {d}")
            input(f"\n{Y}[+] Press Enter...{RS}")
        elif choice=='5':
            print(f"\n{C}[*] USB Drop Attack:{RS}")
            print(f"  1. Buy cheap USB drives\n  2. Create autorun payload\n  3. Label professionally\n  4. Drop near building entrance\n  5. Wait for target to plug in\n{Y}[!] Success: 40-60%{RS}")
            input(f"\n{Y}[+] Press Enter...{RS}")
        elif choice=='6':
            print(f"\n{C}[*] Quid Pro Quo: Offer service/gift in exchange for info/access{Y}")
            print(f"  Examples: IT help for creds, gift card for survey, free tool install{Y}")
            input(f"\n{Y}[+] Press Enter...{RS}")
        elif choice=='7':
            print(f"\n{C}[*] Tailgating Methods:{RS}")
            print(f"  1. Look busy (carry boxes, phone to ear)\n  2. Follow through secured door\n  3. Claim forgot badge\n  4. Pretend delivery\n{Y}[!] Success: 70%+{RS}")
            input(f"\n{Y}[+] Press Enter...{RS}")
        elif choice=='8':
            print(f"\n{C}[*] Impersonation Checklist:{RS}")
            print(f"  - Research company thoroughly\n  - Dress appropriately (uniform if needed)\n  - Use correct jargon\n  - Have fake ID/business card ready\n  - Sound confident and rushed\n  - Have believable reason")
            input(f"\n{Y}[+] Press Enter...{RS}")
        else: print(f"{R}[!] Invalid.{RS}"); time.sleep(1)

if __name__=='__main__': menu()
