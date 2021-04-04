#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/vaccinalert/")

from vaccinalert import app as application
key = open("secret_key", "r").read()
print(key)

application.secret_key = key.strip()
