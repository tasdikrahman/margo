# -*- coding: utf-8 -*-
# @Author: Tasdik Rahman
# @GPLv3 License
# @http://tasdikrahman.me

"""General Utilities"""

import re
from urllib.parse import urlparse

import requests

from constants import BASE_URL, RESULT_FORMAT, AT_BOT
from helpers import help, default_resp

# django url validation regex:
# ref: http://stackoverflow.com/a/7160778/3834059
regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def url_validator(url):
    """
    checks whether the user has entered a valid url or not
    """
    if re.match(regex, url) != None:
        return True
    else:
        return False


def query_url(passed_url, slack_client, channel):
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


def return_response(json_resp, slack_client, channel):
    """
    Calls the method query_url() to get the JSON content and then parses
    it to return whether the website is down or not
    """
    if isinstance(json_resp, int):
        response = "Ironically. It looks like we had a {0} error ".format(
            json_resp)
    else:
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


def handle_command(url, slack_client, channel):
    """
    Receives commands directed at the bot and determines if they
    are valid commands. If so, then acts on the commands. If not,
    returns back what it needs for clarification.
    """
    if url_validator(url):  # check if it's a valid url
        # remove the scheme from it i.e. remove https://, http:// etc
        url = urlparse(url).netloc
        json_resp = query_url(url, channel, slack_client)
        return_response(json_resp, slack_client, channel)

    elif "help" in url:
        help(slack_client, channel)

    else:
        default_resp(slack_client, channel)


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
