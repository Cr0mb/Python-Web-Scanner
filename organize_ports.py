import os
import time

# Dictionary mapping ports to service names
port_services = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    465: "SMTPS",
    587: "SMTP (Submission)",
    993: "IMAPS",
    995: "POP3S",
    25565: "Minecraft"
}

# List of common ports
common_ports = list(port_services.keys())

def extract_addresses(input_file, port, output_file):
    addresses = []
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
                    if port in ports:
                        addresses.append(f"{ip_address}:{port}")
                except ValueError:
                    pass

    with open(output_file, "w") as outfile:
        for address in addresses:
            outfile.write(f"{address}\n")

def main():
    input_file = "ports.txt"
    
    while True:
        # Clear the screen
        if os.name == 'posix':  # for Unix-like systems
            _ = os.system('clear')
        else:  # for Windows systems
            _ = os.system('cls')

        print("Select a port to extract addresses (or enter 'q' to quit):")
        print("Available ports:")
        for port in common_ports:
            if port in port_services:
                service_name = port_services[port]
                print(f"{port}: {service_name}")
        
        choice = input("Enter port number: ")
        
        if choice.lower() == 'q':
            break
        
        try:
            port = int(choice)
            if port in common_ports:
                service_name = port_services[port]
                output_file = f"{service_name.lower()}.txt"  # Output file named after service name
                extract_addresses(input_file, port, output_file)
                print(f"Addresses with port {port} ({port_services[port]}) extracted from {input_file} and saved to {output_file}")
                time.sleep(1)
            else:
                print("Invalid port number. Please select from the list.")
        except ValueError:
            print("Invalid input. Please enter a valid port number.")

if __name__ == "__main__":
    main()
