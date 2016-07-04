#!/usr/bin/env python

import configparser
import os

from slackclient import SlackClient

BOT_NAME = 'isitupbot'

config = configparser.ConfigParser()
# CUR_DIR = os.path.abspath('.')
# PAR_DIR = os.path.dirname(CUR_DIR)
# SETTINGS_FILE = os.path.join(PAR_DIR, 'settings.ini')

SETTINGS_FILE = 'settings.ini'

config.read(SETTINGS_FILE)
sc = SlackClient(config.get('slack', 'SLACK_BOT_TOKEN'))

def bot_id():
    api_call = sc.api_call("auth.test")
    if api_call.get('ok'):
        print(api_call['user_id'])
    else:
        print('could not find a user named : ' + BOT_NAME)
