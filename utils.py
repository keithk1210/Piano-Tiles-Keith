from resources import *
from objects import Tile
import gensound
import random

def createTile(win,noteValue,beat):
    height = noteValue * TILE_HEIGHT
    horizontalPos = random.randint(0,3)
    x = horizontalPos * TILE_WIDTH
    y = -height
    return Tile(x,y,height,horizontalPos,beat,win)

def produceSound(notes,currentBeat):
    chord = notes[currentBeat]
    sound = gensound.Triangle(0,0)
    
    for note in chord:
        if note:
            sound += gensound.Triangle(note,.5e3)
    if len(chord) > 0:
        if chord[0]:
            sound.play(max_amplitude = .1)
            if currentBeat - 1 > 0:
                print("")
    print("currentBeat %d" % (currentBeat))