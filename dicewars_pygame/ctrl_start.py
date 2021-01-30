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

from . import config
from . import events
from . ctrl_view import CtrlView
from . widgets import Button, ToggleButton


class CtrlStart(CtrlView):
    def __init__(self, size, bg_color):
        super().__init__(size, bg_color)
        self._surface.fill(self._bg_color)

        self._num_seats = config.DEFAULT_NUM_PLAYERS

        w, h = size
        w_left, w_right = w - h, h

        rect = pygame.Rect(0, 0, w_left / (config.MAX_NUM_PLAYERS - 1) - 6, h)
        for num_seats in range(2, config.MAX_NUM_PLAYERS + 1):
            btn = ToggleButton(
                f'{num_seats}\nSEATS', rect,
                pygame.event.Event(events.BUTTON_NUM_SEATS, num_seats=num_seats),
                config.PLAYER_COLORS[num_seats - 1], on=num_seats <= self._num_seats
            )
            self._buttons.append(btn)
            btn.draw(self._surface)
            rect.x += rect.width + 6

        rect = pygame.Rect(w_left, 0, w_right, h / 2 - 3)
        btn = Button('SHUFFLE', rect, pygame.event.Event(events.BUTTON_SHUFFLE))
        self._buttons.append(btn)
        btn.draw(self._surface)
        rect.y = h - rect.height
        btn = Button('START', rect, pygame.event.Event(events.BUTTON_START))
        self._buttons.append(btn)
        btn.draw(self._surface)

    @property
    def num_seats(self):
        return self._num_seats

    @num_seats.setter
    def num_seats(self, num_seats):
        if num_seats < self._num_seats:
            range_ = range(num_seats - 1, self._num_seats - 1)
            on = False
        else:
            range_ = range(self._num_seats - 1, num_seats - 1)
            on = True
        for btn_idx in range_:
            self._buttons[btn_idx].set_on(on)
            self._buttons[btn_idx].draw(self._surface)
        self._num_seats = num_seats
