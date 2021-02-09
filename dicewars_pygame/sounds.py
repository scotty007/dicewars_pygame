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

from . import config


button = lambda: None
area = lambda: None
victory = lambda: None
defeat = lambda: None
supply = lambda: None
won = lambda: None
lost = lambda: None


def init():
    if not pygame.mixer:
        import logging
        logging.getLogger(__name__).warning('pygame.mixer support not available, disabling sounds')
        return
    if config.SOUND_VOLUME == 0.0:
        return

    pygame.mixer.quit()
    pygame.mixer.init(**config.SOUND_CONFIG, allowedchanges=pygame.AUDIO_ALLOW_ANY_CHANGE)

    sounds = []
    for name in ('button', 'area', 'victory', 'defeat', 'supply', 'won', 'lost'):
        sound = pygame.mixer.Sound(f'{config.RESOURCES_PATH / name}.wav')
        sound.set_volume(config.SOUND_VOLUME)
        sounds.append(sound.play)

    global button, area, victory, defeat, supply, won, lost
    button, area, victory, defeat, supply, won, lost = sounds
