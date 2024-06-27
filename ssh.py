def extract_ssh_addresses(input_file, output_file):
    ssh_addresses = []
    with open(input_file, "r") as infile:
        lines = infile.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("Open ports for"):
                try:
                    ip_start_index = line.index("http://") + len("http://")
                    ip_end_index = line.index(":", ip_start_index)
                    ip_address = line[ip_start_index:ip_end_index]
                    ports_start_index = line.index("[") + 1
                    ports_end_index = line.index("]")
                    ports_str = line[ports_start_index:ports_end_index]
                    ports = [int(port.strip()) for port in ports_str.split(",")]
                    if 22 in ports:  
                        ssh_addresses.append(ip_address)
                except ValueError:
                    pass  

    with open(output_file, "w") as outfile:
        for address in ssh_addresses:
            outfile.write(f"{address}\n")

def main():
    input_file = "ports.txt"
    output_file = "ssh.txt"
    extract_ssh_addresses(input_file, output_file)
    print(f"SSH addresses extracted from {input_file} and saved to {output_file}")

if __name__ == "__main__":
    main()
