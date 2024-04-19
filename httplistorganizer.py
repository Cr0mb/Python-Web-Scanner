# This script reads URLs from 'sites.txt', extracts unique IP addresses, sorts them, and writes to 'clean_sites.txt'. It provides an organized list of unique IPs for analysis.

import re
with open('sites.txt', 'r') as file:
    addresses = file.readlines()
def extract_ip(url):
    match = re.search(r'http://(\d+\.\d+\.\d+\.\d+)', url)
    if match:
        return match.group(1)
    return None
unique_addresses = set(filter(None, (extract_ip(address) for address in addresses)))
sorted_addresses = sorted(unique_addresses, key=lambda x: tuple(map(int, x.split('.'))))
with open('clean_sites.txt', 'w') as file:
    for address in sorted_addresses:
        file.write(f"http://{address}\n")
print("Unique addresses sorted and written to clean_sites.txt.")
