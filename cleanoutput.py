import re


def is_valid_domain(url):
    # Define a regex to check if a string is a valid domain URL
    domain_regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?![0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)'  # Exclude IP addresses
        r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?))'  # domain...
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE)
    return re.match(domain_regex, url) is not None


def filter_links(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        lines = infile.readlines()
        for line in lines:
            # Split the line into original URL and redirected URL
            parts = line.split(" -> ")
            if len(parts) == 2:
                original_url, redirected_url = parts
                redirected_url = redirected_url.strip()
                # Check if the redirected URL is a valid domain URL
                if is_valid_domain(redirected_url):
                    # Write the valid redirected URL to the output file
                    outfile.write(line)


# Define input and output file paths
input_file = "output.txt"
output_file = "filtered_output.txt"

# Filter the links
filter_links(input_file, output_file)
