import subprocess

def scan_ssh_addresses(input_file, output_file):
    with open(input_file, "r") as infile:
        addresses = infile.readlines()
        for address in addresses:
            address = address.strip()
            if address:
                try:
                    command = f"nmap -p 22 -sV {address}"
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    output = result.stdout
                    
                    ssh_info = parse_ssh_info(output)
                    
                    with open(output_file, "a") as outfile:
                        if ssh_info:
                            outfile.write(f"{address}:22\n{ssh_info}\n\n")
                            print(f"{address}:22\n{ssh_info}")
                        else:
                            outfile.write(f"{address}:22\nNo SSH information found\n\n")
                            print(f"{address}:22\nNo SSH information found")
                except Exception as e:
                    print(f"Error scanning {address}: {e}")

def parse_ssh_info(nmap_output):
    lines = nmap_output.splitlines()
    for line in lines:
        if "OpenSSH" in line:
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
