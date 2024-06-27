import subprocess

def scan_ssh_addresses(input_file, output_file):
    with open(input_file, "r") as infile:
        addresses = infile.readlines()
        for address in addresses:
            address = address.strip()
            if address:
                if ':' in address:
                    ip, port = address.split(':')
                else:
                    ip = address
                    port = '22'
                
                try:
                    command = f"nmap -p {port} -sV {ip}"
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    output = result.stdout
                    
                    ssh_info = parse_ssh_info(output)
                    
                    with open(output_file, "a") as outfile:
                        if ssh_info:
                            output_to_write = f"{ip}:{port}\n{ssh_info}\n\n"  # Add an extra newline here
                            outfile.write(output_to_write)
                            print(output_to_write.strip())
                        else:
                            output_to_write = f"{ip}:{port}\nNo SSH information found\n\n"  # Add an extra newline here
                            outfile.write(output_to_write)
                            print(output_to_write.strip())
                except Exception as e:
                    print(f"Error scanning {ip}:{port}: {e}")

def parse_ssh_info(nmap_output):
    lines = nmap_output.splitlines()
    ssh_keywords = ["OpenSSH", "Dropbear", "libssh", "libssh2", "PuTTY", "Tectia"]
    
    for line in lines:
        for keyword in ssh_keywords:
            if keyword in line:
                return line.strip()
    return None

def main():
    input_file = "ssh.txt"
    output_file = "nmap.txt"
    with open(output_file, "w") as outfile:
        outfile.write("Nmap Scan Results:\n\n")
    scan_ssh_addresses(input_file, output_file)
    print(f"Scan results saved to {output_file}")

if __name__ == "__main__":
    main()
