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

from . import events
from . ctrl_view import CtrlView
from . widgets import Box, Text, Button, EnableButton


class CtrlEnd(CtrlView):
    def __init__(self, size, bg_color):
        super().__init__(size, bg_color)
        self._surface.fill(self._bg_color)

        w, h = size

        rect = pygame.Rect(0, 0, h, h / 2 - 3)
        btn = EnableButton('CONTINUE', rect, pygame.event.Event(events.BUTTON_CONTINUE), on=False)
        self._buttons.append(btn)
        btn.draw(self._surface)
        rect.y = h - rect.height
        btn = Button('REPLAY', rect, pygame.event.Event(events.BUTTON_REPLAY))
        self._buttons.append(btn)
        btn.draw(self._surface)

        rect.right = w
        btn = Button('RESTART', rect, pygame.event.Event(events.BUTTON_RESTART))
        self._buttons.append(btn)
        btn.draw(self._surface)
        rect.y = 0
        btn = Button('SHUFFLE', rect, pygame.event.Event(events.BUTTON_SHUFFLE))
        self._buttons.append(btn)
        btn.draw(self._surface)

        self._box = Box((rect.width + 6, 0, w - (rect.width + 6) * 2, h))
        self._won_text = Text('CONGRATS, YOU WON!', Text.SIZE_L, self._box.rect)
        self._lost_text = Text('YOU LOST, TRY AGAIN?', Text.SIZE_L, self._box.rect)

    def show(self, winner_idx):
        btn = self._buttons[0]
        btn.set_on(winner_idx < 0)
        btn.draw(self._surface)

        self._box.draw(self._surface)
        if winner_idx == 0:
            self._won_text.draw(self._surface)
        else:
            self._lost_text.draw(self._surface)
