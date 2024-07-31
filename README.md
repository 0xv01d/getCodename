# getCodename

getCodename is a Python script designed to assist in the enumeration phase during red teaming engagements. The tool searches for the corresponding distro codename on Launchpad given the OpenSSH version string provided as argument or from a Nmap output file in normal format (-oN). This can help in identifying potential vulnerabilities, dockerized environments or version-specific features.

---

## Features

- **Extract SSH Version:**: Automatically extract the OpenSSH version from Nmap output.
- **Search Launchpad**: Query Launchpad for Distro release information using the extracted or provided SSH version.
- **Identify Codename**: Retrieve the Distro codename associated with the specific OpenSSH version.

## Installation

Clone the repository:
```sh
git clone https://github.com/0xv01d/getCodename.git
cd getCodename
```

Install the required Python packages:
```sh
pip install -r requirements.txt
```

## Usage

Run the script with Python, using either the Nmap output file or the SSH version string as input.

```sh
python getCodename.py [OPTIONS]...
```

## Options

- **-f, --file** : Path to a file containing Nmap output.
- **-s, --ssh-version** : SSH version string to search (e.g., "OpenSSH_8.9p1 Ubuntu 3ubuntu0.6").
- **-n, --num-results** : Number of Launchpad search results to retrieve (default is 1).
- **-h, --help** : Show this help message and exit.

## Examples

Extract SSH version from Nmap output:
```sh
python getCodename.py -f nmap_output.txt
```

Use a specific SSH version string:
```sh
python getCodename.py -s "OpenSSH_8.9p1 Ubuntu 3ubuntu0.6"
```

Specify the number of search results:
```sh
python getCodename.py -f nmap_output.txt -n 3
```
Note: For best results, the SSH version string should be in the format: "8.9p1 Ubuntu 3ubuntu0.6".

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome, fork this repository and submit a pull request for any improvements.

---

**Author**
[**0xv01d**](https://0xv01d.github.io)

