"""
Simple Honeypot

Usage:
    honeypot.py <config_file_path>
Options:
    <config_file_path>  Path to config options .ini file.
    -h --help           Show this screen.
"""

import configparser
from honeypot import Honeypot
import sys

# Check arguments
if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
    print(__doc__)
    sys.exit(1)

# Load config
config_file_path = sys.argv[1]
config = configparser.ConfigParser()
config.read(config_file_path)

ports = config.get('default', 'ports', raw=True, fallback='22,80,443,8080,8888,9999,3306')
host = config.get('default', 'host', raw=True, fallback='0.0.0.0')
log_file_path = config.get('default', 'logfile', raw=True, fallback='/var/log/honeypot.log')

# Double check ports provided
ports_list = []
try:
    ports_list = ports.split(',')
except Exception as e:
    print('[-] Error parsing ports: %s,\nExiting', ports)
    sys.exit(1)

# Launch honeypot
honeypot = Honeypot(host, ports_list, log_file_path)
honeypot.run()
