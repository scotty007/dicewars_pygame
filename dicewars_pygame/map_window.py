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

from . map_area import MapArea


class MapWindow:
    def __init__(self, size):
        self._surface = pygame.Surface(size)

        self._map_pos = None
        self._map_scale = None
        self._map_areas = None

        self._dirty = False

    @property
    def surface(self):
        return self._surface

    def mouse_down(self, x, y):
        print(f'MAP: mouse down at ({x}, {y})')

    def render(self):
        if not self._dirty:
            return False

        self._dirty = False
        return True

    def init_grid(self, grid, bg_color):
        self._surface.fill(bg_color)

        map_rect = pygame.Rect((0, 0), grid.map_size).fit(self._surface.get_rect())
        self._map_pos = (map_rect.x, map_rect.y)
        self._map_scale = min(map_rect.width / grid.map_size[0], map_rect.height / grid.map_size[1])
        self._map_areas = [MapArea(grid_area, *self._map_pos, self._map_scale) for grid_area in grid.areas]

        self._dirty = True

    def init_game(self, game, player_colors):
        for area_idx, seat_idx in enumerate(game.area_seats):
            self._map_areas[area_idx].draw(self._surface, player_colors[seat_idx])
