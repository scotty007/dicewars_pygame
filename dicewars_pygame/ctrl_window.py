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

from . ctrl_start import CtrlStart
from . ctrl_players import CtrlPlayers


class CtrlWindow:
    def __init__(self, size, bg_color):
        self._start = CtrlStart(size, bg_color)
        self._players = CtrlPlayers(size, bg_color)
        self._attack = _CtrlDummy(size, bg_color)
        self._supply = _CtrlDummy(size, bg_color)
        self._match = None

        self._view = self._start
        self._dirty = True

    @property
    def num_seats(self):
        return self._start.num_seats

    @num_seats.setter
    def num_seats(self, num_seats):
        if self._start.num_seats != num_seats:
            self._start.num_seats = num_seats
            self._dirty = True

    def mouse_down(self, x, y):
        for btn in self._view.buttons:
            if btn.mouse_down(x, y):
                self._view.draw_button(btn)
                self._dirty = True
                break

    def mouse_up(self, x, y):
        for btn in self._view.buttons:
            if btn.mouse_up(x, y):
                self._view.draw_button(btn)
                self._dirty = True
                break

    def mouse_move(self, x, y):
        for btn in self._view.buttons:
            if btn.mouse_move(x, y):
                self._view.draw_button(btn)
                self._dirty = True
                break

    def blit(self, surface, rect):
        if self._dirty:
            surface.blit(self._view.surface, rect)
            self._dirty = False
            return True
        return False

    def init_match(self, match):
        self._match = match
        self._view = self._players
        self._players.init_match(self._match)
        self._dirty = True

    def start_turn(self):
        self._players.set_current(self._match.player)
        self._dirty = True

    def start_attack(self):
        self._view = self._attack
        self._attack.show('start attack')
        self._dirty = True

    def show_from_attack(self):
        self._attack.show('show FROM attack')
        self._dirty = True

    def show_to_attack(self):
        self._attack.show('show TO attack')
        self._dirty = True

    def end_attack(self):
        self._view = self._players
        if self._match.last_attack.victory:
            from_player_idx = self._match.last_attack.from_player
            self._players.update(from_player_idx, max_size=self._match.player_max_size[from_player_idx])
            to_player_idx = self._match.last_attack.to_player
            self._players.update(to_player_idx, max_size=self._match.player_max_size[to_player_idx])
        self._dirty = True

    def start_supply(self):
        self._view = self._supply
        self._supply.show('start supply')
        self._dirty = True

    def show_supply(self):
        self._supply.show('show supply')
        self._dirty = True

    def end_supply(self):
        self._view = self._players
        player_idx = self._match.last_supply.player
        self._players.update(player_idx, num_stock=self._match.player_num_stock[player_idx])
        self._dirty = True


import pygame
from . widgets import Text
class _CtrlDummy:
    def __init__(self, size, bg_color):
        self._bg_color = bg_color
        self._surface = pygame.Surface(size)

    @property
    def surface(self):
        return self._surface

    @property
    def buttons(self):
        return ()

    def show(self, msg):
        self._surface.fill(self._bg_color)
        Text(f'TODO: {msg}', Text.SIZE_L, self._surface.get_rect()).draw(self._surface)
