import logging
import threading
import paramiko

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m-%d-%Y %H:%M:%S',
                    filename='stinger.log',
                    filemode='a')


def prepare_logger():
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    return logger


class StingerServer(paramiko.ServerInterface):

    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.log_file_path = 'stinger.log'
        self.logger = prepare_logger()
        self.logger.info('[*] Honeypot initializing...')
        self.logger.info('[*] Log file path: %s' % self.log_file_path)
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        # logging.info('client called check_channel_request ({}): {}'.format(
        #     self.client_ip, kind))
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

    def get_allowed_auths(self, username):
        # logging.info('client called get_allowed_auths ({}) with username {}'.format(
        #     self.client_ip, username))
        return "publickey, password"

    def check_auth_publickey(self, username, key):
        # fingerprint = u(hexlify(key.get_fingerprint()))
        # logging.info(
        #     'client public key ({}): username: {}, key name: {}, md5 fingerprint: {}, base64: {}, bits: {}'.format(
        #         self.client_ip, username, key.get_name(), fingerprint, key.get_base64(), key.get_bits()))
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_password(self, username, password):
        # Accept all passwords as valid by default
        # logging.info('new client credentials ({}): username: {}, password: {}'.format(
        #     self.client_ip, username, password))
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_exec_request(self, channel, command):
        # command_text = str(command.decode("utf-8"))
        #
        # logging.info('client sent command via check_channel_exec_request ({}): {}'.format(
        #     self.client_ip, command_text))
        return True