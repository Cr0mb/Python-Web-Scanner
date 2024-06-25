import socket  # Importing the 'socket' module for network operations
import re  # Importing the 're' module for regular expressions

# Function to extract IP address from a URL
def extract_ip(url):
    match = re.search(r'http://(\d+\.\d+\.\d+\.\d+)', url)  # Search for IP address pattern in the URL
    if match:
        return match.group(1)  # Return the extracted IP address
    return None  # Return None if no IP address is found

# Function to check if a URL has port 554 open (RTSP)
def check_rtsp_port(ip_address):
    port = 554  # RTSP default port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5)  # Set timeout for socket connection
        try:
            result = sock.connect_ex((ip_address, port))  # Attempt to connect to the RTSP port
            if result == 0:  # If connection is successful (result is 0)
                return f"http://{ip_address}:{port}"  # Return the URL with the RTSP port
            else:
                return None  # Return None if connection is not successful
        except socket.error as e:  # Handle socket errors
            print(f"Socket error for {ip_address}:{port} - {e}")  # Print error message
            return None  # Return None in case of socket error

# Main function to process URLs from input file and write URLs with RTSP port to output file
def main():
    input_file = "clean_sites.txt"  # Input file containing clean URLs
    output_file = "rtsp_sites.txt"  # Output file to store URLs with RTSP port

    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            url = line.strip()  # Remove leading/trailing whitespace and newline characters from the URL
            if not url:
                continue  # Skip empty lines

            ip_address = extract_ip(url)  # Extract IP address from the URL
            if ip_address:
                rtsp_url = check_rtsp_port(ip_address)  # Check if the IP address has RTSP port open
                if rtsp_url:
                    print(f"Found RTSP at: {rtsp_url}")  # Print RTSP URL if found
                    outfile.write(f"{rtsp_url}\n")  # Write RTSP URL to the output file
                    outfile.flush()  # Ensure immediate writing to the file
                else:
                    print(f"No RTSP found at: http://{ip_address}")  # Print message if no RTSP found
            else:
                print(f"Invalid URL format: {url}")  # Print message if URL format is invalid

if __name__ == "__main__":
    main()  # Call the main function if the script is executed directly
