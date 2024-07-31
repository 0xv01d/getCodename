#!/usr/bin/env python3

import sys
import requests
import argparse
from termcolor import colored, cprint
from urllib.parse import quote
from bs4 import BeautifulSoup

def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract SSH version and search for distro codename on Launchpad.")
    parser.add_argument('-f', '--file', help="File containing nmap output", type=str)
    parser.add_argument('-s', '--ssh-version', help="SSH version string to search", type=str)
    parser.add_argument('-n', '--num-results', help="Number of Launchpad search results to retrieve (Default 1).", type=int, default=1)
    args = parser.parse_args()
    # If no arguments are provided, print the help message
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)
    return args

def extract_ssh_version(output):
    lines = output.split('\n')
    for line in lines:
        if "OpenSSH" in line:
            words = line.split()
            return ' '.join(words[6:10])
    return None

def main():
    args = parse_arguments()
    num_results = args.num_results
    ssh_version = args.ssh_version
    if not ssh_version and args.file:
        try:
            with open(args.file, 'r') as f:
                output = f.read()
            ssh_version = extract_ssh_version(output)
        except Exception as e:
            cprint(f"[-] Error reading file: {e}", "red")
            sys.exit(1)

    if not ssh_version:
        cprint("\n[-] SSH version not provided.", "red")
        sys.exit(1)

    cprint(f"\nSSH Version: {ssh_version}\n", "magenta")

    base_url = "https://launchpad.net/+search?field.text=OpenSSH+"
    search_url = base_url + quote(ssh_version)

    try:
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        ul_matches = soup.find('ul', class_='site-matches')
        if ul_matches:
            first_link = ul_matches.find('a', href=True)
            links_result = ul_matches.findAll('a', href=True)

            if first_link:
                if num_results > 1:
                    links_result = links_result[:num_results]
                    cprint(f"Launchpad Results\n", "light_green")
                    for link in links_result:
                        print(colored(f"{link['href']}\n\t", "yellow", attrs=["bold", "underline"]),colored(f"{link.text}\n", "red"))
                match_url = first_link['href']

                match_response = requests.get(match_url)
                match_response.raise_for_status()
                match_soup = BeautifulSoup(match_response.text, 'html.parser')

                dt_tag = match_soup.find('dt', string='Uploaded to:'.strip())
                if dt_tag is not None:
                    dd_tag = dt_tag.find_next_sibling('dd')
                    if dd_tag is not None:
                        codename = dd_tag.a.text if dd_tag.a is not None else 'No codename found'
                        print(colored(f"[+] Codename: {codename}", "green"), colored(" -> ","white", attrs=["blink"]),colored(f"{match_url}", "cyan", attrs=["bold", "underline"]))
                    else:
                        cprint("[-] No codename matches found.", "red")
                else:
                    cprint("[-] No codename matches found.", "red")
            else:
                cprint("[-] No matching results found on Launchpad.", "red")
        else:
            cprint("[-] No matching results found on Launchpad.", "red")

    except requests.RequestException as e:
        cprint(f"[-] Error during HTTP request: {e}", "red")
    except Exception as e:
        cprint(f"[-] Error processing the response: {e}", "red")

if __name__ == "__main__":
    main()
