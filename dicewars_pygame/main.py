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

import pygame

from dicewars.__version__ import __version__ as dicewars_version

from . __version__ import __version__
from . config import APP_SIZE, APP_BG_COLOR, parse_cli_args
from . welcome import Welcome
from . engine import Engine
from . import sounds


def main():
    print(f'dicewars_pygame {__version__} (dicewars {dicewars_version})')
    pygame.init()
    sounds.init()
    pygame.display.set_caption(f'DiceWars (pygame) v{__version__}')

    screen = pygame.display.set_mode(APP_SIZE)
    clock = pygame.time.Clock()
    engine = Engine(screen)

    screen.fill(APP_BG_COLOR)
    welcome = Welcome(screen)
    pygame.display.flip()

    running = True
    while running:
        clock.tick(60)
        force_redraw = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.WINDOWRESTORED:
                force_redraw = True
            elif welcome:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    welcome = None
                    screen.fill(APP_BG_COLOR)
                    force_redraw = True
            elif event.type == pygame.MOUSEMOTION:
                engine.mouse_move(*event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                engine.mouse_down(*event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                engine.mouse_up(*event.pos)
            elif pygame.USEREVENT <= event.type:
                engine.user_event(event)

        if (not welcome and engine.render()) or force_redraw:
            pygame.display.flip()

    pygame.quit()


def run():
    parse_cli_args()
    main()


if __name__ == '__main__':
    run()
