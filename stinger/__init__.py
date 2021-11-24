import logging
from socket import socket, timeout
from colors import bcolors
import threading
from stinger.commands.command import StingerCommand


class Honeypot(object):

    def __init__(self, bind_ip, ports, log_file_path):
        if len(ports) < 1:
            raise Exception('No ports provided.')

        self.bind_ip = bind_ip
        self.ports = ports
        self.log_file_path = log_file_path
        self.listener_threads = {}
        self.logger = self.prepare_logger()

        self.logger.info('Honeypot initializing...')
        self.logger.info('Ports: %s' % self.ports)
        self.logger.info('Log file path: %s' % self.log_file_path)

    def handle_connection(self, client_socket, port, ip, remote_port):
        self.logger.info('Connection received: %s:%s: %d' % (port, ip, remote_port))
        client_socket.settimeout(10)
        try:
            data = client_socket.recv(1024)
            self.logger.info('Data received: %s: %s:%d: %s' % (port, ip, remote_port, data))
            client_socket.send((bcolors.COLOR['RED']+'Access Denied.').encode('utf8'))
            print('\n')
        except timeout:
            pass
        client_socket.close()

    def start_new_listener_thread(self, port):
        # create a new listener
        listener = socket()
        listener.bind((self.bind_ip, int(port)))
        listener.listen(5)
        while True:
            client, addr = listener.accept()
            self.logger.info('[*] Accepted connection from: %s:%d' % (addr[0], addr[1]))
            client_handler = threading.Thread(target=self.handle_connection, args=(client, port, addr[0], addr[1]))
            client_handler.start()

    def start_listening(self):
        for port in self.ports:
            self.listener_threads[port] = threading.Thread(target=self.start_new_listener_thread, args=(port,))
            self.listener_threads[port].start()

    def run(self):
        self.start_listening()


    def prepare_logger(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%m-%d-%Y %H:%M:%S',
                            filename=self.log_file_path,
                            filemode='w')
        logger = logging.getLogger(__name__)

        # Adding Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        return logger
