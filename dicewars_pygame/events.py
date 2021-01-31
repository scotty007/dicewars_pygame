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

from pygame.event import custom_type


BUTTON_NUM_SEATS = custom_type()  # attributes: num_seats (int)
BUTTON_SHUFFLE = custom_type()
BUTTON_START = custom_type()
BUTTON_END_TURN = custom_type()
BUTTON_CONTINUE = custom_type()
BUTTON_RESTART = custom_type()
BUTTON_REPLAY = custom_type()

TIMER_NEXT_STEP = custom_type()  # attributes: next_step (callable)
