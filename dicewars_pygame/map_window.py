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

from . config import PLAYER_COLORS
from . map_area import MapArea
from . import sounds


class MapWindow:
    _HL_BG_COLOR = pygame.Color('black')

    def __init__(self, size, bg_color):
        self._bg_color = bg_color
        self._surface = pygame.Surface(size)

        self._map_pos = None
        self._map_scale = None
        self._map_areas = None

        self._dirty = False

    def blit(self, surface, rect):
        if self._dirty:
            surface.blit(self._surface, rect)
            self._dirty = False
            return True
        return False

    def init_grid(self, grid):
        self._surface.fill(self._bg_color)
        map_rect = pygame.Rect((0, 0), grid.map_size).fit(self._surface.get_rect())
        self._map_pos = (map_rect.x, map_rect.y)
        self._map_scale = min(map_rect.width / grid.map_size[0], map_rect.height / grid.map_size[1])
        self._map_areas = [
            MapArea(grid_area, grid.cells[grid_area.center], *self._map_pos, self._map_scale)
            for grid_area in grid.areas
        ]
        self._dirty = True

    def init_game(self, game):
        for area_idx, seat_idx in enumerate(game.area_seats):
            self._map_areas[area_idx].draw(
                self._surface, PLAYER_COLORS[seat_idx], num_dice=game.area_num_dice[area_idx]
            )
        self._dirty = True

    def draw_area(self, area_idx, player_idx, num_dice=None):
        self._map_areas[area_idx].draw(self._surface, PLAYER_COLORS[player_idx], num_dice=num_dice)
        self._dirty = True

    def highlight_area(self, area_idx, player_idx):
        self._map_areas[area_idx].draw(self._surface, self._HL_BG_COLOR, bd_color=PLAYER_COLORS[player_idx])
        sounds.area()
        self._dirty = True

    def get_map_pos(self, x, y):
        return (x - self._map_pos[0]) / self._map_scale, (y - self._map_pos[1]) / self._map_scale
