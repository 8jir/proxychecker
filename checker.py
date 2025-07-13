import os
import requests
import time
from colorama import *
from urllib.parse import urlparse

FOLDER = "proxies"
TEST_URL = "http://httpbin.org/ip"
TIMEOUT = 5

PROTOCOL_KEYWORDS = {
    "SOCKS4": "socks4",
    "SOCKS5": "socks5",
    "HTTP": "http",
    "HTTPS": "http"
}

os.system('cls' if os.name == 'nt' else 'clear')

def detect_protocol(filename):
    for key, prot in PROTOCOL_KEYWORDS.items():
        if key.lower() in filename.lower():
            return prot
    return "http"

def check_proxy(ip_port, protocol):
    proxies = {
        "http": f"{protocol}://{ip_port}",
        "https": f"{protocol}://{ip_port}"
    }
    ip, port = ip_port.split(":")
    try:
        res = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        status = f"{Fore.GREEN}{Style.BRIGHT}LIVE{Fore.WHITE}" if res.status_code == 200 else f"{Fore.RED}{Style.BRIGHT}TIMEOUT{Fore.WHITE}"
    except Exception:
        status = f"{Fore.RED}{Style.BRIGHT}TIMEOUT{Fore.WHITE}"

    print(f" └ Proxy: {Fore.CYAN}{Style.BRIGHT}{ip}{Fore.WHITE}\n └ Port: {Fore.CYAN}{Style.BRIGHT}{port}{Fore.WHITE}\n └ Protocol: {Fore.MAGENTA}{Style.BRIGHT}{protocol}{Fore.WHITE}\n └ Status: {status}")
    return status == f"{Fore.GREEN}{Style.BRIGHT}LIVE{Fore.WHITE}"

def main():
    files = [f for f in os.listdir(FOLDER) if f.endswith(".txt")]
    total_files = len(files)
    total_timeout = 0
    total_valid = 0
    total_proxies = 0

    for file in files:
        filepath = os.path.join(FOLDER, file)
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}[+] Checking {Fore.GREEN}{Style.BRIGHT}{file} ...{Fore.WHITE}")
        protocol = detect_protocol(file)
        with open(filepath, "r") as f:
            lines = [line.strip() for line in f if ":" in line]

        valid = []
        for line in lines:
            total_proxies += 1
            if check_proxy(line, protocol):
                valid.append(line)
            else:
                total_timeout += 1

        total_valid += len(valid)

        if valid:
            with open(f"valid-{file}", "w") as vf:
                vf.write("\n".join(valid))

    print("\n[✓] Done checking all proxy files.")
    print(f" └ Total proxy: {total_proxies}")
    print(f" └ Total file checked: {total_files}")
    print(f" └ Total timeout: {total_timeout}")
    print(f" └ Total valid: {total_valid}")

if __name__ == "__main__":
    main()
