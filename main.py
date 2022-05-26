from math import prod
from threading import Thread
import threading
from tracemalloc import start
from mido import MidiFile
from numpy import append
from resources import *
from pygame import *
from objects import *
from processing import *
from utils import *
import mido
import pygame
import rtmidi
import sys
import time as pytime
import json
import gensound
import random




pygame.init()

FPS = 60
clock = pygame.time.Clock()

mid = MidiFile('C:\\Users\\keith\\coding-projects\\Python\\MIDO\\MIDI\\Ode-To-Joy.mid', clip=True)

port = mido.open_output()

win = pygame.display.set_mode((WIDTH,HEIGHT))
win.fill(WHITE)

screen = Screen([createTile(win,1,0)],win)
keyboard = Keyboard()

song = createSong(mid)
notes = []
running = True
currentBeat = 0
currentBeatForTiles = 0
noteSpawnDT = 0

with open(f'songs/{song.name}.json') as file:
	notes_dict = json.load(file)
song.chordsReadable = notes_dict
notes = song.chordsReadable[song.name]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_q or event.key == pygame.K_w or event.key == pygame.K_e or event.key == pygame.K_r:
                for tile in screen.tiles:
                    if tile.rect.bottom >= HEIGHT and tile.rect.bottom <= HEIGHT + tile.height:
                        if pygame.time.get_ticks() - keyboard.timeSinceLastKeyPress > KEY_PRESS_DELAY:
                            if not tile.ignore:
                                if tile.horizontalPos == 0 and event.key == pygame.K_q:
                                    tile.setIgnore(True)
                                    produceSound(notes,currentBeat)
                                    currentBeat +=1
                                    keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
                                elif tile.horizontalPos == 1 and event.key == pygame.K_w:
                                    tile.setIgnore(True)
                                    produceSound(notes,currentBeat)
                                    currentBeat +=1
                                    keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
                                elif tile.horizontalPos == 2 and event.key == pygame.K_e:
                                    tile.setIgnore(True)
                                    produceSound(notes,currentBeat)
                                    currentBeat +=1
                                    keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
                                elif tile.horizontalPos == 3 and event.key == pygame.K_r:
                                    tile.setIgnore(True)
                                    produceSound(notes,currentBeat)
                                    currentBeat +=1
                                    keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
    for tile in screen.tiles:
        tile.update()
        if pygame.time.get_ticks()- Tile.lastSpawnTime > NOTE_SPAWN_DELAY and abs(tile.rect.y) <= tile.speed/2:
            screen.tiles.append(createTile(win,notes[currentBeatForTiles][0] * song.timeSignature[1],currentBeatForTiles))
            currentBeatForTiles += 1
            Tile.lastSpawnTime = pygame.time.get_ticks()
        if not tile.ignore and tile.rect.top > HEIGHT:
            print(tile.rect.y)
            print(tile)
            running = False
            print("You lose!")
    clock.tick(FPS)
    pygame.display.update()

pygame.quit()



