import os
import sys
import re
import getpass
import socket
import uuid
import time
import json
import subprocess
from datetime import datetime
from urllib.parse import urljoin, urlparse, quote_plus, unquote

import requests
from bs4 import BeautifulSoup

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================= COLOR =================
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def visible_len(s: str) -> int:
    return len(re.sub(r"\033\[[0-9;]*m", "", s))


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


# ================= UI =================
def header():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    left = f"{C.GREEN}{C.BOLD}▸ X-EYELESS v1.0{C.RESET}"
    right = f"{C.GREEN}{now}{C.RESET}"
    print(f"{left}  {C.DIM}{C.GREEN}{'─' * 40}{C.RESET}  {right}")
    print()


def banner():
    art = [
        "⠀⠀⠀⠀⡀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⢸⠉⣹⠋⠉⢉⡟⢩⢋⠋⣽⡻⠭⢽⢉⠯⠭⠭⠭⢽⡍⢹⡍⠙⣯⠉⠉⠉⠉⠉⣿⢫⠉⠉⠉⢉⡟⠉⢿⢹⠉⢉⣉⢿⡝⡉⢩⢿⣻⢍⠉⠉⠩⢹⣟⡏⠉⠹⡉⢻⡍⡇",
        "⠀⢸⢠⢹⠀⠀⢸⠁⣼⠀⣼⡝⠀⠀⢸⠘⠀⠀⠀⠀⠈⢿⠀⡟⡄⠹⣣⠀⠀⠐⠀⢸⡘⡄⣤⠀⡼⠁⠀⢺⡘⠉⠀⠀⠀⠫⣪⣌⡌⢳⡻⣦⠀⠀⢃⡽⡼⡀⠀⢣⢸⠸⡇",
        "⠀⢸⡸⢸⠀⠀⣿⠀⣇⢠⡿⠀⠀⠀⠸⡇⠀⠀⠀⠀⠀⠘⢇⠸⠘⡀⠻⣇⠀⠀⠄⠀⡇⢣⢛⠀⡇⠀⠀⣸⠇⠀⠀⠀⠀⠀⠘⠄⢻⡀⠻⣻⣧⠀⠀⠃⢧⡇⠀⢸⢸⡇⡇",
        "⠀⢸⡇⢸⣠⠀⣿⢠⣿⡾⠁⠀⢀⡀⠤⢇⣀⣐⣀⠀⠤⢀⠈⠢⡡⡈⢦⡙⣷⡀⠀⠀⢿⠈⢻⣡⠁⠀⢀⠏⠀⠀⠀⢀⠀⠄⣀⣐⣀⣙⠢⡌⣻⣷⡀⢹⢸⡅⠀⢸⠸⡇⡇",
        "⠀⢸⡇⢸⣟⠀⢿⢸⡿⠀⣀⣶⣷⣾⡿⠿⣿⣿⣿⣿⣿⣶⣬⡀⠐⠰⣄⠙⠪⣻⣦⡀⠘⣧⠀⠙⠄⠀⠀⠀⠀⠀⣨⣴⣾⣿⠿⣿⣿⣿⣿⣿⣶⣯⣿⣼⢼⡇⠀⢸⡇⡇⡇",
        "⠀⢸⢧⠀⣿⡅⢸⣼⡷⣾⣿⡟⠋⣿⠓⢲⣿⣿⣿⡟⠙⣿⠛⢯⡳⡀⠈⠓⠄⡈⠚⠿⣧⣌⢧⠀⠀⠀⠀⠀⣠⣺⠟⢫⡿⠓⢺⣿⣿⣿⠏⠙⣏⠛⣿⣿⣾⡇⢀⡿⢠⠀⡇",
        "⠀⢸⢸⠀⢹⣷⡀⢿⡁⠀⠻⣇⠀⣇⠀⠘⣿⣿⡿⠁⠐⣉⡀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠳⠄⠀⠀⠀⠀⠋⠀⠘⡇⠀⠸⣿⣿⠟⠀⢈⣉⢠⡿⠁⣼⠁⣼⠃⣼⠀⡇",
        "⠀⢸⠸⣀⠈⣯⢳⡘⣇⠀⠀⠈⡂⣜⣆⡀⠀⠀⢀⣀⡴⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢽⣆⣀⠀⠀⠀⣀⣜⠕⡊⠀⣸⠇⣼⡟⢠⠏⠀⡇",
        "⠀⢸⠀⡟⠀⢸⡆⢹⡜⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠋⣾⡏⡇⡎⡇⠀⡇",
        "⠀⢸⠀⢃⡆⠀⢿⡄⠑⢽⣄⠀⠀⠀⢀⠂⠠⢁⠈⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠄⡐⢀⠂⠀⠀⣠⣮⡟⢹⣯⣸⣱⠁⠀⡇",
        "⠀⠈⠉⠉⠋⠉⠉⠋⠉⠉⠉⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠋⡟⠉⠉⡿⠋⠋⠋⠉⠉⠁",
    ]
    for line in art:
        print(f"{C.GREEN}{line}{C.RESET}")
    print()
    print(f"{C.GREEN}{C.BOLD}{'X - E Y E L E S S'.center(60)}{C.RESET}")
    print(f"{C.GREEN}{'Ultimate Tool Kit Launcher'.center(60)}{C.RESET}")
    print(f"{C.GREEN}{C.DIM}{'coded by DexXShoot'.center(60)}{C.RESET}")
    print()


def info_table():
    user = getpass.getuser() or os.getenv("USER", "unknown")
    ip = get_local_ip()
    uid = uuid.getnode()
    rows = [
        ("Dev",     "DexXTools"),
        ("Contact", "t.me/DexXShoot"),
        ("User",    user),
        ("IP",      ip),
        ("ID",      str(uid)),
        ("Status",  "admin"),
    ]
    for k, v in rows:
        key = f"{C.GREEN}{C.BOLD}{k:<10}{C.RESET}"
        val = f"{C.WHITE}{v}{C.RESET}"
        print(f"  {key} : {val}")
    print()


def menu():
    print(f"{C.GREEN}{C.BOLD}  ┌─ MENU ─────────────────────────────┐{C.RESET}")
    items = [
        ("01", "Email Crawl"),
        ("02", "Google Dorking"),
        ("03", "IP Lookup"),
        ("04", "URL to HTML"),
        ("00", "Exit"),
    ]
    for num, name in items:
        num_str = f"{C.GREEN}{C.BOLD}[{num}]{C.RESET}"
        name_str = f"{C.WHITE}{name}{C.RESET}"
        print(f"  {num_str} {name_str}")
    print(f"{C.GREEN}{C.BOLD}  └────────────────────────────────────┘{C.RESET}")


# ================= SHARED =================
EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def extract_emails(text: str) -> set:
    return set(re.findall(EMAIL_REGEX, text))


def fetch(url: str, timeout: int = 10) -> str:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, verify=False)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        print(f"{C.RED}  [!] Failed to fetch {url}: {e}{C.RESET}")
        return ""


def save_lines(fname: str, lines: list, header_lines: list = None):
    with open(fname, "w", encoding="utf-8") as f:
        if header_lines:
            for h in header_lines:
                f.write(f"# {h}\n")
            f.write("\n")
        f.write("\n".join(lines))
    print(f"  {C.GREEN}✓ Saved to: {fname}{C.RESET}")


# ================= EMAIL CRAWLER =================
def crawl_website(start_url: str, max_pages: int = 20, same_domain: bool = True) -> set:
    visited, to_visit = set(), [start_url]
    found = set()
    base_domain = urlparse(start_url).netloc

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        print(f"{C.GREEN}  ▸ Crawling ({len(visited)}/{max_pages}): {C.WHITE}{url}{C.RESET}")
        html = fetch(url)
        if not html:
            continue

        found |= extract_emails(html)

        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("mailto:"):
                em = href.replace("mailto:", "").split("?")[0].strip()
                if re.match(EMAIL_REGEX, em):
                    found.add(em)

            link = urljoin(url, href)
            p = urlparse(link)
            if p.scheme not in ("http", "https"):
                continue
            if same_domain and p.netloc != base_domain:
                continue
            if link not in visited:
                to_visit.append(link)

        time.sleep(0.5)

    return found


def run_email_crawl():
    clear()
    header()
    print(f"{C.GREEN}{C.BOLD}  ▸ Email Crawl{C.RESET}")
    print(f"  {C.DIM}Crawl a website and collect all email addresses.{C.RESET}\n")

    target = input(f"  {C.GREEN}Target URL{C.RESET} (e.g. https://example.com) : ").strip()
    if not target:
        print(f"{C.RED}  [!] Empty URL.{C.RESET}")
        input(f"\n  {C.DIM}Press ENTER to continue...{C.RESET}")
        return

    if not target.startswith(("http://", "https://")):
        target = "https://" + target

    try:
        pages = int(input(f"  {C.GREEN}Max pages{C.RESET} (default 20) : ").strip() or "20")
    except ValueError:
        pages = 20

    print()
    emails = crawl_website(target, max_pages=pages)

    print(f"\n{C.GREEN}{C.BOLD}  ═══ RESULT ═══{C.RESET}")
    if emails:
        for e in sorted(emails):
            print(f"  {C.GREEN}✓{C.RESET} {C.WHITE}{e}{C.RESET}")
        print(f"\n  {C.GREEN}Total: {C.BOLD}{len(emails)}{C.RESET} emails found")

        save = input(f"\n  {C.GREEN}Save to file? (y/n){C.RESET} : ").strip().lower()
        if save == "y":
            fname = f"emails_{int(time.time())}.txt"
            save_lines(fname, sorted(emails), [
                f"Target: {target}",
                f"Time  : {datetime.now()}",
            ])
    else:
        print(f"  {C.YELLOW}No emails found.{C.RESET}")

    input(f"\n  {C.DIM}Press ENTER to continue...{C.RESET}")


# ================= GOOGLE DORKING =================
DORK_PRESETS = {
    "01": ("Common emails (gmail/yahoo/outlook)", 'site:{target} "@gmail.com" OR "@yahoo.com" OR "@outlook.com"', "Email"),
    "02": ("Emails from public files",            'site:{target} filetype:pdf OR filetype:doc OR filetype:xls "@"', "Email"),
    "03": ("Contact pages",                       'site:{target} inurl:contact OR inurl:kontak OR inurl:about', "Email"),
    "04": ("Staff / team emails",                 'site:{target} inurl:staff OR inurl:team OR inurl:employee', "Email"),

    "05": ("PDF documents",                       'site:{target} filetype:pdf', "Sensitive Files"),
    "06": ("Excel spreadsheets",                  'site:{target} filetype:xls OR filetype:xlsx OR filetype:csv', "Sensitive Files"),
    "07": ("Word documents",                      'site:{target} filetype:doc OR filetype:docx', "Sensitive Files"),
    "08": ("PowerPoint files",                    'site:{target} filetype:ppt OR filetype:pptx', "Sensitive Files"),
    "09": ("Open text files",                     'site:{target} filetype:txt', "Sensitive Files"),
    "10": ("JSON / XML files",                    'site:{target} filetype:json OR filetype:xml', "Sensitive Files"),

    "11": ("Leaked .env files",                   'site:{target} filetype:env OR inurl:.env', "Credentials"),
    "12": ("Config files",                        'site:{target} filetype:conf OR filetype:config OR filetype:cfg OR filetype:ini', "Credentials"),
    "13": ("Password / credential files",         'site:{target} inurl:password OR inurl:passwd OR inurl:credentials', "Credentials"),
    "14": ("SSH keys / private keys",             'site:{target} filetype:pem OR filetype:key OR filetype:ppk', "Credentials"),
    "15": ("Log files",                           'site:{target} filetype:log', "Credentials"),
    "16": ("Database dumps / SQL",                'site:{target} filetype:sql OR inurl:dump.sql OR inurl:database', "Credentials"),

    "17": ("Backup files",                        'site:{target} inurl:backup OR inurl:bak OR filetype:bak', "Backup"),
    "18": ("Zip / RAR / TAR archives",            'site:{target} filetype:zip OR filetype:rar OR filetype:tar OR filetype:gz OR filetype:7z', "Backup"),
    "19": ("Database backups",                    'site:{target} (filetype:sql OR filetype:db OR filetype:sqlite) (backup OR dump)', "Backup"),
    "20": ("Old / temp files",                    'site:{target} inurl:old OR inurl:temp OR inurl:tmp OR filetype:old', "Backup"),

    "21": ("Admin panels",                        'site:{target} inurl:admin OR inurl:administrator OR inurl:adminpanel', "Panels"),
    "22": ("Login pages",                         'site:{target} inurl:login OR inurl:signin OR inurl:auth', "Panels"),
    "23": ("PHPMyAdmin",                          'site:{target} inurl:phpmyadmin OR inurl:pma OR inurl:mysql', "Panels"),
    "24": ("cPanel / WHM / Webmail",              'site:{target} inurl:cpanel OR inurl:whm OR inurl:webmail', "Panels"),
    "25": ("Dashboards / consoles",               'site:{target} inurl:dashboard OR inurl:panel OR inurl:console', "Panels"),

    "26": ("Open directory listing",              'site:{target} intitle:"index of"', "Directory"),
    "27": ("Index of - backup",                   'site:{target} intitle:"index of" backup', "Directory"),
    "28": ("Index of - password",                 'site:{target} intitle:"index of" password', "Directory"),
    "29": ("Index of - config",                   'site:{target} intitle:"index of" config', "Directory"),
    "30": ("Index of - db",                       'site:{target} intitle:"index of" db OR database', "Directory"),

    "31": ("Source code files",                   'site:{target} filetype:php OR filetype:asp OR filetype:jsp OR filetype:py OR filetype:rb', "Source Code"),
    "32": ("Leaked Git / SVN",                    'site:{target} inurl:.git OR inurl:.svn OR inurl:.hg', "Source Code"),
    "33": ("Composer / package files",            'site:{target} (filetype:json) (composer OR package OR requirements)', "Source Code"),
    "34": ("Docker / Kubernetes configs",         'site:{target} (filetype:yml OR filetype:yaml) (docker OR kubernetes OR k8s)', "Source Code"),

    "35": ("Common subdomains",                   'site:*.{target}', "Subdomain"),
    "36": ("Dev / staging subdomains",            'site:{target} inurl:dev OR inurl:staging OR inurl:test OR inurl:demo', "Subdomain"),
    "37": ("API endpoints",                       'site:{target} inurl:api OR inurl:v1 OR inurl:v2 OR inurl:graphql', "Subdomain"),

    "38": ("Error / debug pages",                 'site:{target} inurl:error OR inurl:debug OR inurl:trace OR inurl:warning', "Debug"),
    "39": ("Stack trace / PHP info",              'site:{target} (inurl:phpinfo OR intitle:"phpinfo()" OR inurl:traceback)', "Debug"),
    "40": ("Open error logs",                     'site:{target} (filetype:log OR inurl:error.log OR inurl:debug.log)', "Debug"),

    "99": ("Custom dork (manual input)",          None, "Custom"),
}


def show_dork_menu():
    print(f"\n{C.GREEN}{C.BOLD}  ╔═ DORK PRESETS ═════════════════════════════════════════════╗{C.RESET}")
    current_cat = None
    for key, (name, _, cat) in DORK_PRESETS.items():
        if cat != current_cat:
            current_cat = cat
            print(f"\n  {C.GREEN}{C.BOLD}  ── {cat} ──{C.RESET}")
        num_display = key.lstrip("0") or "0"
        print(f"  {C.GREEN}[{num_display:>2}]{C.RESET} {C.WHITE}{name}{C.RESET}")
    print(f"\n{C.GREEN}{C.BOLD}  ╚════════════════════════════════════════════════════════════╝{C.RESET}")


def search_duckduckgo(query: str, max_results: int = 20) -> list:
    results = []
    url = "https://html.duckduckgo.com/html/"
    try:
        r = requests.post(url, data={"q": query}, headers=HEADERS,
                          timeout=15, verify=False)
        if r.status_code == 202:
            print(f"{C.YELLOW}  [!] DuckDuckGo rate-limited (HTTP 202). Try again later.{C.RESET}")
            return []
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.select("a.result__a"):
            link = a.get("href", "")
            if link.startswith("//duckduckgo.com/l/?uddg="):
                link = unquote(link.split("uddg=")[1].split("&")[0])
            if link.startswith("http"):
                results.append(link)
                if len(results) >= max_results:
                    break
    except Exception as e:
        print(f"{C.RED}  [!] DuckDuckGo error: {e}{C.RESET}")
    return results


def search_google(query: str, max_results: int = 20) -> list:
    results = []
    url = f"https://www.google.com/search?q={quote_plus(query)}&num={max_results}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15, verify=False)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.select("a"):
            href = a.get("href", "")
            if href.startswith("/url?q="):
                link = href.split("/url?q=")[1].split("&")[0]
                if link.startswith("http") and "google.com" not in link:
                    results.append(link)
                    if len(results) >= max_results:
                        break
    except Exception as e:
        print(f"{C.RED}  [!] Google error: {e}{C.RESET}")
    return results


def run_google_dork():
    clear()
    header()
    print(f"{C.GREEN}{C.BOLD}  ▸ Google Dorking{C.RESET}")
    print(f"  {C.DIM}Search for exposed files, credentials, and sensitive data.{C.RESET}\n")

    target = input(f"  {C.GREEN}Target domain{C.RESET} (e.g. example.com) : ").strip()
    if not target:
        print(f"{C.RED}  [!] Empty target.{C.RESET}")
        input(f"\n  {C.DIM}Press ENTER to continue...{C.RESET}")
        return

    target = target.replace("https://", "").replace("http://", "").strip("/")

    show_dork_menu()

    print(f"\n  {C.GREEN}Tip:{C.RESET} {C.DIM}pick 1 number, or multiple separated by comma (e.g. 11,17,21){C.RESET}")
    pilihan_raw = input(f"\n  {C.GREEN}Select dork{C.RESET} : ").strip()

    if not pilihan_raw:
        print(f"{C.RED}  [!] Empty selection.{C.RESET}")
        input(f"\n  {C.DIM}Press ENTER to continue...{C.RESET}")
        return

    keys = []
    for p in pilihan_raw.split(","):
        p = p.strip()
        if not p:
            continue
        p_pad = p.zfill(2)
        if p_pad not in DORK_PRESETS:
            print(f"{C.RED}  [!] Dork '{p}' not found, skipped.{C.RESET}")
            continue
        keys.append(p_pad)

    if not keys:
        print(f"{C.RED}  [!] No valid dork.{C.RESET}")
        input(f"\n  {C.DIM}Press ENTER to continue...{C.RESET}")
        return

    queries = []
    for k in keys:
        name, template, cat = DORK_PRESETS[k]
        if template is None:
            q = input(f"  {C.GREEN}Custom query{C.RESET} : ").strip()
            if not q:
                continue
            q = q.replace("{target}", target)
        else:
            q = template.format(target=target)
        queries.append((name, q))

    print(f"\n{C.GREEN}{C.BOLD}  ▸ Queries to run:{C.RESET}")
    for i, (name, q) in enumerate(queries, 1):
        print(f"  {C.GREEN}{i}.{C.RESET} {C.DIM}{name}{C.RESET}")
        print(f"     {C.WHITE}{q}{C.RESET}")

    mesin = input(f"\n  {C.GREEN}Search engine (1=DuckDuckGo, 2=Google) [1]{C.RESET} : ").strip() or "1"

    all_results = {}
    all_emails = set()

    for i, (name, q) in enumerate(queries, 1):
        print(f"\n{C.GREEN}{C.BOLD}  ═══ [{i}/{len(queries)}] {name} ═══{C.RESET}")
        print(f"  {C.DIM}{q}{C.RESET}\n")

        if mesin == "2":
            results = search_google(q, max_results=20)
        else:
            results = search_duckduckgo(q, max_results=20)

        print(f"  {C.GREEN}▸ {len(results)} results{C.RESET}")
        for u in results:
            if u not in all_results:
                all_results[u] = name

        if results:
            print(f"  {C.GREEN}▸ Extracting emails...{C.RESET}")
            for u in results:
                html = fetch(u, timeout=8)
                if html:
                    all_emails |= extract_emails(html)
                time.sleep(0.2)

    print(f"\n{C.GREEN}{C.BOLD}  ═══ SUMMARY ═══{C.RESET}")
    print(f"  Unique URLs   : {C.WHITE}{len(all_results)}{C.RESET}")
    print(f"  Unique emails : {C.WHITE}{len(all_emails)}{C.RESET}")

    if all_results:
        print(f"\n{C.GREEN}{C.BOLD}  ═══ URL LIST ═══{C.RESET}")
        for i, (u, src) in enumerate(all_results.items(), 1):
            print(f"  {C.GREEN}{i:>2}.{C.RESET} {C.WHITE}{u}{C.RESET}")
            print(f"      {C.DIM}↳ {src}{C.RESET}")

    if all_emails:
        print(f"\n{C.GREEN}{C.BOLD}  ═══ EMAIL LIST ═══{C.RESET}")
        for e in sorted(all_emails):
            print(f"  {C.GREEN}✓{C.RESET} {C.WHITE}{e}{C.RESET}")

    if all_results or all_emails:
        save = input(f"\n  {C.GREEN}Save result? (y/n){C.RESET} : ").strip().lower()
        if save == "y":
            ts = int(time.time())
            meta = [
                f"Target: {target}",
                f"Time  : {datetime.now()}",
                f"Query : {len(queries)} dork",
            ]

            fname_url = f"dork_urls_{ts}.txt"
            save_lines(fname_url, [f"[{src}] {u}" for u, src in all_results.items()], meta)

            if all_emails:
                fname_em = f"dork_emails_{ts}.txt"
                save_lines(fname_em, sorted(all_emails), meta)

    input(f"\n  {C.DIM}Press ENTER to continue...{C.RESET}")


# ================= IP LOOKUP =================
def get_ip_info(ip: str = "") -> dict:
    url = (f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,"
           f"region,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,"
           f"reverse,mobile,proxy,hosting,query")
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": "fail", "message": str(e)}


def get_my_public_ip() -> str:
    try:
        r = requests.get("https://api.ipify.org?format=json", timeout=10)
        return r.json().get("ip", "unknown")
    except Exception:
        return "unknown"


def print_ip_info(data: dict):
    if data.get("status") != "success":
        print(f"{C.RED}  [!] Failed: {data.get('message', 'unknown error')}{C.RESET}")
        return

    cc = data.get("countryCode", "").upper()
    flag = ""
    if len(cc) == 2:
        flag = chr(0x1F1E6 + ord(cc[0]) - ord("A")) + chr(0x1F1E6 + ord(cc[1]) - ord("A"))

    rows = [
        ("IP",           data.get("query", "-")),
        ("Country",      f"{flag} {data.get('country', '-')} ({cc})"),
        ("Region",       data.get("regionName", "-")),
        ("City",         data.get("city", "-")),
        ("ZIP Code",     data.get("zip", "-")),
        ("Latitude",     str(data.get("lat", "-"))),
        ("Longitude",    str(data.get("lon", "-"))),
        ("Timezone",     data.get("timezone", "-")),
        ("ISP",          data.get("isp", "-")),
        ("Organization", data.get("org", "-")),
        ("AS",           data.get("as", "-")),
        ("Reverse DNS",  data.get("reverse", "-") or "-"),
        ("Mobile",       "Yes" if data.get("mobile") else "No"),
        ("Proxy/VPN",    f"{C.RED}Yes{C.RESET}" if data.get("proxy") else f"{C.GREEN}No{C.RESET}"),
        ("Hosting",      f"{C.YELLOW}Yes{C.RESET}" if data.get("hosting") else f"{C.GREEN}No{C.RESET}"),
    ]

    print()
    for k, v in rows:
        key = f"{C.GREEN}{C.BOLD}{k:<14}{C.RESET}"
        print(f"  {key} : {C.WHITE}{v}{C.RESET}")
    print()

    lat, lon = data.get("lat"), data.get("lon")
    if lat and lon:
        print(f"  {C.DIM}Map: https://www.google.com/maps?q={lat},{lon}{C.RESET}")


def run_ip_lookup():
    clear()
    header()
    print(f"{C.GREEN}{C.BOLD}  ▸ IP Lookup{C.RESET}")
    print(f"  {C.DIM}Get detailed info about any IP address or domain.{C.RESET}\n")

    print(f"  {C.GREEN}[1]{C.RESET} {C.WHITE}My Public IP{C.RESET}        {C.DIM}(your public IP address){C.RESET}")
    print(f"  {C.GREEN}[2]{C.RESET} {C.WHITE}My Local IP{C.RESET}         {C.DIM}(your LAN IP){C.RESET}")
    print(f"  {C.GREEN}[3]{C.RESET} {C.WHITE}Lookup IP / Domain{C.RESET}  {C.DIM}(check any IP or domain){C.RESET}")
    print(f"  {C.GREEN}[0]{C.RESET} {C.WHITE}Back{C.RESET}\n")

    pilihan = input(f"  {C.GREEN}Select{C.RESET} : ").strip()

    if pilihan == "0":
        return

    elif pilihan == "1":
        print(f"\n{C.GREEN}  ▸ Fetching public IP...{C.RESET}")
        ip = get_my_public_ip()
        if ip == "unknown":
            print(f"{C.RED}  [!] Failed to get public IP.{C.RESET}")
        else:
            data = get_ip_info(ip)
            print_ip_info(data)

    elif pilihan == "2":
        print(f"\n{C.GREEN}  ▸ Local IP:{C.RESET} {C.WHITE}{get_local_ip()}{C.RESET}")
        try:
            hostname = socket.gethostname()
            print(f"  {C.GREEN}Hostname{C.RESET}      : {C.WHITE}{hostname}{C.RESET}")
        except Exception:
            pass

    elif pilihan == "3":
        target = input(f"  {C.GREEN}Enter IP / Domain{C.RESET} : ").strip()
        if not target:
            print(f"{C.RED}  [!] Empty input.{C.RESET}")
        else:
            if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", target):
                try:
                    resolved = socket.gethostbyname(target)
                    print(f"  {C.DIM}Resolved: {target} → {resolved}{C.RESET}")
                    target = resolved
                except socket.gaierror:
                    print(f"{C.RED}  [!] Cannot resolve {target}{C.RESET}")
                    input(f"\n  {C.DIM}Press ENTER to continue...{C.RESET}")
                    return

            print(f"\n{C.GREEN}  ▸ Fetching info...{C.RESET}")
            data = get_ip_info(target)
            print_ip_info(data)
    else:
        print(f"{C.RED}  [!] Invalid option.{C.RESET}")

    input(f"  {C.DIM}Press ENTER to continue...{C.RESET}")


# ================= URL TO HTML =================
def run_url_to_html():
    clear()
    header()
    print(f"{C.GREEN}{C.BOLD}  ▸ URL to HTML{C.RESET}")
    print(f"  {C.DIM}Download the raw HTML of any web page.{C.RESET}\n")

    target = input(f"  {C.GREEN}Target URL{C.RESET} (e.g. https://example.com) : ").strip()
    if not target:
        print(f"{C.RED}  [!] Empty URL.{C.RESET}")
        input(f"\n  {C.DIM}Press ENTER to continue...{C.RESET}")
        return

    if not target.startswith(("http://", "https://")):
        target = "https://" + target

    print(f"\n{C.GREEN}  ▸ Fetching HTML...{C.RESET}")

    try:
        r = requests.get(target, headers=HEADERS, timeout=15, verify=False)
        r.raise_for_status()
        html = r.text
    except requests.RequestException as e:
        print(f"{C.RED}  [!] Failed: {e}{C.RESET}")
        input(f"\n  {C.DIM}Press ENTER to continue...{C.RESET}")
        return

    print(f"\n{C.GREEN}  ▸ Result:{C.RESET}")
    print(f"  {C.GREEN}Status Code{C.RESET}   : {C.WHITE}{r.status_code}{C.RESET}")
    print(f"  {C.GREEN}Content-Type{C.RESET}  : {C.WHITE}{r.headers.get('Content-Type', '-')}{C.RESET}")
    print(f"  {C.GREEN}Size{C.RESET}          : {C.WHITE}{len(html):,} bytes{C.RESET}")
    print(f"  {C.GREEN}Final URL{C.RESET}     : {C.WHITE}{r.url}{C.RESET}")

    print(f"\n  {C.GREEN}[1]{C.RESET} {C.WHITE}Save as auto-named .html{C.RESET}")
    print(f"  {C.GREEN}[2]{C.RESET} {C.WHITE}Save with custom name{C.RESET}")
    print(f"  {C.GREEN}[3]{C.RESET} {C.WHITE}Preview in terminal{C.RESET}")
    print(f"  {C.GREEN}[4]{C.RESET} {C.WHITE}Copy to clipboard{C.RESET} {C.DIM}(needs termux-api){C.RESET}")
    print(f"  {C.GREEN}[0]{C.RESET} {C.WHITE}Cancel{C.RESET}\n")

    pilihan = input(f"  {C.GREEN}Select{C.RESET} : ").strip()

    if pilihan == "0":
        return

    elif pilihan == "1":
        domain = urlparse(target).netloc.replace(":", "_").replace(".", "_")
        fname = f"{domain}_{int(time.time())}.html"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\n  {C.GREEN}✓ Saved to: {fname}{C.RESET}")

    elif pilihan == "2":
        fname = input(f"  {C.GREEN}Filename{C.RESET} (e.g. page.html) : ").strip()
        if not fname:
            print(f"{C.RED}  [!] Empty filename.{C.RESET}")
            input(f"\n  {C.DIM}Press ENTER to continue...{C.RESET}")
            return
        if not fname.endswith(".html"):
            fname += ".html"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\n  {C.GREEN}✓ Saved to: {fname}{C.RESET}")

    elif pilihan == "3":
        print(f"\n{C.GREEN}{C.BOLD}  ═══ PREVIEW (max 3000 chars) ═══{C.RESET}\n")
        print(f"{C.WHITE}{html[:3000]}{C.RESET}")
        if len(html) > 3000:
            print(f"\n{C.DIM}... ({len(html) - 3000:,} chars truncated){C.RESET}")

    elif pilihan == "4":
        try:
            proc = subprocess.Popen(
                ["termux-clipboard-set"],
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            proc.communicate(html.encode("utf-8"))
            if proc.returncode == 0:
                print(f"\n  {C.GREEN}✓ HTML copied to clipboard{C.RESET}")
            else:
                raise Exception("clipboard failed")
        except Exception:
            print(f"\n  {C.YELLOW}[!] termux-api not available. Install first:{C.RESET}")
            print(f"  {C.WHITE}    pkg install termux-api{C.RESET}")
            print(f"  {C.WHITE}    (also install Termux:API from F-Droid){C.RESET}")
    else:
        print(f"{C.RED}  [!] Invalid option.{C.RESET}")

    input(f"\n  {C.DIM}Press ENTER to continue...{C.RESET}")


# ================= MAIN =================
def main_menu():
    while True:
        clear()
        header()
        banner()
        info_table()
        menu()

        try:
            choice = input(f"\n  {C.GREEN}{C.BOLD}▸ Select menu{C.RESET} : ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{C.RED}Exit...{C.RESET}")
            sys.exit(0)

        if choice in ("1", "01"):
            run_email_crawl()
        elif choice in ("2", "02"):
            run_google_dork()
        elif choice in ("3", "03"):
            run_ip_lookup()
        elif choice in ("4", "04"):
            run_url_to_html()
        elif choice in ("0", "00"):
            print(f"\n{C.GREEN}Exiting X-EYELESS...{C.RESET}")
            sys.exit(0)
        else:
            print(f"{C.RED}  [!] Invalid option.{C.RESET}")
            input(f"  {C.DIM}Press ENTER to continue...{C.RESET}")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{C.RED}Cancelled by user.{C.RESET}")
        sys.exit(0)