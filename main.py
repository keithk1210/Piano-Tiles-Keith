from math import prod
from tracemalloc import start
from mido import MidiFile
from numpy import append
from framework_objects import *
from resources import *
from pygame import *
from objects import *
from framework_objects import *
from utils import *

import pygame

import time as pytime

#TODO
#issues arise near the end of a song for some reason 
#improve playability - the window to make a note sound is too short
#add a menu and something that lets you restart the level
#make it look better
#-main menu looks bad

pygame.init()
clock = pygame.time.Clock()



win = pygame.display.set_mode((WIDTH,HEIGHT))
win.fill(WHITE)
pygame.display.set_caption("Piano Tiles")




notes = []
running = True
noteSpawnDT = 0

#game states

#font



#screen = Screen([createTile(win,notes[0][0] * song.timeSignature[1],0)],win)
#keyboard = Keyboard()
game_state_manager = GameStateManager()
menu_state = MenuState(win,game_state_manager)
game_state_manager.add_state(menu_state)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        game_state_manager.peek().event_loop_update(event) 
        
    if not game_state_manager.peek().update():
       running = False
    clock.tick(FPS)
    pygame.display.update()
    win.fill(WHITE)

pygame.quit()

