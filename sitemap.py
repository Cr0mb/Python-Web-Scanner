import requests
import re

# Function to extract IP address from URL
def extract_ip(url):
    match = re.search(r'http://(\d+\.\d+\.\d+\.\d+)', url)
    if match:
        return match.group(1)
    return None

# Function to check if a URL contains a sitemap
def has_sitemap(ip_address):
    url = f"http://{ip_address}/sitemap.xml"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and 'xml' in response.headers.get('Content-Type', ''):
            return url
        else:
            return None
    except requests.RequestException as e:
        print(f"Request error for {url}: {e}")
        return None
    except requests.Timeout:
        print(f"Timeout for {url}")
        return None
    except Exception as e:
        print(f"Unexpected error for {url}: {e}")
        return None

def main():
    input_file = "clean_sites.txt"
    output_file = "sitemap.txt"

    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            url = line.strip()
            if not url:
                continue  # Skip empty lines
            ip_address = extract_ip(url)
            if ip_address:
                sitemap_url = has_sitemap(ip_address)
                if sitemap_url:
                    print(f"Found sitemap at: {sitemap_url}")
                    outfile.write(f"{sitemap_url}\n")
                    outfile.flush()  # Ensure writing immediately to file
                else:
                    print(f"No sitemap found at: http://{ip_address}")
            else:
                print(f"Invalid URL format: {url}")

if __name__ == "__main__":
    main()
