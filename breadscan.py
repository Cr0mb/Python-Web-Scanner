# Hello youtube my name is Cr0mb, and today I will be sharing with you a webscanner script.pip 
# This Python script performs a simple web scanning task to identify active web servers with potential index pages.
# Will create random addresses, attempt to connect to them, and check if server responds with '200' status code and 
# type "text/html." 
# If the criteria are met, it prints the URL as an active site and checks for a potential index page. 
# The active URLs are logged in a file named "sites.txt."
# The organizer will organize addresses from least to greatest.

# Import necessary libraries
import asyncio
import aiohttp
import random
import os
import ctypes
import argparse
from colorama import Fore, Style, init
from pyfiglet import Figlet

# Initialize colorama for colored text output
init(autoreset=True)

# Function to generate a random IP address
async def generate_random_ip():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))

# Function to scan for potential index page on a given IP address
async def scan_for_index_page(session, ip_address, counter):
    # Construct URL from IP address
    url = f"http://{ip_address}"
    try:
        # Attempt to connect to the URL
        async with session.get(url, timeout=2) as response:
            # Check if response status is 200 and content type is "text/html"
            if response.status == 200 and "text/html" in response.headers.get("Content-Type", ""):
                # Print active result if criteria are met
                print_active_result(url)
                try:
                    # Try to decode and analyze the response text
                    text_content = await response.text(encoding='utf-8', errors='replace')
                    if "/" in text_content:
                        print(f"{Fore.GREEN}[+] Potential index page found!{Style.RESET_ALL}")
                        # Write the active URL to a file
                        await write_to_file(url)
                except UnicodeDecodeError:
                    # Print error if there's an issue decoding the response text
                    print_decode_error(url)
                # Increment the active site counter
                counter['active'] += 1
            else:
                # Print inactive result if criteria are not met
                print_inactive_result(url)
            # Increment the total site counter
            counter['total'] += 1
            # Print total sites scanned
            print_totals(counter)
    except (aiohttp.ClientError, asyncio.TimeoutError):
        # Print inactive result if there's an error connecting to the URL
        print_inactive_result(url)
        # Increment the total site counter
        counter['total'] += 1
        # Print total sites scanned
        print_totals(counter)

# Function to print active result
def print_active_result(url):
    clear_screen()
    print_banner()
    set_window_title("Crumb Finder HTTP GEN")
    print(f"{Fore.GREEN}[+] {url} ACTIVE{Style.RESET_ALL}")

# Function to print inactive result
def print_inactive_result(url):
    clear_screen()
    print_banner()
    set_window_title("Crumb Finder HTTP GEN")
    print(f"{Fore.RED}[-] {url} NOT ACTIVE{Style.RESET_ALL}")

# Function to print decode error
def print_decode_error(url):
    print(f"{Fore.RED}[-] Error decoding response text for {url}{Style.RESET_ALL}")

# Function to print total sites scanned
def print_totals(counter):
    print(f"\nTotal sites searched: {counter['total']}")
    print(f"Total active sites: {counter['active']}")

# Function to write URL to file
async def write_to_file(url):
    with open('sites.txt', 'a') as file:
        file.write(f"{url}\n")

# Function to set window title
def set_window_title(title):
    if os.name == 'posix':
        print(f'\033]0;{title}\007', end='', flush=True)
    elif os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)

# Function to clear screen
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# Function to print banner
def print_banner():
    global fig
    fig = Figlet()
    print(f"{Fore.LIGHTYELLOW_EX}{fig.renderText('Crumb Finder')}{Style.RESET_ALL}")

# Main function
async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Crumb Finder HTTP GEN', add_help=False)
    parser.add_argument('-u', action='store_true', help='Scan unlimited IP addresses')
    parser.add_argument('-n', type=int, default=0, help='Number of IP addresses to scan')
    parser.add_argument('-i', type=int, default=1, help='Number of instances to run concurrently')
    parser.add_argument('-help', action='help', help='Show this help message and exit')
    parser.add_argument('-h', action='help', help='Show this help message and exit')
    args = parser.parse_args()

    # If no arguments are provided, prompt user for input
    if not any(vars(args).values()) or (args.n == 0 and args.i == 1 and not args.u):
        args.n = int(input("Enter the number of IP addresses to scan (0 for unlimited): "))
        args.i = int(input("Enter the number of instances to run concurrently: "))
        if args.n == 0:
            args.u = True

    clear_screen()
    print_banner()
    print(f"{Fore.BLACK}Scans random IP addresses for potential index pages.{Style.RESET_ALL}")
    set_window_title("Crumb Finder HTTP GEN")

    # Determine number of addresses to scan
    num_addresses = args.n if not args.u else 0
    scanned_addresses = set()

    async with aiohttp.ClientSession() as session:
        counter = {'total': 0, 'active': 0}

        # Function to start scanning
        async def start_scanning():
            while num_addresses == 0 or counter['total'] < num_addresses:
                ip_address = await generate_random_ip()

                while ip_address in scanned_addresses:
                    ip_address = await generate_random_ip()

                scanned_addresses.add(ip_address)
                await scan_for_index_page(session, ip_address, counter)

        # Create tasks for concurrent scanning
        tasks = [start_scanning() for _ in range(args.i)]
        await asyncio.gather(*tasks)

# Run the main function
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
