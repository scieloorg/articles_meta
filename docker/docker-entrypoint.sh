#!/bin/bash
set -e

# inicia o webserver:
pserve production.ini 2>&1 &

# inicia o thirft server
articlemeta_thrift_server --port 11620 --host 0.0.0.0
