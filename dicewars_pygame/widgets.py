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

from . config import FONT_FILE_PATH
from . import sounds


if not pygame.font:
    raise SystemError('pygame.font support not available')


class Text:
    SIZE_S = 20
    SIZE_M = 24
    SIZE_L = 42

    DEFAULT_COLOR = pygame.Color('black')

    _FONTS = {}

    @classmethod
    def _get_font(cls, size):
        font = cls._FONTS.get(size)
        if not font:
            font = pygame.font.Font(FONT_FILE_PATH, size)
            cls._FONTS[size] = font
        return font

    def __init__(self, text, size, rect, color=DEFAULT_COLOR):
        font = self._get_font(size)
        lines = text.split('\n')
        self._surface1 = font.render(lines[0], True, color)
        if len(lines) == 2:
            self._surface2 = font.render(lines[1], True, color)
            self._rect1 = self._surface1.get_rect(centerx=rect.centerx, bottom=rect.centery)
            self._rect2 = self._surface2.get_rect(centerx=rect.centerx, top=rect.centery)
        else:
            assert len(lines) == 1
            self._surface2 = None
            self._rect1 = self._surface1.get_rect(center=rect.center)

    def draw(self, surface):
        surface.blit(self._surface1, self._rect1)
        if self._surface2:
            surface.blit(self._surface2, self._rect2)

    def clear(self, surface, bg_color):
        pygame.draw.rect(surface, bg_color, self._rect1.union(self._rect2) if self._surface2 else self._rect1)


class Box:
    BD_WIDTH = 5
    DEFAULT_BG_COLOR = pygame.Color('white')
    DEFAULT_BD_COLOR = pygame.Color('black')

    def __init__(self, rect, bg_color=DEFAULT_BG_COLOR, bd_color=DEFAULT_BD_COLOR):
        self.rect = pygame.Rect(rect)
        self.bg_color = bg_color
        self.bd_color = bd_color

    def draw(self, surface, bg_color=None, bd_color=None):
        pygame.draw.rect(surface, bg_color if bg_color else self.bg_color, self.rect, border_radius=20)
        pygame.draw.rect(
            surface, bd_color if bd_color else self.bd_color, self.rect, width=self.BD_WIDTH, border_radius=20
        )


class Button:
    DOWN_FG_COLOR = pygame.Color('white')
    DOWN_BG_COLOR = Box.DEFAULT_BD_COLOR

    def __init__(self, text, rect, event):
        self._box = Box(rect)
        self._up_text = Text(text, Text.SIZE_S, rect)
        self._down_text = Text(text, Text.SIZE_S, rect, color=self.DOWN_FG_COLOR)
        self._event = event
        self._down = False

    @property
    def rect(self):
        return self._box.rect

    def draw(self, surface):
        if self._down:
            self._box.draw(surface, bg_color=self.DOWN_BG_COLOR)
            self._down_text.draw(surface)
        else:
            self._box.draw(surface)
            self._up_text.draw(surface)

    def mouse_down(self, x, y):
        assert not self._down
        if not self._box.rect.collidepoint(x, y):
            return False
        self._down = True
        return True

    def mouse_up(self, x, y):
        if self._box.rect.collidepoint(x, y) and self._down:
            self._down = False
            pygame.event.post(self._event)  # clicked
            sounds.button()
            return True
        assert not self._down
        return False

    def mouse_move(self, x, y):
        if self._box.rect.collidepoint(x, y):
            return False
        if self._down:
            self._down = False
            return True
        return False


class ToggleButton(Button):
    def __init__(self, text, rect, event, on_color, on=False):
        super().__init__(text, rect, event)
        self._on_color = on_color
        self.set_on(on)

    def set_on(self, on):
        self._box.bg_color = self._on_color if on else Box.DEFAULT_BG_COLOR


class EnableButton(Button):
    OFF_FG_COLOR = pygame.Color('gray')
    OFF_BD_COLOR = OFF_FG_COLOR

    def __init__(self, text, rect, event, on=True):
        super().__init__(text, rect, event)
        self._off_text = Text(text, Text.SIZE_S, rect, color=self.OFF_FG_COLOR)
        self._on = on

    def draw(self, surface):
        if self._on:
            super().draw(surface)
        else:
            self._box.draw(surface, bd_color=self.OFF_BD_COLOR)
            self._off_text.draw(surface)

    def mouse_down(self, x, y):
        return self._on and super().mouse_down(x, y)

    def mouse_up(self, x, y):
        return self._on and super().mouse_up(x, y)

    def mouse_move(self, x, y):
        return self._on and super().mouse_move(x, y)

    def set_on(self, on):
        self._on = on
        self._down = False
