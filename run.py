# -*- coding: utf-8 -*-
# @Author: Tasdik Rahman
# @GPLv3 License
# @http://tasdikrahman.me

import argparse

from margo.core import runner
from scripts.print_bot_id import bot_id

FUCNTION_MAP = {
    'start': runner,
    'bot_id': bot_id
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Margo: An opiniated slack bot for SRMSE's slack channel")
    parser.add_argument('command', choices=FUCNTION_MAP.keys())
    args = parser.parse_args()

    func = FUCNTION_MAP[args.command]
    func()
