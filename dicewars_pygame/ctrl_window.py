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

from . ctrl_start import CtrlStart
from . ctrl_players import CtrlPlayers
from . ctrl_attack import CtrlAttack
from . ctrl_supply import CtrlSupply
from . ctrl_end import CtrlEnd
from . import sounds


class CtrlWindow:
    def __init__(self, size, bg_color):
        self._start = CtrlStart(size, bg_color)
        self._players = CtrlPlayers(size, bg_color)
        self._attack = CtrlAttack(size, bg_color)
        self._supply = CtrlSupply(size, bg_color)
        self._end = CtrlEnd(size, bg_color)
        self._supplies = []

        self._view = self._start
        self._dirty = True

    @property
    def num_seats(self):
        return self._start.num_seats

    @num_seats.setter
    def num_seats(self, num_seats):
        if self._start.num_seats != num_seats:
            self._start.num_seats = num_seats
            self._dirty = True

    def mouse_down(self, x, y):
        for btn in self._view.buttons:
            if btn.mouse_down(x, y):
                self._view.draw_button(btn)
                self._dirty = True
                break

    def mouse_up(self, x, y):
        for btn in self._view.buttons:
            if btn.mouse_up(x, y):
                self._view.draw_button(btn)
                self._dirty = True
                break

    def mouse_move(self, x, y):
        for btn in self._view.buttons:
            if btn.mouse_move(x, y):
                self._view.draw_button(btn)
                self._dirty = True
                break

    def blit(self, surface, rect):
        if self._dirty:
            surface.blit(self._view.surface, rect)
            self._dirty = False
            return True
        return False

    def show_start(self):
        if self._view is not self._start:
            self._view = self._start
            self._dirty = True

    def init_match(self, match):
        self._view = self._players
        self._players.init_match(match)
        self._dirty = True

    def start_turn(self, player_idx, is_replay=False):
        self._players.set_current(player_idx, is_replay)
        self._dirty = True

    def start_attack(self, attack):
        self._view = self._attack
        self._attack.init(attack.from_player, attack.to_player)
        self._dirty = True

    def show_from_attack(self, attack):
        self._attack.show_from(attack.from_dice, attack.from_sum_dice)
        self._dirty = True

    def show_to_attack(self, attack):
        self._attack.show_to(attack.to_dice, attack.to_sum_dice, attack.victory)
        if attack.victory:
            sounds.victory()
        else:
            sounds.defeat()
        self._dirty = True

    def end_attack(self, attack):
        self._view = self._players
        if attack.victory:
            self._players.update(attack.from_player, max_size=attack.from_player_max_size)
            self._players.update(attack.to_player, max_size=attack.to_player_max_size)
        self._dirty = True

    def start_supply(self, supply):
        assert not self._supplies
        self._view = self._supply
        for i, area_idx in enumerate(supply.areas):
            num_dice = supply.area_num_dice[i] - supply.dice[i] + 1
            self._supplies.extend((area_idx, num_dice + j) for j in range(supply.dice[i]))
        self._supplies.reverse()
        self._supply.init(supply.player, supply.sum_dice + supply.player_num_stock)
        self._dirty = True

    def next_supply(self, supply):
        if self._supplies:
            area_dice = self._supplies.pop()
            self._supply.hide(supply.player_num_stock + len(self._supplies))
            sounds.supply()
            self._dirty = True
            return area_dice
        return None

    def end_supply(self, supply):
        self._view = self._players
        self._players.update(supply.player, num_stock=supply.player_num_stock)
        self._dirty = True

    def show_end(self, winner_idx):
        self._view = self._end
        self._end.show(winner_idx)
        if winner_idx == 0:
            sounds.won()
        else:
            sounds.lost()
        self._dirty = True
