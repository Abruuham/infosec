# -*- coding: utf-8 -*-
"""

Usage:
    honeypot.py <config_file_path>
Options:
    <config_file_path>               Path to config options .ini file.
    -h --help                        Show this screen.
"""

import logging
import socket
import threading
import argparse
import time
import sys
import traceback
from binascii import hexlify
import paramiko
from paramiko.py3compat import u
import colors

print(
    colors.bcolors.COLOR['YELLOW'] +
    '============================================================================\n' +
    ' /$$$$$$\  $$$$$$$$\ $$$$$$\ |$$\   $$\   /$$$$$$\   |$$$$$$$$\  |$$$$$$$\\ \n' +
    '|$$  __$$\ \__$$  __|\_$$ _| |$$$\  $$ | |$$  __$$\  |$$  _____| |$$  __$$\\\n' +
    '|$$ /  \__|  |$$ |    |$$ |  |$$$$\ $$ | |$$ /  \__| |$$ |       |$$ |  $$ |\n' +
    '\$$$$$$\     |$$ |    |$$ |  |$$ $$\$$ | |$$ |$$$$\  |$$$$$\     |$$$$$$$  |\n' +
    ' \____$$\    |$$ |    |$$ |  |$$ \$$$$ | |$$ |\_$$ | |$$  __|    |$$  __$$< \n' +
    '|$$\  $$ |   |$$ |    |$$ |  |$$ |\$$$ | |$$ |  $$ | |$$ |       |$$ |  $$ |\n' +
    '\$$$$$$  |   |$$ |   $$$$$$\ |$$ | \$$ | \$$$$$$   | |$$$$$$$$\  |$$ |  $$ |\n' +
    '\_______/    \___|   \_____|  \__|  \__|  \_______/  \________|   \__|  \__|\n' +
    '\n' +
    '                                 \     /                                    \n' +
    '                             \    o ^ o    /                                \n' +
    '                               \ (     ) /                                  \n' +
    '                    ____________(%%%%%%%)____________                       \n' +
    '                   (     /   /  )%%%%%%%(  \   \     )                      \n' +
    '                   (___/___/__/           \__\___\___)                      \n' +
    '                      (     /  /(%%%%%%%)\  \     )                         \n' +
    '                       (__/___/ (%%%%%%%) \___\__)                          \n' +
    '                               /(       )\\                                 \n' +
    '                             /   (%%%%%)   \\                               \n' +
    '                                  (%%%)                                     \n' +
    '                                   \ /                                      \n' +
    '                                    V                                       \n' +
    '                                    |                                       \n' +
    '============================================================================\n' +
    colors.bcolors.COLOR['RESET_ALL']
)

HOST_KEY = paramiko.RSAKey(filename='server.key')

UP_KEY = '\x1b[A'.encode()
DOWN_KEY = '\x1b[B'.encode()
RIGHT_KEY = '\x1b[C'.encode()
LEFT_KEY = '\x1b[D'.encode()
BACK_KEY = '\x7f'.encode()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m-%d-%Y %H:%M:%S',
                    filename='stinger.log',
                    filemode='a')


def prepare_logger():
    logger = logging.getLogger(__name__)

    # Adding Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    return logger


class StingerPot(paramiko.ServerInterface):

    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.log_file_path = 'honeypot.log'
        self.logger = prepare_logger()
        self.logger.info('Honeypot initializing...')
        self.logger.info('Log file path: %s' % self.log_file_path)
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        logging.info('client called check_channel_request ({}): {}'.format(
            self.client_ip, kind))
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

    def get_allowed_auths(self, username):
        logging.info('client called get_allowed_auths ({}) with username {}'.format(
            self.client_ip, username))
        return "publickey,password"

    def check_auth_publickey(self, username, key):
        fingerprint = u(hexlify(key.get_fingerprint()))
        logging.info(
            'client public key ({}): username: {}, key name: {}, md5 fingerprint: {}, base64: {}, bits: {}'.format(
                self.client_ip, username, key.get_name(), fingerprint, key.get_base64(), key.get_bits()))
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_password(self, username, password):
        # Accept all passwords as valid by default
        logging.info('new client credentials ({}): username: {}, password: {}'.format(
            self.client_ip, username, password))
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_exec_request(self, channel, command):
        command_text = str(command.decode("utf-8"))

        logging.info('client sent command via check_channel_exec_request ({}): {}'.format(
            self.client_ip, command_text))
        return True


def handle_command(cmd, chan, ip):
    response = ''
    if cmd.startswith('ls'):
        response = 'users.txt'
    elif cmd.startswith('pwd'):
        response = '/home/root/'

    if response != '':
        response = response + '\r\n'

    chan.send(response)


def handle_connection(client, addr):
    client_ip = addr[0]
    logging.info('New connection from: {}'.format(client_ip))
    print('New connection from: {}'.format(client_ip))

    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(HOST_KEY)
        server = StingerPot(client_ip)
        try:
            transport.start_server(server=server)

        except paramiko.SSHException:
            print('*** SSH negotiation failed.')
            raise Exception("SSH negotiation failed")

        # wait for auth
        chan = transport.accept(10)
        if chan is None:
            print('*** No channel (from ' + client_ip + ').')
            raise Exception("No channel")

        chan.settimeout(10800)

        if transport.remote_mac != '':
            logging.info('Client mac ({}): {}'.format(client_ip, transport.remote_mac))

        if transport.remote_compression != '':
            logging.info('Client compression ({}): {}'.format(client_ip, transport.remote_compression))

        if transport.remote_version != '':
            logging.info('Client SSH version ({}): {}'.format(client_ip, transport.remote_version))

        if transport.remote_cipher != '':
            logging.info('Client SSH cipher ({}): {}'.format(client_ip, transport.remote_cipher))

        server.event.wait(10)
        if not server.event.is_set():
            logging.info('** Client ({}): never asked for a shell'.format(client_ip))
            raise Exception("No shell request")

        # chan.send("root@localhost's password: "+colors.bcolors.COLOR['CLEAR'])

        try:
            date = time.ctime()
            chan.send("Linux kali 4.19.0-kali4-amd64 #1 SMP Debian 4.19.28-2kali1 (2019-03-18) x86_64\r\n\r\n")
            chan.send("The programs included with the Kali GNU/Linux system are free software;\r\n" +
                      "the exact distribution terms for each program are described in the\r\n" +
                      "individual files in /usr/share/doc/*/copyright.\r\n\r\n" +
                      "Kali GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent\r\n" +
                      "permitted by applicable law.\r\n" +
                      "Last login: " + date + " from " + str(client_ip) + "\r\n" +
                      "┏━(" + colors.bcolors.COLOR["RED"] + "Message from Kali developers" +
                      colors.bcolors.COLOR["RESET_ALL"] + ")\r\n" +
                      "┃\r\n" +
                      "┃ This is a minimal installation of Kali Linux, you likely\r\n" +
                      "┃ want to install supplementary tools. Learn how:\r\n" +
                      "┃ ⇒ https://www.kali.org/docs/troubleshooting/common-minimum-setup/\r\n" +
                      "┃\r\n" +
                      "┗━(" + colors.bcolors.COLOR['GREY'] + "Run “touch ~/.hushlogin” to hide this message)" +
                      colors.bcolors.COLOR['RESET_ALL'] + "\r\n")

            run = True
            while run:
                chan.send(colors.bcolors.COLOR['RED'] + "root@kali" + colors.bcolors.COLOR['RESET_ALL'] + ':' +
                          colors.bcolors.COLOR['BLUE'] + '~' + colors.bcolors.COLOR['RESET_ALL'] + '# ')
                command = ""
                while not command.endswith("\r"):
                    transport = chan.recv(1024)
                    # Echo input to pseudo-simulate a basic terminal
                    if (
                            transport != UP_KEY
                            and transport != DOWN_KEY
                            and transport != LEFT_KEY
                            and transport != RIGHT_KEY
                            and transport != BACK_KEY
                    ):
                        chan.send(transport)
                        command += transport.decode("utf-8")

                chan.send("\r\n")
                command = command.rstrip()
                logging.info('Command received ({}): {}'.format(client_ip, command))
                print('Command received ({}): {}'.format(client_ip, command))
                # detect_url(command, client_ip)

                if command == "exit":
                    chan.send('logout\r\nConnection to 192.168.1.242 closed')
                    run = False

                else:
                    handle_command(command, chan, client_ip)

        except Exception as err:
            print('!!! Exception: {}: {}'.format(err.__class__, err))
            try:
                transport.close()
            except Exception:
                pass

        chan.close()

    except Exception as err:
        print('!!! Exception: {}: {}'.format(err.__class__, err))
        try:
            transport.close()
        except Exception:
            pass


def start_server(port, bind):
    """Init and run the ssh server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((bind, port))
    except Exception as err:
        print('*** Bind failed: {}'.format(err))
        traceback.print_exc()
        sys.exit(1)

    threads = []
    while True:
        try:
            sock.listen(100)
            print('Listening for connection ...')
            client, addr = sock.accept()
        except Exception as err:
            print('*** Listen/accept failed: {}'.format(err))
            traceback.print_exc()
        new_thread = threading.Thread(target=handle_connection, args=(client, addr))
        new_thread.start()
        threads.append(new_thread)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", "-p", help="The port to bind the ssh server to (default 22)", default=2222, type=int,
                        action="store")
    parser.add_argument("--bind", "-b", help="The address to bind the ssh server to", default="", type=str,
                        action="store")
    args = parser.parse_args()
    start_server(args.port, args.bind)
