# JSHound

**JSHound** is a recon tool designed for bug bounty hunters and pentesters.  
It helps you extract JavaScript files of a target domain from multiple sources (Wayback Machine, Common Crawl, urlscan.io), and then searches those files for potentially sensitive information such as API keys, tokens, credentials, and more.

---

## Features
- 🔍 Collect JavaScript files from:
  - [Archive.org (Wayback Machine)](https://archive.org)
  - [Common Crawl](https://commoncrawl.org)
  - [urlscan.io](https://urlscan.io)
- 📥 Download JavaScript files locally for offline analysis
- 🕵️ Search for sensitive patterns (API keys, tokens, secrets, passwords, etc.)
- 🎛️ Interactive terminal menu for workflow selection
- 📂 Organized output saved in `./targets/<domain>/result/result.txt`
- ✨ Customizable:
  - Skip unwanted JS files (frameworks, libraries, etc.)
  - Use your own regex wordlist for pattern matching

---

## Installation

```bash
# Clone this repository
git clone https://github.com/yourusername/JSHound.git
cd JSHound
pip3 install -r requirements.txt

```

## Usage
```bash
python jshound.py -d <domain>
```

### Options

- `-d` : Target domain (required)  
  **Example:** `-d example.com`
    
- `-pf` : Comma-separated list of paths to skip  
  **Example:** `-pf nuxt,node,jquery`
    
- `-pw` : Custom wordlist file containing regex patterns to search  
  **Example:** `-pw ./wordlists/patterns.txt`


## Output

All findings are saved in:
```
./targets/<domain>/result/result.txt
```

#### Each finding includes:
- The JS file path or URL
- The matching keyword/pattern
- Line number and line content

#### Notes
- By default, common libraries (React, Vue, jQuery, etc.) are skipped.
- SSL warnings are disabled for easier fetching of JS files.
- If no matches are found, the tool will exit gracefully.
