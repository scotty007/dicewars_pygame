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
        self._view = self._players
        self._players.init_match(match)
        self._dirty = True
