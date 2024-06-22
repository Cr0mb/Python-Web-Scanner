import requests
import os

def read_sites(file_path):
    urls = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                url = line.strip()
                if url.startswith('http://') or url.startswith('https://'):
                    urls.append(url)
    return urls

def check_for_sitemap(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text.lower()
            if "sitemap" in content or "index of /" in content:
                return True
    except requests.RequestException:
        pass
    return False

def main():
    file_path = 'sites.txt'
    urls = read_sites(file_path)
    
    sites_with_sitemap = []
    
    for url in urls:
        if check_for_sitemap(url):
            sites_with_sitemap.append(url)
            print(f"Found sitemap or 'index of /' at: {url}")
    
    print("\nSites with sitemap or 'index of /':")
    for site in sites_with_sitemap:
        print(site)

if __name__ == "__main__":
    main()
