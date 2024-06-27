import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 25565]

def scan_port(ip_address, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip_address, port))
        if result == 0:
            return port
        sock.close()
    except socket.error:
        return None

def scan_ports(ip_address):
    open_ports = []
    with ThreadPoolExecutor(max_workers=20) as executor:  # Adjust max_workers as needed
        futures = [executor.submit(scan_port, ip_address, port) for port in common_ports]
        for future in as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
    return open_ports

def main():
    input_file = "clean_sites.txt"
    output_file = "ports.txt"
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        urls = infile.readlines()

        for url in urls:
            url = url.strip()
            if url:
                ip_address = url_to_ip(url)
                if ip_address:
                    open_ports = scan_ports(ip_address)
                    if open_ports:
                        outfile.write(f"Open ports for {url}: {open_ports}\n")
                        print(f"Open ports for {url}: {open_ports}")
                    else:
                        outfile.write(f"No open ports found for {url}\n")
                        print(f"No open ports found for {url}")
                else:
                    outfile.write(f"Invalid URL format: {url}\n")
                    print(f"Invalid URL format: {url}")

def url_to_ip(url):
    parts = url.split('//')
    if len(parts) > 1:
        url = parts[1]
    host = url.split('/')[0]
    try:
        ip_address = socket.gethostbyname(host)
        return ip_address
    except socket.gaierror:
        return None

if __name__ == "__main__":
    main()
