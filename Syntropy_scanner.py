#!/usr/bin/env python3
import subprocess
import sys
import re
import os
import shutil
from datetime import datetime

# --- CONFIGURATION ---
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_banner():
    print(f"{BLUE}=========================================================={RESET}")
    print(f"{BLUE}   SYNTROPY SECURITY :: COMPREHENSIVE SCANNER v2   {RESET}")
    print(f"{BLUE}=========================================================={RESET}")
    print(f"{YELLOW}[*] Intent: Leave No Stone Unturned.{RESET}")

def check_dependencies():
    tools = ["nmap", "rustscan", "xsltproc"]
    for tool in tools:
        if shutil.which(tool) is None:
            print(f"{RED}[!] Error: {tool} is not installed or not in PATH.{RESET}")
            sys.exit(1)

def run_command(command, show_output=False):
    """Runs a shell command and returns stdout."""
    try:
        if show_output:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            output = ""
            for line in process.stdout:
                sys.stdout.write(line)
                output += line
            process.wait()
            return output
        else:
            # We capture BOTH stdout and stderr to ensure we don't miss anything
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout + result.stderr
    except Exception as e:
        print(f"{RED}[!] Execution Error: {e}{RESET}")
        return ""

def extract_ports_nmap(nmap_output):
    ports = re.findall(r"(\d+)/tcp\s+open", nmap_output)
    return set(map(int, ports))

def extract_ports_rustscan_greppable(rust_output):
    """
    Parses Rustscan 'greppable' output.
    Format is usually: '10.10.10.10 -> [80, 443, 6520]' or just simple lines
    """
    # Strategy 1: Look for numbers inside brackets [80, 443]
    bracket_match = re.search(r"\[(.*?)\]", rust_output)
    if bracket_match:
        content = bracket_match.group(1)
        # Split by comma, strip whitespace, filter empty strings
        ports = [p.strip() for p in content.split(',') if p.strip().isdigit()]
        return set(map(int, ports))
    
    # Strategy 2: Fallback for different versions, look for any 'port' patterns
    # This finds all standalone numbers that might be ports if the bracket parse fails
    potential_ports = re.findall(r"\b(\d{1,5})\b", rust_output)
    # Filter out the IP address itself (rough heuristic: ports usually don't look like octets in this context)
    valid_ports = set()
    for p in potential_ports:
        if int(p) < 65536 and int(p) != 0: 
            valid_ports.add(int(p))
            
    return valid_ports

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <TARGET_IP>")
        sys.exit(1)

    target = sys.argv[1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_dir = f"scan_results_{target}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    print_banner()
    check_dependencies()
    
    print(f"\n{GREEN}[+] Target locked: {target}{RESET}")

    # --- STEP 1: FAST NMAP (Top 1000) ---
    print(f"\n{YELLOW}[1/4] Running Initial Fast Nmap (Top 1000 Ports)...{RESET}")
    nmap_fast_cmd = f"nmap -T4 -n {target}"
    nmap_fast_output = run_command(nmap_fast_cmd, show_output=True)
    nmap_ports = extract_ports_nmap(nmap_fast_output)
    print(f"{GREEN}    > Nmap found {len(nmap_ports)} ports.{RESET}")

    # --- STEP 2: RUSTSCAN (All Ports) ---
    print(f"\n{YELLOW}[2/4] Running Rustscan (Checking ALL 65,535 ports)...{RESET}")
    
    # CRITICAL CHANGE: Added '-g' for greppable output and explicit range
    # We use -g so it prints a list like [22, 80, 6520] which is easier to regex
    rust_cmd = f"rustscan -a {target} -r 1-65535 -g"
    
    print(f"{BLUE}    > Executing: {rust_cmd}{RESET}")
    rust_output = run_command(rust_cmd, show_output=False)
    
    # Debug: Print raw output if parsing seems empty (Safety check)
    rust_ports = extract_ports_rustscan_greppable(rust_output)
    
    if len(rust_ports) == 0:
        print(f"{RED}[!] WARNING: Rustscan returned 0 ports. Raw output below for debugging:{RESET}")
        print(rust_output)
    else:
        print(f"{GREEN}    > Rustscan raw count: {len(rust_ports)} ports found.{RESET}")

    # --- STEP 3: COMPARISON & INTELLIGENCE ---
    print(f"\n{BLUE}[3/4] Comparative Analysis{RESET}")
    
    missed_ports = rust_ports - nmap_ports
    combined_ports = rust_ports.union(nmap_ports)
    
    if missed_ports:
        print(f"{RED}[!] ALERT: Standard Nmap scan MISSED these ports:{RESET}")
        for p in sorted(list(missed_ports)):
            print(f"{RED}    -> {p}/tcp (Caught by Rustscan){RESET}")
    else:
        print(f"{GREEN}    > No hidden ports found outside top 1000.{RESET}")

    if not combined_ports:
        print(f"{RED}[!] No open ports found. Exiting.{RESET}")
        sys.exit(1)

    ports_str = ",".join(map(str, combined_ports))
    print(f"{GREEN}    > Consolidated Port List: {ports_str}{RESET}")

    # --- STEP 4: INTENSE SCAN ---
    print(f"\n{YELLOW}[4/4] Starting Comprehensive Deep Scan on Open Ports...{RESET}")
    print(f"{YELLOW}    > Scanning: {ports_str}{RESET}")
    
    deep_cmd = f"nmap -p {ports_str} -sC -sV -O -oA {output_dir}/comprehensive {target}"
    run_command(deep_cmd, show_output=True)

    # --- STEP 5: HTML REPORT ---
    print(f"\n{BLUE}[*] Generating HTML Report...{RESET}")
    # Fix: Ensure absolute path usage or check if file exists
    xml_output = f"{output_dir}/comprehensive.xml"
    html_output = f"{output_dir}/report.html"
    
    if os.path.exists(xml_output):
        run_command(f"xsltproc {xml_output} -o {html_output}")
        print(f"{GREEN}[+] Report Ready: {html_output}{RESET}")
    else:
        print(f"{RED}[!] Error: XML file not found. Scan might have failed.{RESET}")

if __name__ == "__main__":
    main()
