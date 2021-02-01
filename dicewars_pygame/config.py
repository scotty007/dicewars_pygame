#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2021 Thomas Schott <scotty@c-base.org>
#
# This file is part of dicewars_pygame.
#
# dicewars_pygame is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# dicewars_pygame is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with dicewars_pygame.  If not, see <http://www.gnu.org/licenses/>.

from pathlib import Path
from argparse import ArgumentParser

from pygame import Color
from dicewars.game import Game


APP_SIZE = (800, 800)

PLAYER_COLORS = [
    Color(color)
    for color in ('#B37FFE', '#B3FF01', '#009302', '#FF7FFE', '#FF7F01', '#B3FFFE', '#FFFF01', '#FF5858')
]

MAX_NUM_PLAYERS = len(PLAYER_COLORS)
DEFAULT_NUM_PLAYERS = Game.DEFAULT_NUM_SEATS

DEFAULT_STEP_INTERVAL_BASE = 5
STEP_INTERVAL = DEFAULT_STEP_INTERVAL_BASE * 100  # [ms]
SUPPLY_INTERVAL = DEFAULT_STEP_INTERVAL_BASE * 10  # [ms]

RESOURCES_PATH = Path(__file__).absolute().parent / 'resources'
FONT_FILE_PATH = RESOURCES_PATH / 'Anton-Regular.ttf'


def parse_cli_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--interval', type=int,
        help=f'attack/supply step interval (min=1, default={DEFAULT_STEP_INTERVAL_BASE})'
    )
    args = parser.parse_args()

    if args.interval is not None:
        global STEP_INTERVAL, SUPPLY_INTERVAL
        interval_base = max(1, args.interval)
        STEP_INTERVAL = interval_base * 100
        SUPPLY_INTERVAL = interval_base * 10
