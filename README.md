# 🛡️ Syntropy Scanner
> **/// LEAVE NO STONE UNTURNED ///**

## 💀 The Problem
You are in a CTF or a Pentest. You run a standard `nmap` scan. It checks the top 1,000 ports. You see port 80 and 445. You attack them for 3 hours and get nowhere.

**The Reality:** The target had a hidden administrative console on **Port 6520**. Nmap missed it. You missed the shell.

## ⚡ The Solution
**Syntropy Scanner** automates the "Discovery" phase of a penetration test. It runs two scans simultaneously (Fast Nmap + Full Rustscan) and performs a **Gap Analysis**. If Rustscan finds a port that Nmap missed, it triggers a **RED ALERT**.

### Now Available in Two Editions:

| Feature | 🟢 Standard Edition (`Syntropy_scanner.py`) | 🔴 Ultimate Edition (`Syntropy_Scanner_Ultimate.py`) |
| :--- | :---: | :---: |
| **Speed** | ⚡ Instant | 🐢 Slower (Deep Analysis) |
| **Gap Analysis** | ✅ Yes | ✅ Yes |
| **Visual Dashboard** | ❌ No | ✅ **Pro Console UI** |
| **UDP Support** | ❌ No | ✅ **Optional Module** |
| **Root Required** | ❌ No | ✅ Yes (For UDP/OS Detect) |

## 📸 Professional Reporting
Don't just stare at terminal output. Syntropy generates clean HTML report for every scan—perfect for documentation on pentest reports.

## 🚀 Installation

**Prerequisites:**
* `python3`
* `nmap`
* `rustscan` ([Install Guide](https://github.com/RustScan/RustScan))
* `xsltproc` (Required for HTML reports: `sudo apt install xsltproc`)

```bash
# 1. Clone the repository
# 2. Enter directory
cd Syntropy-Scanner
# 3. Make scripts executable
chmod +x *.py
```

## ⚔️ Usage

### Option A: Standard Edition (Fast & Stable)

Best for quick CTF checks or when you don't have root access.

Bash

```
python3 Syntropy_scanner.py <TARGET_IP>

```

### Option B: Ultimate Edition (The "Pro" Experience)

Includes the Dashboard, OS Detection, and the optional UDP Scan module. _Requires Sudo._

Bash

```
sudo python3 Syntropy_Scanner_Ultimate.py <TARGET_IP>

```

## 📂 Output Artifacts

For every scan, a timestamped folder is created containing:

-   `*_report.html` - The dark-mode HTML report.
    
-   `*_scan.xml` - XML format for importing into Metasploit/Faraday.
    
-   `*_scan.nmap` - Raw grepable output.
    

----------

_Built with 💀 by Syntropy Security._

