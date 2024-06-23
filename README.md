![image](https://github.com/Cr0mb/Python-Web-Scanner/assets/137664526/30698e54-aee9-4194-915f-84210bda2d89)
```
v1.45
> Enhanced Error Handling
> Validation for Empty or Invalid URLs
> Logging and Error / Timeout Indication
```
```
v1.4
> added a sitemap checker script to find out which sites found contain a sitemap.
```
```
v1.3
> Added 'Total Amount of sites: ' to read total amount of sites that are written in sites.txt
> Now any site will not be duplicated in sites.txt if scanned the same randomly generated address twice.
```
```
V1.2
> Introduced a 'TIMEOUT' constant, so if a request takes longer than the specified timeout period, it will raise a 'requests.Timeout' exception.
   > Crucial when dealing with potentially slow or unresponsive web servers.
```
```
V1.12
> Added "cleanoutput.py"; will show all website URLs ignoring IP addresses that don't link to a domain.
> You can use this after you use checker.py, this python script will grab all of the website link URLs from output.txt, ignoring the ones that redirect to an IP address.
```

```
V1.1
> Updated "checker.py" so that chrome driver is no longer needed.
> Makes finding the redirected sites exponentially faster and less power hungry.
> Also no longer uses selenium.
```

# Python-Web-Scanner

Youtube Video: https://www.youtube.com/watch?v=pT0DIE-ReMk&t=4s

This Python script performs web scanning tasks to identify active web servers, potential index pages, and check redirections for websites. It utilizes asynchronous programming, concurrent execution, and web automation to efficiently scan and analyze web addresses. This tutorial provides step-by-step instructions on how to use and understand each component of the script.

## Prerequisites
Before getting started, make sure you have the following installed:

- Python 3.x
- Pip (Python package manager)

## Installation

You can install the required Python packages using pip:
```
pip install aiohttp colorama pyfiglet
```

## Components of the Script

1. Web Scanner (breadscan.py)
- Generates random IP addresses.
- Scans for potential index pages on active web servers.
- Logs active URLs in a file named "sites.txt".
```
python breadscan.py [-u] [-n NUM_ADDRESSES] [-i NUM_INSTANCES]

-u: Scan unlimited IP addresses.
-n: Number of IP addresses to scan (default: 0).
-i: Number of instances to run concurrently (default: 1).
```

2. URL Organizer (httplistorganizer.py)
- Reads URLs from "sites.txt".
- Extracts unique IP addresses and sorts them.  
- Writes sorted addresses to "clean_sites.txt".
```
python httplistorganizer.py
```

3. Redirection Checker (checker.py)
- Checks redirections for websites listed in "clean_sites.txt".
- Uses requests for handling HTTP requests and concurrent.futures for managing concurrent execution.
  - check_redirect: Sends an HTTP GET request to the provided URL and follows any redirects (allow_redirects=True). It returns the final URL unless it contains the word 'login'.
    - Retaining websites that contain 'login' slightly minimizes the amount of routers (not by much.)
- Logs redirected URLs in "output.txt" excluding sites containing 'login'.

![image](https://github.com/Cr0mb/Python-Web-Scanner/assets/137664526/0b0bd03c-321c-4b3f-b714-d5a9563b8527)

4. Regex for Domain Validation (cleanoutput.py)
- This script will create filtered_output.txt with only the valid URL redirection pairs that point to domain names, excluding those that redirect to IP addresses.


## How to Use

1. Web Scanner:

- Run web_scanner.py with desired options to scan for active web servers.
Adjust the number of addresses and instances based on your requirements.

2. URL Organizer:

- Execute url_organizer.py to extract and organize unique IP addresses.

3. Redirection Checker:

- Run redirection_checker.py to check redirections for websites.

4. Domain Validator

- Run cleanout.py to consolidate domain links to a seperate file for organization.

