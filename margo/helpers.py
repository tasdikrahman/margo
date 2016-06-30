# -*- coding: utf-8 -*-
# @Author: Tasdik Rahman
# @GPLv3 License
# @http://tasdikrahman.me

"""Helper functions"""

def help(slack_client, channel):
    """Will show every possible interaction with the slack bot"""
    response = "You can ask me questions like\n"\
               "1) @isitupbot http://srmsearchengine.in/ \n"\
               "*More commands coming through later on* "\
               "You can check the source code at \nhttps://github.com/prodicus/margo \n"\
               "Happy hacking :smile:"

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def default_resp(slack_client, channel):
    """
    Default response when the bot isn't able to parse the data that
    has been to it by the user
    """
    response = "Not sure what you meant. :sweat_smile: \n"\
               "Type *@isitupbot* *help* for a list of possible commands"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)
