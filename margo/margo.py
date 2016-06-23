# -*- coding: utf-8 -*-
# @Author: Tasdik Rahman
# @GPLv3 License
# @http://tasdikrahman.me

import json
import time
from urllib.parse import urlparse

from slackclient import SlackClient
import requests

from utils import url_validator
from constants import (SLACK_TOKEN, BASE_URL, RESULT_FORMAT, BOT_ID,
                       AT_BOT, READ_WEBSOCKET_DELAY)

slack_client = SlackClient(SLACK_TOKEN)


def help():
    """Will show every possible interaction with the slack bot"""
    response = "You can ask me questions like\n"\
               "1) @isitupbot http://srmsearchengine.in/ \n"\
               "*More commands coming through later on* "\
               "You can check the source code at \nhttps://github.com/prodicus/margo \n"\
               "Happy hacking :smile:"

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def default_resp():
    """
    Default response when the bot isn't able to parse the data that
    has been to it by the user
    """
    response = "Not sure what you meant. :sweat_smile: \n"\
               "Type *@isitupbot* *help* for a list of possible commands"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def query_url(passed_url, channel):
    """
    Makes the query for the website to know whether it is up or not
    and returns the response which is JSON compatible

    :returns: The JSON response from isitup.org
    """
    url = "{0}{1}.{2}".format(
        BASE_URL,
        passed_url,
        RESULT_FORMAT
    )
    # Eg: https://isitup.org/srmsearchengine.in.json

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        return response.json()
    except requests.exceptions.HTTPError as e:
        return response.status_code
        response = "Looks like you had a {0} error".format(e)
        slack_client.api_call("chat.postMessage", channel=channel,
                              text=response, as_user=True)


def return_reponse(json_resp, channel):
    """
    Calls the method query_url() to get the JSON content and then parses
    it to return whether the website is down or not
    """
    if isinstance(json_resp, int):
        response = "Ironically. It looks like we had a {0} error ".format(
            json_resp)
    else:
        # json_resp = json.loads(json.dumps(json_resp))
        if json_resp['status_code'] == 1:
            response = ":thumbsup: The domain: {0} is up and working\nLatency : {1}".format(
                json_resp['domain'],
                json_resp['response_time']
            )

        if json_resp['status_code'] == 2:
            response = ":disappointed: The domain: {0} is not working".format(
                json_resp['domain'],
            )

        if json_resp['status_code'] == 3:
            response = ":interrobang: The domain: {0} entered is not a valid one!".format(
                json_resp['domain'],
            )

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                url = output['text'].split(AT_BOT)[1].strip().lower()
                # clean the url
                url = url.replace('<', '').replace('>', '')
                channel = output['channel']
                return url, channel
    return None, None


def handle_command(url, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    if url_validator(url):  # check if it's a valid url
        # remove the scheme from it i.e. remove https://, http:// etc
        url = urlparse(url).netloc
        json_resp = query_url(url, channel)
        return_reponse(json_resp, channel)

    elif "help" in url:
        help()

    else:
        default_resp()


if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            url, channel = parse_slack_output(slack_client.rtm_read())
            if url and channel:
                handle_command(url, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
