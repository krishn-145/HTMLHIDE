#!/data/data/com.termux/files/usr/bin/bash
"clear"
#====clear====
echo -e "\e[1;32m"
figlet "HTML" | lolcat
echo -e "\e[0m"
printf '\033[1;34m[*] </> : FOLLW IN INSTAGRAM: ur_.krishn._02\033[0m\n'
printf '\033[1;36m[✓] HTML CSS JS JAVASCRIP\033[0m\n'
printf '\033[1;35m[*] Update...\033[0m\n'
pkg install python -y 
set -e
BASE="$(cd "$(dirname "$0")" && pwd)"
chmod +x "$BASE/htmlshield.sh" "$BASE/codehide.py"
printf '\033[1;32m[+] HTMLShield Advanced ready.\033[0m\n'
echo "Put index.html in: $BASE"
echo "Then run: bash $BASE/htmlshield.sh"
