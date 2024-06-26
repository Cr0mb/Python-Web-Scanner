import requests
import ipaddress
import argparse
import time

def get_ip_location(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve information for {ip_address}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving information for {ip_address}: {str(e)}")
        return None

def main():
    input_file = "clean_sites.txt"
    output_file = "locations.txt"

    with open(input_file, "r", encoding="utf-8") as infile:
        ip_addresses = [extract_ip(line.strip()) for line in infile if line.strip()]

    with open(output_file, "w", encoding="utf-8") as outfile:
        for ip_address in ip_addresses:
            if ip_address:
                location_info = get_ip_location(ip_address)
                if location_info and location_info["status"] == "success":
                    print(f"IP: {ip_address}")
                    print(f"Country: {location_info.get('country', 'N/A')}")
                    print(f"Region: {location_info.get('regionName', 'N/A')}")
                    print(f"City: {location_info.get('city', 'N/A')}")
                    print(f"ISP: {location_info.get('isp', 'N/A')}")
                    print(f"Latitude: {location_info.get('lat', 'N/A')}")
                    print(f"Longitude: {location_info.get('lon', 'N/A')}")
                    print(f"Organization: {location_info.get('org', 'N/A')}")
                    print()

                    outfile.write(f"IP: {ip_address}\n")
                    outfile.write(f"Country: {location_info.get('country', 'N/A')}\n")
                    outfile.write(f"Region: {location_info.get('regionName', 'N/A')}\n")
                    outfile.write(f"City: {location_info.get('city', 'N/A')}\n")
                    outfile.write(f"ISP: {location_info.get('isp', 'N/A')}\n")
                    outfile.write(f"Latitude: {location_info.get('lat', 'N/A')}\n")
                    outfile.write(f"Longitude: {location_info.get('lon', 'N/A')}\n")
                    outfile.write(f"Organization: {location_info.get('org', 'N/A')}\n")
                    outfile.write("\n")
                else:
                    print(f"No location information found for IP: {ip_address}")
                    outfile.write(f"No location information found for IP: {ip_address}\n\n")
                    
                time.sleep(1)
            else:
                print(f"Invalid URL format or IP address: {ip_address}")

def extract_ip(url):
    try:
        ip_address = ipaddress.ip_address(url.strip("http://"))  
        return str(ip_address)
    except ValueError:
        return None  

if __name__ == "__main__":
    main()
