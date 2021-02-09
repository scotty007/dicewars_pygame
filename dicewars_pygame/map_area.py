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

from . widgets import Text


class MapArea:
    _BD_COLOR = pygame.Color('black')
    _TEXT_BASE_SIZE = 10

    def __init__(self, grid_area, grid_center_cell, map_x0, map_y0, map_scale):
        self._points = [(map_x0 + x * map_scale, map_y0 + y * map_scale) for x, y in grid_area.border]
        bbox = [(map_x0 + x * map_scale, map_y0 + y * map_scale) for x, y in grid_center_cell.bbox]
        self._dice_rect = pygame.Rect(*bbox[0], bbox[1][0] - bbox[0][0], bbox[1][1] - bbox[0][1])
        self._num_dice = None

    def draw(self, surface, bg_color, bd_color=_BD_COLOR, num_dice=None):
        pygame.draw.polygon(surface, bg_color, self._points)
        pygame.draw.lines(surface, bd_color, True, self._points, 3)
        if num_dice is not None:
            self._num_dice = num_dice
        assert self._num_dice is not None
        Text(
            str(self._num_dice), self._TEXT_BASE_SIZE + self._num_dice * 2, self._dice_rect, color=bd_color
        ).draw(surface)
