# -*- coding: utf-8 -*-
# @Author: Tasdik Rahman
# @GPLv3 License
# @http://tasdikrahman.me

"""Stiches everything together to make margo work"""

import time

from slackclient import SlackClient

from utils import handle_command, parse_slack_output
from constants import SLACK_TOKEN, READ_WEBSOCKET_DELAY


slack_client = SlackClient(SLACK_TOKEN)


if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            url, channel = parse_slack_output(slack_client.rtm_read())
            if url and channel:
                handle_command(url, slack_client, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
