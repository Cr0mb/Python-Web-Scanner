import requests
import ipaddress
import argparse

def get_ip_location(ip_address):
    url = f"https://ipapi.co/{ip_address}/json/"
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

    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            url = line.strip()
            if not url:
                continue

            ip_address = extract_ip(url)
            if ip_address:
                location_info = get_ip_location(ip_address)
                if location_info:
                    print(f"IP: {ip_address}")
                    print(f"Country: {location_info.get('country_name', 'N/A')}")
                    print(f"State: {location_info.get('region', 'N/A')}")
                    print(f"City: {location_info.get('city', 'N/A')}")
                    print(f"ISP: {location_info.get('org', 'N/A')}")
                    print(f"Latitude: {location_info.get('latitude', 'N/A')}")
                    print(f"Longitude: {location_info.get('longitude', 'N/A')}")
                    print(f"Organization: {location_info.get('org', 'N/A')}")
                    print()

                    outfile.write(f"IP: {ip_address}\n")
                    outfile.write(f"Country: {location_info.get('country_name', 'N/A')}\n")
                    outfile.write(f"State: {location_info.get('region', 'N/A')}\n")
                    outfile.write(f"City: {location_info.get('city', 'N/A')}\n")
                    outfile.write(f"ISP: {location_info.get('org', 'N/A')}\n")
                    outfile.write(f"Latitude: {location_info.get('latitude', 'N/A')}\n")
                    outfile.write(f"Longitude: {location_info.get('longitude', 'N/A')}\n")
                    outfile.write(f"Organization: {location_info.get('org', 'N/A')}\n")
                    outfile.write("\n")
                else:
                    print(f"No location information found for IP: {ip_address}")
                    outfile.write(f"No location information found for IP: {ip_address}\n\n")
            else:
                print(f"Invalid URL format: {url}")

def extract_ip(url):
    try:
        ip_address = ipaddress.ip_address(url.strip("http://")) 
        return str(ip_address)
    except ValueError:
        return None  

if __name__ == "__main__":
    main()





