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

from dicewars.__version__ import __version__ as dw_version
from dicewars.grid import Grid

from . __version__ import __version__
from . widgets import Text


class Welcome:
    _BG_MAP_COLOR = pygame.Color('gray')

    def __init__(self, surface):
        grid = Grid()
        rect = pygame.Rect((0, 0), grid.map_size).fit(surface.get_rect().inflate(-20, -20))

        scale = min(rect.width / grid.map_size[0], rect.height / grid.map_size[1])
        for cell in grid.cells:
            if cell.area < 0:
                points = [(rect.x + x * scale, rect.y + y * scale) for x, y in cell.border]
                pygame.draw.lines(surface, self._BG_MAP_COLOR, True, points, 1)
        for area in grid.areas:
            points = [(rect.x + x * scale, rect.y + y * scale) for x, y in area.border]
            pygame.draw.lines(surface, self._BG_MAP_COLOR, True, points, 3)

        rect.y = 0
        r = rect.move(0, -Text.SIZE_L * 2)
        Text('Welcome to', Text.SIZE_M, r).draw(surface)
        Text('DiceWars', Text.SIZE_L * 2, rect).draw(surface)
        r = rect.move(0, Text.SIZE_L * 2)
        Text('A Risk-like board game.\nConquer all areas on the map by dice rolls!', Text.SIZE_M, r).draw(surface)
        r.move_ip(0, Text.SIZE_M * 3)
        Text(f'version {__version__}', Text.SIZE_S, r).draw(surface)
        r.move_ip(0, Text.SIZE_M * 3)
        Text('(C) 2021 Thomas Schott\nhttps://github.com/scotty007/dicewars_pygame', Text.SIZE_S, r).draw(surface)
        r.move_ip(0, Text.SIZE_S * 4)
        Text(f'using pygame (v{pygame.version.ver})\nand dicewars (v{dw_version})', Text.SIZE_S, r).draw(surface)
