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
APP_BG_COLOR = Color('white')

PLAYER_COLORS = [
    Color(color)
    for color in ('#B37FFE', '#B3FF01', '#009302', '#FF7FFE', '#FF7F01', '#B3FFFE', '#FFFF01', '#FF5858')
]
MAX_NUM_PLAYERS = len(PLAYER_COLORS)
DEFAULT_NUM_PLAYERS = Game.DEFAULT_NUM_SEATS

DEFAULT_STEP_INTERVAL_BASE = 5
STEP_INTERVAL = DEFAULT_STEP_INTERVAL_BASE * 100  # [ms]
SUPPLY_INTERVAL = DEFAULT_STEP_INTERVAL_BASE * 10  # [ms]

DEFAULT_SOUND_VOLUME = 1.0
SOUND_VOLUME = DEFAULT_SOUND_VOLUME
SOUND_CONFIG = {'frequency': 44100, 'size': -16, 'channels': 1}

RESOURCES_PATH = Path(__file__).absolute().parent / 'resources'
FONT_FILE_PATH = RESOURCES_PATH / 'Anton-Regular.ttf'


def parse_cli_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--interval', type=int,
        help=f'attack/supply step interval (min=1, default={DEFAULT_STEP_INTERVAL_BASE})'
    )
    parser.add_argument(
        '-v', '--volume', type=float,
        help=f'sound effects volume (range=[0.0..1.0], default={DEFAULT_SOUND_VOLUME})'
    )
    args = parser.parse_args()

    if args.interval is not None:
        global STEP_INTERVAL, SUPPLY_INTERVAL
        interval_base = max(1, args.interval)
        STEP_INTERVAL = interval_base * 100
        SUPPLY_INTERVAL = interval_base * 10

    if args.volume is not None:
        global SOUND_VOLUME
        SOUND_VOLUME = (max(0.0, min(1.0, args.volume)))
