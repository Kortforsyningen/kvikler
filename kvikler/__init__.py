import os
import json
import getpass
from pathlib import Path

# Used for controlling the database setup when running the test suite
IS_TESTING = False
RC_NAME = 'kvikler_settings.json'

__version__ = '0.0.1'

if os.environ.get('HOME'):
    home = Path.os.environ['HOME']
else:
    home = Path('')

search_files = [
    home / Path(RC_NAME),
    home / Path('.' + RC_NAME),
    Path('/etc') / Path(RC_NAME),
    Path('C:\\Users') / Path(getpass.getuser()) / Path(RC_NAME),
    Path('C:\\Users\\Default\\AppData\\Local\\kvikler') / Path(RC_NAME),
]


for conf_file in search_files:
    if os.path.isfile(conf_file):
        with open(conf_file) as conf:
            settings = json.load(conf)
            if 'connection' in settings:
                conf_db = settings['connection']
                if not ('username' in conf_db and 'password' in conf_db and
                        'hostname' in conf_db and 'database' in conf_db and
                        'schema' in conf_db):
                    raise ValueError('Malformed config file. Consult documentation!')
        break
else:
    raise EnvironmentError('Configuration file not found!')

username = conf_db['username']
password = conf_db['password']
hostname = conf_db['hostname']
database = conf_db['database']
schema = conf_db['schema']
if 'port' in conf_db:
    port = conf_db['port']
else:
    port = 5432

con_str = 'postgresql://{usr}:{pswd}@{host}:{port}/{db}'.format(
    usr=username,
    pswd=password,
    host=hostname,
    port=port,
    db=database,
)

conf_db = None

