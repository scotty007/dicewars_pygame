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

from dicewars.grid import Grid
from dicewars.game import Game
from dicewars.match import Match, Attack
from dicewars.player import DefaultPlayer
from dicewars.util import pick_grid_area

from . import config
from . import events
from . map_window import MapWindow
from . ctrl_window import CtrlWindow


class Engine:

    def __init__(self, surface):
        self._surface = surface

        pad = 10
        w_surf, h_surf = self._surface.get_size()
        w_win, h_ctrl = w_surf - pad * 2, 100
        self._map_rect = pygame.Rect(pad, pad, w_win, h_surf - h_ctrl - pad * 3)
        self._map_window = MapWindow(self._map_rect.size, config.APP_BG_COLOR)
        self._ctrl_rect = pygame.Rect(pad, self._map_rect.bottom + pad, w_win, h_ctrl)
        self._ctrl_window = CtrlWindow(self._ctrl_rect.size, config.APP_BG_COLOR)

        self._grid = None
        self._game = None
        self._match = None
        self._ai_player = DefaultPlayer()
        self._timer_running = False

        self._init_grid()

    def mouse_down(self, x, y):
        if self._ctrl_rect.collidepoint(x, y):
            self._ctrl_window.mouse_down(x - self._ctrl_rect.x, y - self._ctrl_rect.y)
            return
        if self._timer_running:
            return
        if self._match and self._match.player == 0 and self._map_rect.collidepoint(x, y):
            map_pos = self._map_window.get_map_pos(x - self._map_rect.x, y - self._map_rect.y)
            grid_area = pick_grid_area(self._grid, *map_pos)
            if grid_area:
                self._set_user_area(grid_area.idx)

    def mouse_up(self, x, y):
        if self._ctrl_rect.collidepoint(x, y):
            self._ctrl_window.mouse_up(x - self._ctrl_rect.x, y - self._ctrl_rect.y)

    def mouse_move(self, x, y):
        self._ctrl_window.mouse_move(x - self._ctrl_rect.x, y - self._ctrl_rect.y)

    def user_event(self, event):
        if event.type == events.BUTTON_NUM_SEATS:
            self._ctrl_window.num_seats = event.num_seats
            self._init_game()
        elif event.type == events.BUTTON_SHUFFLE:
            self._init_grid()
        elif event.type == events.BUTTON_START:
            self._init_match()
        elif event.type == events.BUTTON_END_TURN:
            self._end_user_turn()
        elif event.type == events.BUTTON_CONTINUE:
            self._continue_match()
        elif event.type == events.BUTTON_RESTART:
            self._restart_match()
        elif event.type == events.BUTTON_REPLAY:
            self._replay_match()
        elif event.type == events.TIMER_NEXT_STEP:
            event.next_step()
        else:
            print('unhandled user event:', event)

    def render(self):
        dirty = self._map_window.blit(self._surface, self._map_rect)
        dirty |= self._ctrl_window.blit(self._surface, self._ctrl_rect)
        return dirty

    def _init_grid(self):
        self._grid = Grid()
        self._map_window.init_grid(self._grid)
        self._init_game()

    def _init_game(self):
        assert self._grid
        self._match = None
        self._game = Game(self._grid, num_seats=self._ctrl_window.num_seats)
        self._map_window.init_game(self._game)
        self._ctrl_window.show_start()

    def _init_match(self):
        assert self._game
        self._match = Match(self._game)
        self._ctrl_window.init_match(self._match)
        self._start_turn()

    def _continue_match(self):
        assert self._match and self._match.winner < 0
        self._ctrl_window.end_attack(self._match.last_attack)
        self._next_ai_action()

    def _restart_match(self):
        assert self._game
        self._map_window.init_game(self._game)
        self._init_match()

    def _start_turn(self):
        assert self._match
        self._ctrl_window.start_turn(self._match.player)
        if 0 < self._match.player:  # AI player
            self._next_ai_action()
        else:  # user player
            assert self._match.player == 0
            self._timer_running = False

    def _set_user_area(self, area_idx):
        assert self._match.player == 0
        if area_idx == self._match.from_area:  # unset from-area
            assert self._match.set_from_area(-1)
            self._map_window.draw_area(area_idx, 0)
            return
        if self._match.from_area < 0:  # (try to) set from-area
            if self._match.set_from_area(area_idx):
                self._map_window.highlight_area(area_idx, 0)
            return
        if self._match.set_to_area(area_idx):  # (try to) set to-area and attack
            self._map_window.highlight_area(area_idx, 0)
            self._attack()

    def _end_user_turn(self):
        assert self._match.player == 0
        if 0 <= self._match.from_area:  # unset from-area
            self._map_window.draw_area(self._match.from_area, 0)
        self._supply()

    def _next_ai_action(self):
        def show_from_area():
            self._map_window.highlight_area(self._match.from_area, self._match.player)
            self._start_timer(show_to_area, config.STEP_INTERVAL)

        def show_to_area():
            self._map_window.highlight_area(self._match.to_area, self._match.area_players[self._match.to_area])
            self._start_timer(self._attack, config.STEP_INTERVAL)

        attack_areas = self._ai_player.get_attack_areas(self._grid, self._match.state)
        if attack_areas:
            assert self._match.set_from_area(attack_areas[0])
            assert self._match.set_to_area(attack_areas[1])
            self._start_timer(show_from_area, config.STEP_INTERVAL)
        else:
            self._start_timer(self._supply, config.STEP_INTERVAL)

    def _attack(self):
        def show_from():
            self._ctrl_window.show_from_attack(self._match.last_attack)
            self._start_timer(show_to, config.STEP_INTERVAL)

        def show_to():
            self._ctrl_window.show_to_attack(self._match.last_attack)
            self._start_timer(end_attack, config.STEP_INTERVAL)

        def end_attack():
            la = self._match.last_attack
            self._map_window.draw_area(la.from_area, la.from_player, num_dice=la.from_area_num_dice)
            if la.victory:
                self._map_window.draw_area(la.to_area, la.from_player, num_dice=la.to_area_num_dice)
            else:
                self._map_window.draw_area(la.to_area, la.to_player)

            if 0 <= self._match.winner or (la.to_player == 0 and la.to_player_num_areas == 0):
                # match finished or user player just eliminated
                self._ctrl_window.show_end(self._match.winner)
                return
            self._ctrl_window.end_attack(la)

            if self._match.player == 0:  # user player
                self._timer_running = False
            else:  # AI player
                self._next_ai_action()

        assert self._match.attack()
        self._ctrl_window.start_attack(self._match.last_attack)
        self._start_timer(show_from, config.STEP_INTERVAL)

    def _supply(self):
        def next_supply():
            area_dice = self._ctrl_window.next_supply(self._match.last_supply)
            if area_dice:
                self._map_window.draw_area(area_dice[0], self._match.last_supply.player, area_dice[1])
                self._start_timer(next_supply, config.SUPPLY_INTERVAL)
            else:
                self._ctrl_window.end_supply(self._match.last_supply)
                self._start_turn()

        assert self._match.end_turn()
        self._ctrl_window.start_supply(self._match.last_supply)
        self._start_timer(next_supply, config.STEP_INTERVAL)

    def _replay_match(self):
        def next_step():
            nonlocal step_idx, player_idx, step_action
            step_idx += 1
            assert step_idx < self._match.num_steps
            step_action = self._match.history[step_idx]
            if isinstance(step_action, Attack):
                if player_idx != step_action.from_player:
                    player_idx = step_action.from_player
                    self._ctrl_window.start_turn(player_idx, is_replay=True)
                self._start_timer(show_from_area, config.STEP_INTERVAL)
            else:  # Supply
                if player_idx != step_action.player:
                    player_idx = step_action.player
                    self._ctrl_window.start_turn(player_idx, is_replay=True)
                self._start_timer(start_supply, config.STEP_INTERVAL)

        def show_from_area():
            self._map_window.highlight_area(step_action.from_area, step_action.from_player)
            self._start_timer(show_to_area, config.STEP_INTERVAL)

        def show_to_area():
            self._map_window.highlight_area(step_action.to_area, step_action.to_player)
            self._start_timer(start_attack, config.STEP_INTERVAL)

        def start_attack():
            self._ctrl_window.start_attack(step_action)
            self._start_timer(show_from_attack, config.STEP_INTERVAL)

        def show_from_attack():
            self._ctrl_window.show_from_attack(step_action)
            self._start_timer(show_to_attack, config.STEP_INTERVAL)

        def show_to_attack():
            self._ctrl_window.show_to_attack(step_action)
            self._start_timer(end_attack, config.STEP_INTERVAL)

        def end_attack():
            self._map_window.draw_area(
                step_action.from_area, step_action.from_player, num_dice=step_action.from_area_num_dice
            )
            if step_action.victory:
                self._map_window.draw_area(
                    step_action.to_area, step_action.from_player, num_dice=step_action.to_area_num_dice
                )
            else:
                self._map_window.draw_area(step_action.to_area, step_action.to_player)

            if step_idx < self._match.num_steps - 1:  # more actions available
                self._ctrl_window.end_attack(step_action)
                next_step()
            else:
                self._ctrl_window.show_end(self._match.winner)

        def start_supply():
            self._ctrl_window.start_supply(step_action)
            self._start_timer(next_supply, config.STEP_INTERVAL)

        def next_supply():
            area_dice = self._ctrl_window.next_supply(step_action)
            if area_dice:
                self._map_window.draw_area(area_dice[0], step_action.player, area_dice[1])
                self._start_timer(next_supply, config.SUPPLY_INTERVAL)
            else:
                self._ctrl_window.end_supply(step_action)
                next_step()  # NOTE: replay never starts after supply

        assert self._match and self._match.num_steps
        step_idx = -1
        player_idx = -1
        step_action = None
        self._map_window.init_game(self._game)
        self._ctrl_window.init_match(Match(self._game))
        next_step()

    def _start_timer(self, callback, timeout):
        pygame.time.set_timer(pygame.event.Event(events.TIMER_NEXT_STEP, next_step=callback), timeout, loops=1)
        self._timer_running = True
