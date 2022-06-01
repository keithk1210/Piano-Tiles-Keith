from resources import *

from objects import *
import gensound
import random

def createTile(win,noteValue,beat,notes=None,keyboard=None):
    Tile.nextBeat()
    if notes is not None and keyboard is not None:
        if beat < len(notes):
            if len(notes[beat]) == 1:
                height = noteValue * TILE_HEIGHT
                horizontalPos = random.randint(0,3)
                x = horizontalPos * TILE_WIDTH
                y = -height
                tile = Tile(x,y,height,horizontalPos,beat,win)
                tile.color = SCREEN_COLOR
                tile.rest = True
                tile.ignore = True
                return tile
            else:
                height = noteValue * TILE_HEIGHT
                horizontalPos = random.randint(0,3)
                x = horizontalPos * TILE_WIDTH
                y = -height
                return Tile(x,y,height,horizontalPos,beat,win)
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
            sound += gensound.Sawtooth(note,.5e3)
    if len(chord) > 0:
        if chord[0]:
            sound.play(max_amplitude = .1)
            if currentBeat - 1 > 0:
                print("")

