# Syntropy Scanner

A smart, two-stage network scanner that automates the "discovery" phase of a penetration test. It bridges the gap between speed and thoroughness by combining Nmap's reliability with Rustscan's raw speed.

## Why I Built This
We have all been there. You run a standard Nmap scan, see ports 80 and 445, and start attacking. Hours later, you realize the target is rock solid. You finally decide to run a full port scan and discover a hidden administration console on port 6520 that gives you an easy shell.

I built Syntropy Scanner after missing a non-standard port during an engagement. I wanted a tool that would ensure I never miss a "hidden" port again, without forcing me to wait 2 hours for a full Nmap scan to finish.

## How It Works
This script automates a specific methodology designed to "leave no stone unturned" while respecting your time:

1. **The Fast Check:** Immediately scans the top 1,000 TCP ports using Nmap to give you initial data to work with.
2. **The Full Sweep:** Simultaneously runs `Rustscan` in the background on all 65,535 ports.
3. **The Gap Analysis:** This is the core feature. The script mathematically compares the Nmap results against the Rustscan results. If Rustscan finds a port that Nmap missed (like 6520), it highlights it as an "Anomaly" in the console.
4. **The Deep Dive:** It automatically aggregates all found ports and runs a comprehensive Nmap scan (`-sC -sV -O`) on just those specific targets.
5. **UDP Support:** Includes an optional module to scan the top 1,000 UDP ports if you need a complete picture.

## Prerequisites
To run this tool, you need a standard penetration testing environment (like Kali Linux or Parrot OS) with the following installed:

* python3
* nmap
* xsltproc (for generating the HTML reports)
* rustscan (needs to be installed and in your system PATH)

## Installation

Clone the repository and make the script executable:

git clone https://github.com/YOUR_USERNAME/Syntropy-Scanner.git
cd Syntropy-Scanner
chmod +x syntropy_scanner.py

## Usage

Since the script performs OS detection and UDP scanning, it requires root privileges.

sudo python3 syntropy_scanner.py <TARGET_IP>

## Features & Output
* **Real-time Feedback:** You see the results of the fast scan immediately.
* **Firewall Bypass:** Automatically applies `-Pn` to all scans to handle Windows targets that block ping probes.
* **Report Generation:** Creates a neat folder for every scan containing:
    * `report.html`: A clean, dark-themed HTML report you can drop into your notes.
    * `comprehensive.xml`: XML data for importing into tools like Metasploit or Faraday.
    * `comprehensive.nmap`: The raw grepable output.

## Disclaimer
This tool is intended for legal security auditing and penetration testing on networks you have authorization to scan. Please use responsibly.
