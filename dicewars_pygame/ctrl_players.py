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
from . widgets import Box, Text, EnableButton


class CtrlPlayers:
    def __init__(self, size, bg_color):
        self._bg_color = bg_color
        self._surface = pygame.Surface(size)

        w, h = size
        w_left, w_right = w - h, h

        rect = pygame.Rect(0, 0, 0, h)
        self._player_states = [
            _PlayerState(config.PLAYER_COLORS[player_idx], rect)
            for player_idx in range(config.MAX_NUM_PLAYERS)
        ]

        rect = pygame.Rect(w_left, 0, w_right, h)
        self._buttons = [EnableButton('END\nTURN', rect, pygame.event.Event(events.BUTTON_END_TURN))]

    @property
    def surface(self):
        return self._surface

    @property
    def buttons(self):
        return self._buttons

    def draw_button(self, button):
        button.draw(self._surface)

    def init_match(self, match):
        self._surface.fill(self._bg_color)
        btn = self._buttons[0]
        x, w = 0, btn.rect.left / match.game.num_seats - 6
        for seat_idx, player_idx in enumerate(match.game.seat_order):
            self._player_states[player_idx].init(self._surface, x, w, match.player_max_size[player_idx])
            x += w + 6
        btn.set_on(match.player == 0)
        btn.draw(self._surface)


class _PlayerState:
    def __init__(self, color, rect):
        self._box = Box(rect, bd_color=color)
        self._size_text = None
        self._stock_text = None

    def init(self, surface, pos_x, width, dwp_max_size):
        self._box.rect.x = pos_x
        self._box.rect.width = width
        self._box.draw(surface)

        self._size_text = Text(str(dwp_max_size), Text.SIZE_L, self._box.rect.move(0, -Text.SIZE_L * 0.25))
        self._size_text.draw(surface)
        self._stock_text = Text('0', Text.SIZE_S, self._box.rect.move(0, Text.SIZE_S * 1.25))
        self._stock_text.draw(surface)
