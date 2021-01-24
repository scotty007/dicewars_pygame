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

from . map_window import MapWindow
from . ctrl_window import CtrlWindow


class Engine:
    def __init__(self, surface):
        self._surface = surface
        self._surface.fill('white')

        pad = 10
        w_surf, h_surf = self._surface.get_size()
        w_win, h_ctrl = w_surf - pad * 2, 100
        self._map_rect = pygame.Rect(pad, pad, w_win, h_surf - h_ctrl - pad * 3)
        self._map_window = MapWindow(self._map_rect.size)
        self._ctrl_rect = pygame.Rect(pad, self._map_rect.bottom + pad, w_win, h_ctrl)
        self._ctrl_window = CtrlWindow(self._ctrl_rect.size)

        self._grid = None
        self._init_grid()

    def mouse_down(self, x, y):
        if self._map_rect.collidepoint(x, y):
            self._map_window.mouse_down(x - self._map_rect.x, y - self._map_rect.y)
        elif self._ctrl_rect.collidepoint(x, y):
            self._ctrl_window.mouse_down(x - self._ctrl_rect.x, y - self._ctrl_rect.y)

    def mouse_up(self, x, y):
        if self._ctrl_rect.collidepoint(x, y):
            self._ctrl_window.mouse_up(x - self._ctrl_rect.x, y - self._ctrl_rect.y)

    def mouse_move(self, x, y):
        if self._ctrl_rect.collidepoint(x, y):
            self._ctrl_window.mouse_move(x - self._ctrl_rect.x, y - self._ctrl_rect.y)

    def render(self):
        dirty = False
        if self._map_window.render():
            self._surface.blit(self._map_window.surface, self._map_rect)
            dirty = True
        if self._ctrl_window.render():
            self._surface.blit(self._ctrl_window.surface, self._ctrl_rect)
            dirty = True
        return dirty

    def _init_grid(self):
        self._grid = Grid()
        self._map_window.init_grid(self._grid)
