#!/bin/bash
# ============================================================
#  A2Tool v4.0 - Linux/macOS/Termux Launcher
#  Ultimate All-in-One Penetration Testing Suite
#  Author: Ayush Rajdev & Anzar Iqbal
# ============================================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo " ============================================================"
echo "     A2Tool v4.0 - Ultimate Penetration Testing Suite"
echo "     Author: Ayush Rajdev & Anzar Iqbal"
echo " ============================================================"
echo -e "${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 is not installed!${NC}"
    echo -e "${YELLOW}[INFO] Install using: pkg install python (Termux)"
    echo -e "${YELLOW}[INFO] Or: apt install python3 (Linux)${NC}"
    exit 1
fi

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Auto-install dependencies
echo -e "${GREEN}[*] Checking dependencies...${NC}"
pip3 install -r requirements.txt --quiet --break-system-packages 2>/dev/null
echo -e "${GREEN}[+] Dependencies ready!${NC}"

# Run A2Tool
echo -e "${GREEN}[*] Starting A2Tool...${NC}"
python3 A2Tool.py

if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR] Failed to start A2Tool${NC}"
    exit 1
fi
