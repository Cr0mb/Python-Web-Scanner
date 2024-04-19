# This Python script uses Selenium to check redirections for websites listed in "sites.txt." 
# Employing concurrent execution with a maximum of 5 ports, it utilizes a headless Chrome browser. 
# Redirected URLs are logged in "output.txt," excluding sites containing 'login.' 
# The script displays execution time upon completion.

# Import necessary libraries
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures
import time

# Define maximum number of concurrent ports
MAX_CONCURRENT_PORTS = 5 

# Function to check redirection of a URL
def check_redirect(url):
    # Configure Chrome options for headless browsing
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  
    options.add_argument('--disable-gpu')  
    options.add_argument('--no-sandbox')  
    options.add_argument('--disable-dev-shm-usage')  
    # Initialize Chrome WebDriver
    with webdriver.Chrome(options=options) as driver:
        try:
            # Navigate to the URL
            driver.get(url)
            # Get the final URL after redirection
            final_url = driver.current_url
            # Check if final URL contains 'login'
            if "login" not in final_url:
                return final_url
            else:
                return None
        except Exception as e:
            # Handle exceptions
            print(f"Error checking {url}: {str(e)}")
            return None

# Main function
def main():
    input_file = "clean_sites.txt"
    output_file = "output.txt"
    # Read URLs from input file
    with open(input_file, "r") as infile:
        sites = [line.strip() for line in infile]
    # Initialize ThreadPoolExecutor with maximum concurrent workers
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_PORTS) as executor:
        # Submit tasks for each URL to check redirection
        futures = {executor.submit(check_redirect, site): site for site in sites}
        # Iterate through completed futures
        for future in concurrent.futures.as_completed(futures):
            site = futures[future]
            try:
                # Get result of the future
                redirected_url = future.result()
                # Process result
                if redirected_url:
                    print(f"Redirected: {site} -> {redirected_url}")
                    # Write redirected URL to output file
                    with open(output_file, "a") as outfile:
                        outfile.write(f"{site} -> {redirected_url}\n")
                else:
                    print(f"Skipped: {site} (contains 'login')")
            except Exception as e:
                # Handle exceptions
                print(f"Error processing {site}: {str(e)}")

# Execute main function if script is run directly
if __name__ == "__main__":
    # Record start time
    start_time = time.time()
    main()
    # Print execution time
    print(f"Execution time: {time.time() - start_time} seconds")
