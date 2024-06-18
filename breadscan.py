# Hello youtube my name is Cr0mb, and today I will be sharing with you a webscanner script.pip 
# This Python script performs a simple web scanning task to identify active web servers with potential index pages.
# Will create random addresses, attempt to connect to them, and check if server responds with '200' status code and 
# type "text/html." 
# If the criteria are met, it prints the URL as an active site and checks for a potential index page. 
# The active URLs are logged in a file named "sites.txt."
# The organizer will organize addresses from least to greatest.

import asyncio
import aiohttp
import random
import os
import ctypes
import argparse
from colorama import Fore, Style, init
from pyfiglet import Figlet

init(autoreset=True)


# Function to load existing IP addresses from sites.txt
def load_existing_ips(file_path):
    existing_ips = set()
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                url = line.strip()
                if url.startswith('http://'):
                    ip_address = url[len('http://'):]
                    existing_ips.add(ip_address)
    return existing_ips


# Function to generate a random IP address that is not in the existing_ips set
def generate_random_ip(existing_ips):
    while True:
        ip_address = '.'.join(str(random.randint(0, 255)) for _ in range(4))
        if ip_address not in existing_ips:
            return ip_address


# Function to print banner
def print_banner():
    fig = Figlet()
    print(
        f"{Fore.LIGHTYELLOW_EX}{fig.renderText('Crumb Finder')}{Style.RESET_ALL}"
    )


# Function to print totals
def print_totals(counter):
    print(f"\nTotal sites searched: {counter['total']}")
    print(f"Total active sites: {counter['active']}")
    print(f"Total amount of sites: {counter['active'] + counter['existing']}")


# Function to count existing sites in sites.txt
def count_existing_sites(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return len(file.readlines())
    return 0


# Function to set window title
def set_window_title(title):
    if os.name == 'posix':
        print(f'\033]0;{title}\007', end='', flush=True)
    elif os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)


# Function to clear screen
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')


# Function to write URL to file
def write_to_file(url):
    with open('sites.txt', 'a') as file:
        file.write(f"{url}\n")


# Function to handle scan result
def handle_scan_result(url, active):
    clear_screen()
    print_banner()
    set_window_title("Crumb Finder HTTP GEN")
    if active:
        print(f"{Fore.GREEN}[+] {url} ACTIVE{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[-] {url} NOT ACTIVE{Style.RESET_ALL}")


# Function to scan for potential index page on a given IP address
async def scan_for_index_page(session, ip_address, counter):
    url = f"http://{ip_address}"
    try:
        async with session.get(url, timeout=2) as response:
            if response.status == 200 and "text/html" in response.headers.get(
                    "Content-Type", ""):
                handle_scan_result(url, active=True)
                try:
                    text_content = await response.text(encoding='utf-8',
                                                       errors='replace')
                    if "/" in text_content:
                        print(
                            f"{Fore.GREEN}[+] Potential index page found!{Style.RESET_ALL}"
                        )
                        write_to_file(url)
                except UnicodeDecodeError:
                    print(
                        f"{Fore.RED}[-] Error decoding response text for {url}{Style.RESET_ALL}"
                    )
                counter['active'] += 1
            else:
                handle_scan_result(url, active=False)
            counter['total'] += 1
            print_totals(counter)
    except (aiohttp.ClientError, asyncio.TimeoutError):
        handle_scan_result(url, active=False)
        counter['total'] += 1
        print_totals(counter)


# Main function
async def main():
    parser = argparse.ArgumentParser(description='Crumb Finder HTTP GEN',
                                     add_help=False)
    parser.add_argument('-u',
                        action='store_true',
                        help='Scan unlimited IP addresses')
    parser.add_argument('-n',
                        type=int,
                        default=0,
                        help='Number of IP addresses to scan')
    parser.add_argument('-i',
                        type=int,
                        default=1,
                        help='Number of instances to run concurrently')
    args = parser.parse_args()

    if not any(vars(args).values()) or (args.n == 0 and args.i == 1
                                        and not args.u):
        args.n = int(
            input(
                "Enter the number of IP addresses to scan (0 for unlimited): ")
        )
        args.i = int(
            input("Enter the number of instances to run concurrently: "))
        if args.n == 0:
            args.u = True

    clear_screen()
    print_banner()
    print(
        f"{Fore.BLACK}Scans random IP addresses for potential index pages.{Style.RESET_ALL}"
    )
    set_window_title("Crumb Finder HTTP GEN")

    num_addresses = args.n if not args.u else 0
    scanned_addresses = set()

    counter = {
        'total': 0,
        'active': 0,
        'existing': count_existing_sites('sites.txt')
    }

    existing_ips = load_existing_ips('sites.txt')

    async with aiohttp.ClientSession() as session:

        async def start_scanning():
            while num_addresses == 0 or counter['total'] < num_addresses:
                ip_address = generate_random_ip(existing_ips)
                while ip_address in scanned_addresses:
                    ip_address = generate_random_ip(existing_ips)
                scanned_addresses.add(ip_address)
                await scan_for_index_page(session, ip_address, counter)

        tasks = [start_scanning() for _ in range(args.i)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
