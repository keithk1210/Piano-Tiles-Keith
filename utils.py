import easygui
from resources import *

from objects import *
import gensound
import random

def createTile(win,noteValue,beat,song,measures=None,keyboard=None): #this method is important because it advanctes the beat of the tile
    Tile.nextBeat(song)
    print("note value %s " % (noteValue))
    if measures is not None and keyboard is not None:
        if beat[0] < len(measures):
            if len(measures[beat[0]].chords[beat[1]]) == 1:
                
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

def produceSound(measures,currentBeat):
    chord = measures[currentBeat[0]].chords[currentBeat[1]][1:len(measures[currentBeat[0]].chords[currentBeat[1]])]
    sound = gensound.Triangle(0,0)
    
    for note in chord:
        if note:
            sound += gensound.Sawtooth(note,.5e3)
    if len(chord) > 0:
        if chord[0]:
            sound.play(max_amplitude = .1)

def open_JSON_dir():
    return easygui.fileopenbox(msg="Please select a JSON file",default='songs\\*.json')
