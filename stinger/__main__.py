"""

Usage:
    honeypot.py <config_file_path>
Options:
    <config_file_path>               Path to config options .ini file.
    -h --help                        Show this screen.
"""

import configparser
from stinger import Honeypot, StartServer
import sys
import colors


print(
    colors.bcolors.COLOR['YELLOW'] +
    '============================================================================\n' +
    ' $$$$$$\  $$$$$$$$\  $$$$$$\ |$$\   $$\   /$$$$$$\   |$$$$$$$$\  |$$$$$$$\\ \n' +
    '$$  __$$\ \__$$  __| \_$$  _||$$$\  $$ | |$$  __$$\  |$$  _____| |$$  __$$\\\n' +
    '$$ /  \__|  $$  |      $$ |  |$$$$\ $$ | |$$ /  \__| |$$ |       |$$ |  $$ |\n' +
    '\$$$$$$\    $$  |      $$ |  |$$ $$\$$ | |$$ |$$$$\  |$$$$$\     |$$$$$$$  |\n' +
    ' \____$$\   $$  |      $$ |  |$$ \$$$$ | |$$ |\_$$ | |$$  __|    |$$  __$$< \n' +
    '$$\   $$ |  $$  |      $$ |  |$$ |\$$$ | |$$ |  $$ | |$$ |       |$$ |  $$ |\n' +
    '\$$$$$$  |  $$  |    $$$$$$\ |$$ | \$$ | \$$$$$$   | |$$$$$$$$\  |$$ |  $$ |\n' +
    '\_______/   \___|    \_____|  \__|  \__|  \_______/  \________|   \__|  \__|\n' +
    '\n' +
    '                             \     /                                        \n' +
    '                         \    o ^ o    /                                    \n' +
    '                           \ (     ) /                                      \n' +
    '                ____________(%%%%%%%)____________                           \n' +
    '               (     /   /  )%%%%%%%(  \   \     )                          \n' +
    '               (___/___/__/           \__\___\___)                          \n' +
    '                  (     /  /(%%%%%%%)\  \     )                             \n' +
    '                   (__/___/ (%%%%%%%) \___\__)                              \n' +
    '                           /(       )\\                                     \n' +
    '                         /   (%%%%%)   \\                                   \n' +
    '                              (%%%)                                         \n' +
    '                               \ /                                          \n' +
    '                                V                                           \n' +
    '                                |                                           \n' +
    '============================================================================\n' +
    colors.bcolors.COLOR['RESET_ALL']
)

# Check arguments
if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
    print(__doc__)
    sys.exit(1)
else:
    # Load config
    config_file_path = 'honeypot.ini'
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
    server = StartServer(host, ports_list, log_file_path)
    honeypot.run()


