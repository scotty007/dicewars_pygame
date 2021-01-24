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


class MapArea:
    _BORDER_COLOR = pygame.Color(0, 0, 0)

    def __init__(self, grid_area, surface, map_x0, map_y0, map_scale):
        self._points = [(map_x0 + x * map_scale, map_y0 + y * map_scale) for x, y in grid_area.border]
        pygame.draw.polygon(surface, (127, 127, 127), self._points)
        pygame.draw.lines(surface, self._BORDER_COLOR, True, self._points, 3)
