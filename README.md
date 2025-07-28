# 🛡️ XSS Scanner Tool

A Python-based tool to detect **Reflected XSS vulnerabilities** in web applications using URL parameters and HTML forms.

---

## 🚀 Features

* 🔍 Crawls and extracts all links from a given webpage
* 💉 Tests query parameters for reflected XSS
* 📝 Optionally scans HTML `<form>` elements (GET & POST)
* 🎯 Multiple payloads injected automatically
* 🎨 Color-coded terminal output
* 🧰 No browser automation needed (pure Python)

---

## 📦 Requirements

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

`requirements.txt` contents:

```
requests>=2.25.0
beautifulsoup4>=4.9.0
```

---

## ⚙️ Run the script

```bash
python xss_scanner.py
```

### 🧱 You will be prompted to:

1. Enter the **target URL**
2. Choose whether to scan HTML forms

#### 🧪 Example interaction:

```
Enter the target URL (e.g. https://example.com): https://vulnerable.site
Do you want to scan forms on the base page for XSS? (yes/no): yes
```

---

## 📤 Example Output

```
[+] Found 8 links on the page.
[*] Testing: https://example.com/search?q=test
[✓] Clean: https://example.com/search?q=<script>alert(1)</script>
[!] XSS Found: https://example.com/search?q=<svg/onload=alert(1)>
    Payload: <svg/onload=alert(1)>
```

---

## ⚠️ Disclaimer

This tool is for **educational and authorized testing only**.
Do not scan or attack websites without **explicit permission**.
The author is **not responsible** for any misuse of this tool.

---

## 👤 Author

Developed by [@youssef-mo55](https://github.com/youssef-mo55)
Pull requests, issues, and contributions are welcome!
