import os
import json

# Used for controlling the database setup when running the test suite
IS_TESTING = False
RC_NAME = 'kvikler_settings.json'

__version__ = '0.0.1'


# Possible locations for configuration file
search_files = [
    # HOME is usually either /home/user or C:\Users\user
    os.path.join(os.environ.get('HOME'), '.' + RC_NAME), # with a dot for unix users
    os.path.join(os.environ.get('HOME'), RC_NAME), # without a dot for windows users
    os.path.join('/etc', RC_NAME),
    os.path.join('C:\\Users\\Default\\AppData\\Local\\kvikler', RC_NAME),
]

for conf_file in search_files:
    if os.path.isfile(conf_file):
        with open(conf_file) as conf:
            settings = json.load(conf)
            if settings.has_key('connection'):
                conf_db = settings['connection']
                if not (conf_db.has_key('username') and conf_db.has_key('password') and
                        conf_db.has_key('hostname') and conf_db.has_key('database') and
                        conf_db.has_key('schema')):
                    raise ValueError('Malformed config file. Consult documentation!')
        break
else:
    raise EnvironmentError('Configuration file not found!')

username = conf_db['username']
password = conf_db['password']
hostname = conf_db['hostname']
database = conf_db['database']
schema = conf_db['schema']
if conf_db.has_key('port'):
    port = conf_db['port']
else:
    port = 5432

con_str = 'postgresql://{usr}:{pswd}@{host}:{port}'.format(
    usr=username,
    pswd=password,
    host=hostname,
    port=port,
)

conf_db = None

