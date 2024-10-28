from configparser import ConfigParser
from vk import API, Session

config = ConfigParser()
config.read('config.ini')
vk_params = config['vk']
token = vk_params['token']
session = Session(access_token=token)
api = API(session, v=vk_params['api_version'])
