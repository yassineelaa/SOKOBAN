#!/usr/bin/env python3
import pygame, sys, random, yaml
from copy import deepcopy
from pygame.locals import *

from grid_utils import *
from solver import Solver

f = open("config.yaml", "r")
config = yaml.safe_load(f.read())
f.close()

def load_img(filepath): # create pygame image from file path
    img = pygame.image.load(filepath)
    return pygame.transform.scale(img, (config["SQUARE_SIZE"], config["SQUARE_SIZE"]))

class Player:
    img = load_img(config["imgs"]["player"])
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self, win, coord):
        win.blit(self.img,((coord[0]+self.x)*config["SQUARE_SIZE"], (coord[1]+self.y)*config["SQUARE_SIZE"]))
    def up(self):
        self.y -= 1
    def down(self):
        self.y += 1
    def right(self):
        self.x += 1
    def left(self):
        self.x -= 1

class Level: # class holding all data for one level
    wall = load_img(config["imgs"]["wall"])
    case = load_img(config["imgs"]["case"])
    target = load_img(config["imgs"]["target"])

    def __init__(self):
        self.player = None
        self.grid = []
        self.width, self.height = 0, 0
        self.targets_pos = []
        self.solution = ""

    def init(self, coord):
        self.backup_grid = deepcopy(self.grid)
        self.backup_player_pos = (self.player.x, self.player.y)
        self.coord = coord

    def draw(self, win):
        for t in self.targets_pos: # draw targets from targets_pos to redraw them when unhidden
            win.blit(self.target, ((self.coord[0]+t[0])*config["SQUARE_SIZE"], (self.coord[1]+t[1])*config["SQUARE_SIZE"]))
        for y in range(self.height):
            for x in range(self.width):
                if len(self.grid[y]) > x:
                    if self.grid[y][x] == "#":
                        win.blit(Level.wall, ((self.coord[0]+x)*config["SQUARE_SIZE"],  (self.coord[1]+y)*config["SQUARE_SIZE"]))
                    elif self.grid[y][x] == "$":
                        win.blit(Level.case, ((self.coord[0]+x)*config["SQUARE_SIZE"],  (self.coord[1]+y)*config["SQUARE_SIZE"]))
                    elif self.grid[y][x] == "*":
                        win.blit(Level.target, ((self.coord[0]+t[0])*config["SQUARE_SIZE"],  (self.coord[1]+t[1])*config["SQUARE_SIZE"]))
                        win.blit(Level.case, ((self.coord[0]+x)*config["SQUARE_SIZE"],  (self.coord[1]+y)*config["SQUARE_SIZE"]))
        self.player.draw(win, self.coord)

    def is_success(self): #check that all cases are on a target
        for y in range(self.height):
            for x in range(self.width):
                if len(self.grid[y]) > x:
                    if self.grid[y][x] == "$":
                        ok = False
                        for t in self.targets_pos:
                            if t[0] == x and t[1] == y:
                                ok = True
                                break
                        if not ok:
                            return False
        return True

    def reset(self):
        self.grid = deepcopy(self.backup_grid)
        self.player.x, self.player.y = self.backup_player_pos

    def handle_collision(self, dir): # try to move player if possible, handling cases movements
        move_player = False
        target = self.grid[get_y(self.player.y, dir, 1)][get_x(self.player.x, dir, 1)]
        if target == "$" or target == "*":
            box_target = self.grid[get_y(self.player.y, dir, 2)][get_x(self.player.x, dir, 2)]
            if box_target == " " or box_target == ".":
                self.grid[get_y(self.player.y, dir, 2)][get_x(self.player.x, dir, 2)] = "$"
                if target == "*":
                    self.grid[get_y(self.player.y, dir, 1)][get_x(self.player.x, dir, 1)] = "."
                else:
                    self.grid[get_y(self.player.y, dir, 1)][get_x(self.player.x, dir, 1)] = " "
                move_player = True
        elif target == " " or target == ".":
            move_player = True
        if move_player:
            if dir == "l":
                self.player.left()
            elif dir == "r":
                self.player.right()
            elif dir == "u":
                self.player.up()
            elif dir == "d":
                self.player.down()

    def play(self, win, config, movements): # play a recorded sequence of movements
        for d in movements:
            self.handle_collision(d)
            win.fill(config["wallpaper"])
            self.draw(win)
            pygame.display.update()

class Sokoban:
    def __init__(self, config):
        self.config = config
        self.levels = Sokoban.parse_levels(config["levels_file"])

    def print_help():
        print("""
        Déplacements:                   Flèches du clavier
        Réinitialiser le niveau:        {}
        Solveur automatique:            {}
        Solveur enregistré:             {}
        Enregitrer une solution:        {}
        Entrer des déplacements:        {}
        Démarrer un combat:             {}

        Editez ces paramètres dans le fichier "config.yaml".
        """.format(
                config["keys"]["reset"][1],
                config["keys"]["autosolve"][1],
                config["keys"]["savedsolve"][1],
                config["keys"]["record"][1],
                config["keys"]["input"][1],
                config["keys"]["fight"][1]
            ))

    def parse_levels(filepath): # load levels from a file as Level objects
        levels = [Level()]
        with open(filepath, "r") as f:
            x, y = 0, 0
            widths = []
            while True:
                line = f.readline()
                if not line: # EOF
                    break
                elif len(line) > 1:
                    if line[0] != ";":
                        if line[0] == "=": # solution
                            levels[-1].solution = line[1:].strip()
                        else:
                            levels[-1].grid.append([])
                            for c in line:
                                if c in ["#", "@", "$", ".", "*", "+", " "]:
                                    if c == "@" or c == "+":
                                        levels[-1].player = Player(x, y)
                                        if c == "@":
                                            levels[-1].grid[y].append(" ")
                                        else:
                                            levels[-1].grid[y].append(".")
                                            levels[-1].targets_pos.append((x, y))
                                    else:
                                        levels[-1].grid[y].append(c)
                                        if c == "." or c == "*":
                                            levels[-1].targets_pos.append((x, y))
                                x += 1
                            widths.append(x-1)
                            y += 1
                            x = 0
                    elif y > 0:
                        levels[-1].height = y
                        levels[-1].width = max(widths)
                        levels.append(Level())
                        widths.clear()
                        y = 0
        return levels

    def play(self):
        Sokoban.print_help()
        #Musique
        file = 'music/Cybersdf-Dolling.wav'
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1) # If the loops is -1 then the music will repeat indefinitely.
        #effectSound
        hitSound = pygame.mixer.Sound('music/clack.wav')

        font = pygame.font.SysFont("Comic Sans MS", 30)
        text_player = font.render("Player", False, (255, 255, 255))
        text_bot = font.render("Bot", False, (255, 255, 255))
        for lvl in self.levels:
            lvl_bot = None
            bot_solution_index = 0 # index of the current movement in the solution
            win = pygame.display.set_mode((lvl.width*self.config["SQUARE_SIZE"], lvl.height*self.config["SQUARE_SIZE"]))
            pygame.display.set_caption(self.config["title"])
            lvl.init((0, 0))
            recorded = ""
            record = False
            while True:
                pygame.time.delay(self.config["pygame_delay"])
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                direction = None
                keys = pygame.key.get_pressed()
                if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and keys[pygame.K_n]: # Cheat code to skip a level
                    if lvl_bot is None:
                        break
                elif keys[getattr(pygame, self.config["keys"]["autosolve"][0])]:
                    if lvl_bot is None:
                        solver = Solver(lvl)
                        solver.solve(win, self.config)
                elif keys[pygame.K_LEFT]:
                    direction = "l"
                elif keys[pygame.K_RIGHT]:
                    direction = "r"
                elif keys[pygame.K_UP]:
                    direction = "u"
                elif keys[pygame.K_DOWN]:
                    direction = "d"
                elif keys[getattr(pygame, self.config["keys"]["reset"][0])]:
                    if record:
                        recorded = ""
                    if lvl_bot is not None:
                        lvl_bot.reset()
                        bot_solution_index = 0
                    lvl.reset()
                elif keys[getattr(pygame, self.config["keys"]["input"][0])]:
                    m = input("Déplacements: ")
                    lvl.play(win, self.config, m)
                elif keys[getattr(pygame, self.config["keys"]["record"][0])]:
                    lvl.reset()
                    if lvl_bot is not None:
                        lvl_bot.reset()
                        bot_solution_index = 0
                    record = True
                    print("Recording started")
                elif keys[getattr(pygame, self.config["keys"]["savedsolve"][0])]:
                    if lvl_bot is None:
                        if lvl.solution:
                            lvl.reset()
                            lvl.play(win, config, lvl.solution)
                        else:
                            print("Pas de solution enregistrée")
                elif keys[getattr(pygame, self.config["keys"]["fight"][0])]:
                    if lvl.solution:
                        lvl.reset()
                        lvl.coord = ((0, 1))
                        win = pygame.display.set_mode(((2+lvl.width*2)*self.config["SQUARE_SIZE"], (lvl.height+1)*self.config["SQUARE_SIZE"]))
                        lvl_bot = Level()
                        lvl_bot.player = Player(lvl.player.x, lvl.player.y)
                        lvl_bot.grid = deepcopy(lvl.grid)
                        lvl_bot.width = lvl.width
                        lvl_bot.height = lvl.height
                        lvl_bot.targets_pos = lvl.targets_pos
                        lvl_bot.init((lvl.width+2, 1))
                    else:
                        print("Pas de solution enregistrée. Joue tout seul.")
                if direction is not None:
                    hitSound.play()
                    if record:
                        recorded += direction
                    lvl.handle_collision(direction)
                    if lvl_bot is not None:
                        lvl_bot.handle_collision(lvl.solution[bot_solution_index])
                        bot_solution_index += 1
                win.fill(self.config["wallpaper"])
                lvl.draw(win)
                if lvl_bot is not None:
                    lvl_bot.draw(win)
                    win.blit(text_player, (self.config["SQUARE_SIZE"]/2, 0))
                    win.blit(text_bot, ((lvl.width+2.5)*self.config["SQUARE_SIZE"],0))
                pygame.display.update()

                # handling level success
                player_win = lvl.is_success()
                if lvl_bot is not None:
                    bot_win = lvl_bot.is_success()
                    if bot_win and not player_win:
                        print("Perdu !")
                        lvl.reset()
                        lvl_bot.reset()
                        bot_solution_index = 0
                    elif (player_win and not bot_win) or (player_win and bot_win):
                        break
                elif player_win:
                    break

            if record:
                print(recorded)

if __name__ == "__main__":
    pygame.init()
    Sokoban(config).play()
