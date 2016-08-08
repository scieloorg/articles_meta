# -*- coding: utf-8 -*-
import os
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0


PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MONGO_SETTINGS = {
    'host': 'articlemeta-mongo',  # ver hostname: docker-compose.yml
    'port': '27017',
    'dbname': 'scielo_network'
}
WEBAPP_PORT = 8000  # ver ports: docker-compose.yml e Dockerfile

production_template_ini_filepath = os.path.join(PROJECT_PATH + '/production-TEMPLATE.ini')
new_production_ini_filepath = os.path.join(PROJECT_PATH + '/production.ini')

config = ConfigParser()
config.read(production_template_ini_filepath)
config.set('app:main', 'mongo_uri', 'mongodb://{host}:{port}/{dbname}'.format(**MONGO_SETTINGS))
config.set('server:main', 'port', WEBAPP_PORT)

with open(new_production_ini_filepath, 'w') as configfile:    # save
    config.write(configfile)
