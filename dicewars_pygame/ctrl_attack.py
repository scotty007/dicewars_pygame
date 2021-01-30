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
from . widgets import Box, Text


class CtrlAttack(CtrlView):
    def __init__(self, size, bg_color):
        super().__init__(size, bg_color)

        rect = self._surface.get_rect()
        w_sum, h, dx = 80, rect.height, 10

        self._from_sum_box = Box((rect.centerx - w_sum - dx, 0, w_sum, h))
        w_val = self._from_sum_box.rect.left + Box.BD_WIDTH
        self._from_val_box = Box((0, 0, w_val, h))
        self._to_sum_box = Box((rect.centerx + dx, 0, w_sum, h))
        self._to_val_box = Box((self._to_sum_box.rect.right - Box.BD_WIDTH, 0, w_val, h))

        w_val /= (Match.AREA_MAX_NUM_DICE + 1)
        x = w_val * 0.5
        self._from_val_rects = []
        self._to_val_rects = []
        for _ in range(Match.AREA_MAX_NUM_DICE):
            self._from_val_rects.append(pygame.Rect(self._from_val_box.rect.right - w_val - x, 0, w_val, h))
            self._to_val_rects.append(pygame.Rect(self._to_val_box.rect.left + x, 0, w_val, h))
            x += w_val

        self._from_sum_text = None

    def init(self, from_player_idx, to_player_idx):
        self._surface.fill(self._bg_color)

        self._from_sum_box.bg_color = Box.DEFAULT_BG_COLOR
        self._from_sum_box.bd_color = config.PLAYER_COLORS[from_player_idx]
        self._from_val_box.bd_color = self._from_sum_box.bd_color
        self._from_sum_box.draw(self._surface)
        self._from_val_box.draw(self._surface)

        self._to_sum_box.bg_color = Box.DEFAULT_BG_COLOR
        self._to_sum_box.bd_color = config.PLAYER_COLORS[to_player_idx]
        self._to_val_box.bd_color = self._to_sum_box.bd_color
        self._to_sum_box.draw(self._surface)
        self._to_val_box.draw(self._surface)

    def show_from(self, dice, sum_dice):
        for dice_idx, dice_val in enumerate(dice):
            Text(str(dice_val), Text.SIZE_M, self._from_val_rects[dice_idx]).draw(self._surface)

        self._from_sum_text = Text(str(sum_dice), Text.SIZE_L, self._from_sum_box.rect)
        self._from_sum_text.draw(self._surface)

    def show_to(self, dice, sum_dice, victory):
        for dice_idx, dice_val in enumerate(dice):
            Text(str(dice_val), Text.SIZE_M, self._to_val_rects[dice_idx]).draw(self._surface)

        if victory:
            self._from_sum_box.bg_color = self._from_sum_box.bd_color
            self._from_sum_box.draw(self._surface)
            self._from_sum_text.draw(self._surface)
        else:
            self._to_sum_box.bg_color = self._to_sum_box.bd_color
            self._to_sum_box.draw(self._surface)
        Text(str(sum_dice), Text.SIZE_L, self._to_sum_box.rect).draw(self._surface)
        self._from_sum_text = None
