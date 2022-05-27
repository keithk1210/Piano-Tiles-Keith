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

mid = MidiFile('C:\\Users\\keith\\coding-projects\\Python\\MIDO\\MIDI\\BrahmsLullaby.mid', clip=True)

port = mido.open_output()

win = pygame.display.set_mode((WIDTH,HEIGHT))
win.fill(WHITE)
pygame.display.set_caption("Piano Tiles")



song = createSong(mid)
notes = []
running = True
noteSpawnDT = 0


with open(f'songs/BrahmsLullaby.json', 'r') as openfile:
    notes_dict = json.load(openfile)



song.chordsReadable = notes_dict
notes = song.chordsReadable[song.name]
screen = Screen([createTile(win,notes[0][0] * song.timeSignature[1],0)],win)
keyboard = Keyboard()

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
                                    print(notes[keyboard.getCurrentBeat()])
                                    tile.setIgnore(True)
                                    produceSound(notes,keyboard.getCurrentBeat())
                                    keyboard.nextBeat()
                                    keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
                                elif tile.horizontalPos == 1 and event.key == pygame.K_w:
                                    print(notes[keyboard.getCurrentBeat()])
                                    tile.setIgnore(True)
                                    produceSound(notes,keyboard.getCurrentBeat())
                                    keyboard.nextBeat()
                                    keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
                                elif tile.horizontalPos == 2 and event.key == pygame.K_e:
                                    print(notes[keyboard.getCurrentBeat()])
                                    tile.setIgnore(True)
                                    produceSound(notes,keyboard.getCurrentBeat())
                                    keyboard.nextBeat()
                                    keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
                                elif tile.horizontalPos == 3 and event.key == pygame.K_r:
                                    print(notes[keyboard.getCurrentBeat()])
                                    tile.setIgnore(True)
                                    produceSound(notes,keyboard.getCurrentBeat())
                                    keyboard.nextBeat()
                                    keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
    for tile in screen.tiles:
        tile.update()
        if pygame.time.get_ticks()- Tile.lastSpawnTime > NOTE_SPAWN_DELAY and abs(tile.rect.y) <= tile.speed/2:
            screen.tiles.append(createTile(win,notes[Tile.currentBeat][0] * song.timeSignature[1],Tile.currentBeat,notes,keyboard))
            Tile.lastSpawnTime = pygame.time.get_ticks()
        if not tile.ignore and tile.rect.top > HEIGHT:
            print(tile.rect.y)
            print(tile)
            running = False
            print("You lose!")
        if tile.rest and abs(HEIGHT - tile.rect.top) <= tile.speed/2 and pygame.time.get_ticks() - Tile.lastBeatUpdate > BEAT_UPDATE_DELAY:
            print("in")
            keyboard.nextBeat()
            Tile.lastBeatUpdate = pygame.time.get_ticks()
    clock.tick(FPS)
    pygame.display.update()
    win.fill(WHITE)

pygame.quit()



