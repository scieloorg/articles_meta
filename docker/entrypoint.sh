#!/bin/bash
set -e

# inicia o webserver:
cd /app

python docker/generate_production_ini.py

/usr/bin/supervisord