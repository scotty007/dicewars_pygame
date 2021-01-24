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


class MapWindow:
    def __init__(self, size):
        self._surface = pygame.Surface(size)

        self._surface.fill((255, 255, 255))
        self._dirty = True

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
