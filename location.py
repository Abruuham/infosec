import ipinfo
import yaml

class IPInfo:

    def __init__(self, ip):
        self.ip = ip
        parsed_yaml = open('configs.yml')
        self.token = yaml.load(parsed_yaml, Loader=yaml.FullLoader)
        self.access_token = self.token['access_token']
        self.handler = ipinfo.getHandler(self.access_token)
        self.details = self.handler.getDetails(self.ip)

    def get_location(self):
        location = self.details.city + ', ' + self.details.country_name
        return location

    def get_coords(self):
        return self.details.loc
