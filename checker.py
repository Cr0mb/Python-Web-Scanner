import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

MAX_CONCURRENT_REQUESTS = 5

def check_redirect(url):
    try:
        response = requests.get(url, allow_redirects=True)
        final_url = response.url
        if "login" not in final_url:
            return final_url
        else:
            return None
    except requests.RequestException as e:
        print(f"Error checking {url}: {str(e)}")
        return None

def main():
    input_file = "clean_sites.txt"
    output_file = "output.txt"
    with open(input_file, "r") as infile:
        sites = [line.strip() for line in infile]
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_REQUESTS) as executor:
        futures = {executor.submit(check_redirect, site): site for site in sites}
        for future in as_completed(futures):
            site = futures[future]
            try:
                redirected_url = future.result()
                if redirected_url:
                    print(f"Redirected: {site} -> {redirected_url}")
                    with open(output_file, "a") as outfile:
                        outfile.write(f"{site} -> {redirected_url}\n")
                else:
                    print(f"Skipped: {site} (contains 'login')")
            except Exception as e:
                print(f"Error processing {site}: {str(e)}")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Execution time: {time.time() - start_time} seconds")
