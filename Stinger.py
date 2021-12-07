# -*- coding: utf-8 -*-

import logging
import socket
import threading
import argparse
import time
import sys
import traceback
import paramiko
import colors
import os
from twisted.python import log
from commands import __all__
from pynput import keyboard
from commands.adduser import Command_adduser
from commands.apt import APTCommand
from StingerServer import StingerServer
from commands.ls import LSCommand

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

COMMANDS = {}

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m-%d-%Y %H:%M:%S',
                    filename='stinger.log',
                    filemode='a')


def handle_command(cmd, chan,transport):
    response = ''
    if cmd.startswith('ls'):
        x = cmd.split(' ')
        y = LSCommand()
        y.start(x, chan)
    elif cmd.startswith('pwd'):
        response = '/home/root/'
    elif cmd.startswith('adduser'):
        y = cmd.split(' ')
        t = Command_adduser()
        l = t.start(y[1], chan, transport)
    elif cmd.startswith('apt'):
        y = cmd.split(' ')
        t = APTCommand()
        l = t.start(y, chan)
    if response != '':
        response = response + '\r\n'
    chan.send(response)


def handle_connection(client, addr):
    client_ip = addr[0]
    logging.info('New connection from: {}'.format(client_ip))
    print('[*] New connection from: {}'.format(client_ip))

    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(HOST_KEY)
        server = StingerServer(client_ip)
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

        try:
            chan.send('root@192.168.1.242\'s password: ')
            passwd = ''
            while not passwd.endswith('\r'):
                p = chan.recv(1024)
                if (
                        transport != UP_KEY
                        and transport != DOWN_KEY
                        and transport != LEFT_KEY
                        and transport != RIGHT_KEY
                        and transport != BACK_KEY
                ):
                    passwd += p.decode("utf-8")

            date = time.ctime()
            chan.send("\r\n\r\nLinux kali 4.19.0-kali4-amd64 #1 SMP Debian 4.19.28-2kali1 (2019-03-18) x86_64\r\n\r\n")
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
                    elif transport == BACK_KEY:
                        chan.send(transport)
                        command += transport.decode('utf-8')

                chan.send("\r\n")
                command = command.rstrip()
                logging.info('Command received ({}): {}'.format(client_ip, command))
                print('[*] Command received ({}): {}'.format(client_ip, command))
                # detect_url(command, client_ip)

                if command == "exit":
                    chan.send('logout\r\n')
                    run = False

                else:
                    handle_command(command, chan, transport)

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
        print('Listening for connection ...\r\n')
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
            client, addr = sock.accept()
        except Exception as err:
            print('*** Listen/accept failed: {}'.format(err))
            traceback.print_exc()
        new_thread = threading.Thread(target=handle_connection, args=(client, addr))
        new_thread.start()
        threads.append(new_thread)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Stinger SSH Honeypot")
    parser.add_argument("--port", "-p", help="The port to bind the ssh server to (default 22)", default=2222, type=int,
                        action="store")
    parser.add_argument("--bind", "-b", help="The address to bind the ssh server to", default="", type=str,
                        action="store")
    args = parser.parse_args()

    list = os.system("who")
    print(list)

    command = 'iptables -A PREROUTING -t nat -p tcp --dport 22 -j REDIRECT --to-port {}'.format(args.port)
    os.system(command)

    start_server(args.port, args.bind)
