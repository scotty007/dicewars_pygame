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
from . widgets import Box, Text, EnableButton


class CtrlPlayers(CtrlView):
    def __init__(self, size, bg_color):
        super().__init__(size, bg_color)

        self._player_idx = -1

        w, h = size
        w_left, w_right = w - h, h

        rect = pygame.Rect(0, 0, 0, h)
        self._player_states = [
            _PlayerState(config.PLAYER_COLORS[player_idx], rect)
            for player_idx in range(config.MAX_NUM_PLAYERS)
        ]

        rect = pygame.Rect(w_left, 0, w_right, h)
        self._buttons.append(EnableButton('END\nTURN', rect, pygame.event.Event(events.BUTTON_END_TURN)))

    def init_match(self, match):
        self._surface.fill(self._bg_color)
        self._player_idx = match.player
        btn = self._buttons[0]
        x, w = 0, btn.rect.left / match.game.num_seats - 6
        for player_idx in match.game.seat_order:
            self._player_states[player_idx].init(
                self._surface, x, w, player_idx == self._player_idx, match.player_max_size[player_idx]
            )
            x += w + 6
        btn.set_on(self._player_idx == 0)
        btn.draw(self._surface)

    def set_current(self, player_idx, is_replay):
        assert 0 <= self._player_idx
        assert 0 <= player_idx
        self._player_states[self._player_idx].set_current(self._surface, False)
        self._player_states[player_idx].set_current(self._surface, True)
        if self._player_idx == 0 or player_idx == 0:
            self._buttons[0].set_on(player_idx == 0 and not is_replay)
            self._buttons[0].draw(self._surface)
        self._player_idx = player_idx

    def update(self, player_idx, max_size=None, num_stock=None):
        self._player_states[player_idx].update(self._surface, max_size, num_stock)


class _PlayerState:
    _SIZE_DY = -Text.SIZE_L * 0.25
    _STOCK_DY = Text.SIZE_S * 1.25
    _STOCK_0_COLOR = pygame.Color('gray')

    def __init__(self, color, rect):
        self._box = Box(rect, bd_color=color)
        self._size_text = None
        self._stock_text = None

    def init(self, surface, pos_x, width, current, max_size):
        self._box.rect.x = pos_x
        self._box.rect.width = width
        self._size_text = Text(str(max_size), Text.SIZE_L, self._box.rect.move(0, self._SIZE_DY))
        self._stock_text = Text('0', Text.SIZE_S, self._box.rect.move(0, self._STOCK_DY), color=self._STOCK_0_COLOR)
        self.set_current(surface, current)

    def set_current(self, surface, current):
        assert self._size_text  # not dead
        self._box.bg_color = self._box.bd_color if current else Box.DEFAULT_BG_COLOR
        self._box.draw(surface)
        self._size_text.draw(surface)
        self._stock_text.draw(surface)

    def update(self, surface, max_size=None, num_stock=None):
        assert self._size_text  # not dead
        self._size_text.clear(surface, self._box.bg_color)
        self._stock_text.clear(surface, self._box.bg_color)

        if max_size is not None:
            if max_size == 0:  # dead
                self._size_text = None
                self._stock_text = None
                return
            self._size_text = Text(str(max_size), Text.SIZE_L, self._box.rect.move(0, self._SIZE_DY))
        if num_stock is not None:
            self._stock_text = Text(
                str(num_stock), Text.SIZE_S, self._box.rect.move(0, self._STOCK_DY),
                color=self._STOCK_0_COLOR if num_stock == 0 else Text.DEFAULT_COLOR
            )

        self._size_text.draw(surface)
        self._stock_text.draw(surface)
