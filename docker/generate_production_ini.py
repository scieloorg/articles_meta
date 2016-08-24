# -*- coding: utf-8 -*-
import os
import uuid

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0


PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

production_template_ini_filepath = os.path.join(PROJECT_PATH + '/production-TEMPLATE.ini')
new_production_ini_filepath = os.path.join(PROJECT_PATH + '/production.ini')

config = ConfigParser()
config.read(production_template_ini_filepath)
config.set('app:main', 'mongo_uri', 'mongodb://{mongodb_host}/articlemeta' % os.environ.get('MONGODB_HOST', '127.0.0.1:27017'))
config.set('app:main', 'admintoken', os.environ.get('ADMIN_TOKEN', uuid.uuid4().hex))
config.set('server:main', 'port', 8000)

with open(new_production_ini_filepath, 'w') as configfile:    # save
    config.write(configfile)
