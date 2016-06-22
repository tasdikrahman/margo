# -*- coding: utf-8 -*-
# @Author: Tasdik Rahman
# @GPLv3 License
# @http://tasdikrahman.me

import re

# django url validation regex:
# ref: http://stackoverflow.com/a/7160778/3834059
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def url_validator(url):
    """
    checks whether the user has entered a valid url or not
    """
    if re.match(regex, url) != None:
        return True
    else:
        return False