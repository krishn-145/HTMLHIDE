#!/data/data/com.termux/files/usr/bin/bash
set -e
BASE="$(cd "$(dirname "$0")" && pwd)"
cd "$BASE"

printf '\033[1;36m'
cat <<'BANNER'
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██╗  ██╗████████╗███╗   ███╗██╗      ███████╗██╗  ██╗    ║
║   ██║  ██║╚══██╔══╝████╗ ████║██║      ██╔════╝██║  ██║    ║
║   ███████║   ██║   ██╔████╔██║██║      ███████╗███████║    ║
║   ██╔══██║   ██║   ██║╚██╔╝██║██║      ╚════██║██╔══██║    ║
║   ██║  ██║   ██║   ██║ ╚═╝ ██║███████╗███████║██║  ██║    ║
║   ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝    ║
║                                                              ║
║       ADVANCED HTML • CSS • JAVASCRIPT PACKER               ║
║                  OFFLINE / TERMUX                           ║
╚══════════════════════════════════════════════════════════════╝
BANNER
printf '\033[0m\n'

command -v python >/dev/null 2>&1 || {
  printf '\033[1;31m[-] Python missing.\033[0m\n'
  echo "[*] Install with: pkg install python"
  exit 1
}

[ -f "$BASE/index.html" ] || {
  printf '\033[1;31m[-] index.html nahi mila.\033[0m\n'
  exit 1
}

python "$BASE/codehide.py" "$BASE/index.html" "$BASE/protected/index.html"
printf '\033[1;32m[+] BUILD SUCCESSFUL\033[0m\n'
echo "[+] Output: $BASE/protected/index.html"
