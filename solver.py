#!/usr/bin/python3
import pygame, time
from copy import deepcopy

from grid_utils import *

class Solver:
    def __init__(self, lvl):
        self.lvl = lvl

    def is_blocked(self, possible_pos):
        blocked = False
        for y in range(self.lvl.height):
            for x in range(self.lvl.width):
                if len(self.lvl.grid[y]) > x:
                    if self.lvl.grid[y][x] == "$":
                        if not (x, y) in possible_pos:
                            blocked = True
                        else:
                            ok = False
                            for t in self.lvl.targets_pos:
                                if t[0] == x and t[1] == y:
                                    ok = True
                                    break
                            if not ok: # not on a target
                                #check if two cases are next to a wall
                                if self.lvl.grid[y][x+1] == "$":
                                    blocked = (self.lvl.grid[y+1][x] == "#" and self.lvl.grid[y+1][x+1] == "#") or (self.lvl.grid[y-1][x] == "#" and self.lvl.grid[y-1][x+1] == "#")
                                elif self.lvl.grid[y][x-1] == "$":
                                    blocked = (self.lvl.grid[y+1][x] == "#" and self.lvl.grid[y+1][x-1] == "#") or (self.lvl.grid[y-1][x] == "#" and self.lvl.grid[y-1][x-1] == "#")
                                elif self.lvl.grid[y-1][x] == "$":
                                    blocked = (self.lvl.grid[y][x-1] == "#" and self.lvl.grid[y-1][x-1] == "#") or (self.lvl.grid[y][x+1] == "#" and self.lvl.grid[y-1][x+1] == "#")
                                elif self.lvl.grid[y+1][x] == "$":
                                    blocked = (self.lvl.grid[y][x-1] == "#" and self.lvl.grid[y+1][x-1] == "#") or (self.lvl.grid[y][x+1] == "#" and self.lvl.grid[y+1][x+1] == "#")
                        if blocked:
                            break
            if blocked:
                break
        return blocked

    def detect_possible_pos(self): # detect places where the player can PULL cases
        pos = deepcopy(self.lvl.targets_pos)
        history = []
        while len(pos) > 0:
            test_pos = pos.pop()
            for dir in ("l", "r", "u", "d"):
                new_player_pos = (get_y(test_pos[1], dir, 2), get_x(test_pos[0], dir, 2))
                if new_player_pos[0] < len(self.lvl.grid):
                    if new_player_pos[1] < len(self.lvl.grid[new_player_pos[0]]):
                        if self.lvl.grid[new_player_pos[0]][new_player_pos[1]] != "#":
                            new_pos = (get_x(test_pos[0], dir, 1), get_y(test_pos[1], dir, 1))
                            if self.lvl.grid[new_pos[1]][new_pos[0]] != "#":
                                if not new_pos in history:
                                    history.append(new_pos)
                                    pos.append(new_pos)
        return history+self.lvl.targets_pos

    def solve(self, win, config):
        possible_pos = self.detect_possible_pos()
        # try first with light_solve (don't move cases if they are on targets)
        t = time.time()
        solution = self.do_solve(win, config, possible_pos, True)
        if solution is None:
            solution = self.do_solve(win, config, possible_pos, False)
        if solution is not None:
            print("Résolut en: {}s".format(round(time.time()-t, 2)))
        return solution

    def do_solve(self, win, config, possible_pos, light_solve=False):
        open_paths = [(deepcopy(self.lvl.grid), (self.lvl.player.x, self.lvl.player.y), "")]
        history = []
        while len(open_paths) > 0:
            test_path = open_paths.pop()
            self.lvl.grid = deepcopy(test_path[0])
            self.lvl.player.x, self.lvl.player.y = test_path[1]
            solution = test_path[2]
            for dir in ("l", "r", "u", "d"):
                if light_solve:
                    targets_pos = (get_y(self.lvl.player.y, dir, 1), get_x(self.lvl.player.x, dir, 1))
                    if self.lvl.grid[targets_pos[0]][targets_pos[1]] == "$":
                        case_targets_pos = (get_y(self.lvl.player.y, dir, 2), get_x(self.lvl.player.x, dir, 2))
                        if self.lvl.grid[case_targets_pos[0]][case_targets_pos[1]] != ".":
                            ok = False
                            for t in self.lvl.targets_pos:
                                if targets_pos[1] == t[0] and targets_pos[0] == t[1]:
                                    ok = True
                                    break
                            if ok: # we would moved a case which is already on a target
                                continue
                backup_player_pos = (self.lvl.player.x, self.lvl.player.y)
                self.lvl.handle_collision(dir)
                win.fill(config["wallpaper"])
                self.lvl.draw(win)
                pygame.display.update()
                if backup_player_pos != (self.lvl.player.x, self.lvl.player.y): # player moved
                    if self.is_blocked(possible_pos):
                        # reinitializing the level
                        self.lvl.grid = deepcopy(test_path[0])
                        self.lvl.player.x, self.lvl.player.y = test_path[1]
                        solution = test_path[2]
                    else:
                        if (self.lvl.grid, (self.lvl.player.x, self.lvl.player.y)) in history:
                            # reinitializing the level
                            self.lvl.grid = deepcopy(test_path[0])
                            self.lvl.player.x, self.lvl.player.y = test_path[1]
                            solution = test_path[2]
                        else:
                            if self.lvl.is_success():
                                print(test_path[2]+dir)
                                open_paths.clear() # stop the while loop
                                return test_path[2]+dir
                            else:
                                solution += dir
                                open_paths.append((deepcopy(self.lvl.grid), (self.lvl.player.x, self.lvl.player.y), solution))
                                history.append((deepcopy(self.lvl.grid), (self.lvl.player.x, self.lvl.player.y)))
        return None
