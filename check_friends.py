from configparser import ConfigParser
from json import dumps
from os import listdir
from requests.exceptions import ConnectionError
from time import localtime
from vk import API, Session

config = ConfigParser()
config.read('config.ini')

work_dir = 'work/'
friends_path = work_dir + 'friends'
log_path = work_dir + 'friends.log'
vk_params = config['vk']
token = vk_params['token']
target_id = int(config['target']['ids'])

session = Session(access_token=token)
api = API(session, v=vk_params['api_version'])


def get_friends():
    try:
        raw_friends = api.friends.get(user_id=target_id)
        friends = set(raw_friends['items'])
    except ConnectionError:
        friends = None
    return friends


def log(entry, success=True, befriended=(), unfriended=()):
    if success:
        entry['+'] = befriended
        entry['-'] = unfriended
    else:
        entry['status'] = 'Unable to connect to vk server'
    with open(log_path, 'a') as f:
        f.write(dumps(entry) + '\n')

actual_friends = get_friends()
entry = {'ts': localtime()}

if actual_friends:
    if 'friends' in listdir('work'):
        with open(friends_path, 'r') as f:
            old_friends = {int(line) for line in f}
    else:
        old_friends = set()

    befriended = actual_friends - old_friends
    unfriended = old_friends - actual_friends
    log(entry, befriended=tuple(befriended), unfriended=tuple(unfriended))

    if befriended or unfriended:
        with open(friends_path, 'w') as f:
            f.write('\n'.join(str(friend) for friend in actual_friends))
else:
    log(entry, success=False)
    exit()
