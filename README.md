

# Python-Web-Scanner

Youtube Video: https://www.youtube.com/watch?v=pT0DIE-ReMk&t=4s

Python-based toolset for conducting advanced reconnaissance tasks on web resources associated with IP addresses. It leverages asyncio for concurrent scanning, aiohttp for asynchronous HTTP requests, and integrates various utilities for handling files, terminal interactions, and network-related tasks.

## Prerequisites
Before getting started, make sure you have the following installed:

- Python 3.x
- Pip (Python package manager)
  - asyncio (Standard library for asynchronous programming)
  - aiohttp (For asynchronous HTTP requests)
  - colorama (For colored terminal output)
  - pyfiglet (For ASCII art text rendering)
  - requests (For making HTTP requests)
  - re (Standard library for regular expressions)
  - concurrent.futures (For concurrent execution of tasks)
  - time (Standard library for time-related functions)
  - socket (Standard library for low-level networking interfaces)

## Installation

You can install the required Python packages using pip:
```
pip install asyncio aiohttp colorama pyfiglet requests
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

![image](https://github.com/Cr0mb/Python-Web-Scanner/assets/137664526/30698e54-aee9-4194-915f-84210bda2d89)


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
```
python checker.py
```

![image](https://github.com/Cr0mb/Python-Web-Scanner/assets/137664526/0b0bd03c-321c-4b3f-b714-d5a9563b8527)

4. Regex for Domain Validation (cleanoutput.py)
- This script will create filtered_output.txt with only the valid URL redirection pairs that point to domain names, excluding those that redirect to IP addresses.
```
python cleanoutput.py
```

5. Sitemap redirect checker (sitemap.py)
- Checks to see if a given site has a sitemap.xml.
```
python sitemap.py
```

6. RTSP Port Checker (rtsp.py)
- The rtsp.py script is designed to identify IP addresses with an open RTSP (Real-Time Streaming Protocol) port. RTSP ports are commonly used for streaming media servers, and detecting open ports can help in discovering accessible media services.
```
python rtsp.py
```

![image](https://github.com/Cr0mb/Python-Web-Scanner/assets/137664526/d6d052a9-896e-43f4-a2df-e5297fd5c6c8)


7. IP location finder (location.py)
- Scans IP addresses listed in clean_sites.txt using ipinfo.io api; retrieving location information such as:
>  Country, State, Region, ISP, Latitude, Longitude, and Organization
- Uses the ip-api.com API.
- it's slowed a little because of possible limiting to the api requests (error 429)

![image](https://github.com/Cr0mb/Python-Web-Scanner/assets/137664526/f3502e19-2ab1-480c-a06f-65e7e110955e)


## How to Use

1. Web Scanner:

- Run breadscan.py with desired options to scan for active web servers.
Adjust the number of addresses and instances based on your requirements.

2. URL Organizer:

- Execute httplistorganizer.py to extract and organize unique IP addresses.

3. Redirection Checker:

- Run checker.py to check redirections for websites.

4. Domain Validator

- Run cleanoutput.py to consolidate domain links to a seperate file for organization.

5. Sitemap Chcker

- Run sitemap.py to index sites that contain /sitemap.xml

6. RTSP Checker

- Run rtsp.py to find sites that contain open port 554

## Updates
```
v1.5
> Added a rtsp checker script to find out which sites contain media streaming under port 554.
```
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

