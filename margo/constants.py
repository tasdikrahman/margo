# -*- coding: utf-8 -*-
# @Author: Tasdik Rahman
# @GPLv3 License
# @http://tasdikrahman.me


import os
READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose

file_path = os.path.abspath(__file__)
par_dir = file_path.split('margo/constants.py')[0]
settings_file = os.path.join(par_dir, 'settings.ini')

"""check whether the file 'settings.ini' exists or not"""
if os.path.isfile(settings_file):
    import configparser
    config = configparser.ConfigParser()
    config.read(settings_file)

    SLACK_TOKEN = config.get('slack', 'SLACK_BOT_TOKEN')
    BASE_URL = config.get('isitup', 'BASE_URL')
    RESULT_FORMAT = config.get('isitup', 'RESULT_FORMAT')
    BOT_ID = config.get('slack', 'BOT_ID')
else:
    # config will be specified in the HEROKU environment
    SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
    BASE_URL = os.environ.get('BASE_URL')
    RESULT_FORMAT = os.environ.get('RESULT_FORMAT')
    BOT_ID = os.environ.get('BOT_ID')


AT_BOT = "<@" + BOT_ID + ">:"