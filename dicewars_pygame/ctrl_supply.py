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

from dicewars.match import Match

from . import config
from . ctrl_view import CtrlView
from . widgets import Box


class CtrlSupply(CtrlView):
    _DICE_BD_COLOR = pygame.Color('black')

    def __init__(self, size, bg_color):
        super().__init__(size, bg_color)
        self._surface.fill(self._bg_color)

        self._box = Box(self._surface.get_rect())

        size = self._box.rect.height // 4  # for box offsets
        size_ = size - 2  # for box drawing w/ gap
        dice_per_row = int(self._box.rect.width / size) - 1
        x, y = (self._box.rect.width - size * dice_per_row) * 0.5 + 1, size * 0.5 + 1
        rects0 = []  # 1st row
        rects1 = []  # 2nd row
        rects2 = []  # 3rd row
        for _ in range(dice_per_row):
            rects0.append(pygame.Rect(x, y, size_, size_))
            rects1.append(pygame.Rect(x, y + size, size_, size_))
            rects2.append(pygame.Rect(x, y + size + size, size_, size_))
            x += size
        self._dice_rects = rects0 + rects1 + rects2
        assert Match.PLAYER_MAX_NUM_STOCK <= len(self._dice_rects)

    def init(self, player_idx, num_dice):
        color = config.PLAYER_COLORS[player_idx]
        self._box.draw(self._surface, bd_color=color)

        for rect in self._dice_rects[:num_dice]:
            pygame.draw.rect(self._surface, color, rect, border_radius=5)
            pygame.draw.rect(self._surface, self._DICE_BD_COLOR, rect, width=2, border_radius=5)

    def hide(self, dice_idx):
        pygame.draw.rect(self._surface, self._bg_color, self._dice_rects[dice_idx])
