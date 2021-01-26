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

from dicewars.grid import Grid
from dicewars.game import Game
from dicewars.match import Match
from dicewars.util import pick_grid_area

from . import events
from . map_window import MapWindow
from . ctrl_window import CtrlWindow


class Engine:
    _BG_COLOR = pygame.Color('white')

    def __init__(self, surface):
        self._surface = surface
        self._surface.fill(self._BG_COLOR)

        pad = 10
        w_surf, h_surf = self._surface.get_size()
        w_win, h_ctrl = w_surf - pad * 2, 100
        self._map_rect = pygame.Rect(pad, pad, w_win, h_surf - h_ctrl - pad * 3)
        self._map_window = MapWindow(self._map_rect.size, self._BG_COLOR)
        self._ctrl_rect = pygame.Rect(pad, self._map_rect.bottom + pad, w_win, h_ctrl)
        self._ctrl_window = CtrlWindow(self._ctrl_rect.size, self._BG_COLOR)

        self._grid = None
        self._game = None
        self._match = None
        self._init_grid()

    def mouse_down(self, x, y):
        if self._map_rect.collidepoint(x, y):
            map_pos = self._map_window.get_map_pos(x - self._map_rect.x, y - self._map_rect.y)
            grid_area = pick_grid_area(self._grid, *map_pos)
            print(grid_area.idx if grid_area else 'none')
        elif self._ctrl_rect.collidepoint(x, y):
            self._ctrl_window.mouse_down(x - self._ctrl_rect.x, y - self._ctrl_rect.y)

    def mouse_up(self, x, y):
        if self._ctrl_rect.collidepoint(x, y):
            self._ctrl_window.mouse_up(x - self._ctrl_rect.x, y - self._ctrl_rect.y)

    def mouse_move(self, x, y):
        self._ctrl_window.mouse_move(x - self._ctrl_rect.x, y - self._ctrl_rect.y)

    def user_event(self, event):
        if event.type == events.BUTTON_NUM_SEATS:
            self._ctrl_window.num_seats = event.num_seats
            self._init_game()
        elif event.type == events.BUTTON_SHUFFLE:
            self._init_grid()
        elif event.type == events.BUTTON_START:
            self._init_match()
        else:
            print('unhandled user event:', event)

    def render(self):
        dirty = self._map_window.blit(self._surface, self._map_rect)
        dirty |= self._ctrl_window.blit(self._surface, self._ctrl_rect)
        return dirty

    def _init_grid(self):
        self._grid = Grid()
        self._map_window.init_grid(self._grid)
        self._init_game()

    def _init_game(self):
        assert self._grid
        self._game = Game(self._grid, num_seats=self._ctrl_window.num_seats)
        self._map_window.init_game(self._game)

    def _init_match(self):
        assert self._game
        self._match = Match(self._game)
        self._ctrl_window.init_match(self._match)
