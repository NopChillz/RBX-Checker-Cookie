from concurrent.futures import ThreadPoolExecutor
from requests import get
from datetime import datetime
from colorama import Fore, Style, init

init()

cookie_file = "Cookies.txt"
valid_file = "Normal.txt"
not_valid_file = "Broken.txt"


def log(text):
    print(f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}] → {text}")


def read_cookies(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        log(f"Error: '{file_path}' not found.")
        return []


def write_to_file(file_path, data):
    with open(file_path, "w") as file:
        file.write("\n".join(data))
    log(f"Saved results to '{file_path}'")


def check_cookie(cookie):
    try:
        response = get(
            'https://users.roblox.com/v1/users/authenticated',
            cookies={'.ROBLOSECURITY': cookie},
            timeout=5,
        )
        if '"id":' in response.text:
            log(f"{Fore.GREEN}[CHECK] Normal Cookie Found: {cookie[:10]}... (hidden){Style.RESET_ALL}")
            return cookie, "valid"
        elif 'Unauthorized' in response.text:
            log(f"{Fore.RED}[CHECK] Broken Cookie Found: {cookie[:10]}... (hidden){Style.RESET_ALL}")
            return cookie, "invalid"
        else:
            log(f"{Fore.YELLOW}Unexpected response for cookie: {cookie[:10]}... (hidden){Style.RESET_ALL}")
            return cookie, "unknown"
    except Exception as e:
        log(f"{Fore.RED}Error checking cookie: {cookie[:10]}... {str(e)}{Style.RESET_ALL}")
        return cookie, "unknown"


def main():
    log("Starting Cookie Checker...")
    cookies = read_cookies(cookie_file)

    if not cookies:
        log("No cookies found. Exiting...")
        return

    valid_cookies = []
    invalid_cookies = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(check_cookie, cookies))

    for cookie, status in results:
        if status == "valid":
            valid_cookies.append(cookie)
        elif status == "invalid":
            invalid_cookies.append(cookie)

    write_to_file(valid_file, valid_cookies)
    write_to_file(not_valid_file, invalid_cookies)

    print("=" * 80)
    log(f"{Fore.CYAN}[SYSTEM] Checker Cookies Success !!{Style.RESET_ALL} "
        f"{Fore.YELLOW}\nAll Checker Cookies: {len(cookies)}{Style.RESET_ALL}"
        f"{Fore.GREEN}\nNormal Cookies: {len(valid_cookies)}{Style.RESET_ALL}"
        f"{Fore.RED}\nBroken Cookies: {len(invalid_cookies)}{Style.RESET_ALL}")
    print("=" * 80)
    
    input("\nPress Enter to exit...")  # รอให้ผู้ใช้กด Enter ก่อนปิดโปรแกรม


if __name__ == "__main__":
    main()
