import os
import winsound
import easygui
from resources import *

from objects import Tile
import gensound
import random

def create_tile(win,chord,beat,song,game_started): #this method is important because it advanctes the beat of the tile
    global tile_height
    if game_started:
        """havent added rests yet
        if beat[0] < len(measures) and beat[1]+1 < len(measures[beat[0]].chords):
            note_val = measures[beat[0]].chords[beat[1]+1][0]
            
            if len(measures[beat[0]].chords[beat[1]+1]) == 1: 
                height = note_val * Tile.tile_height
                horizontalPos = random.randint(0,3)
                x = horizontalPos * TILE_WIDTH
                y = -height
                tile = Tile(x,y,height,horizontalPos,beat,get_random_color(),win)
                tile.color = SCREEN_COLOR
                tile.rest = True
                tile.ignore = True
                Tile.next_chord(song)
                return tile
            else:
                """
    #this is used to create the very first tile
    height = chord.duration * Tile.tile_height
    horizontalPos = random.randint(0,3)
    x = horizontalPos * TILE_WIDTH
    y = -height
    Tile.next_chord(song)
    if chord.notes[0].name == "Rest":
        return Tile(x,y,height,horizontalPos,chord,SCREEN_COLOR,win,True)
    else:
        return Tile(x,y,height,horizontalPos,chord,get_random_color(),win,False)

def produce_sound(song,current_chord):
    chord = song.measures[current_chord[0]].chords[current_chord[1]] 
    """
    duration_in_beats =  chord.duration #the 0th index of a chord represents the duration of the chord in beats
    duration_in_seconds = (1 / (72 / 60)) * duration_in_beats
    duration_in_ms = float(duration_in_seconds * 1000)
    sound = gensound.Sawtooth(0,0)
    """
    winsound.PlaySound(None, winsound.SND_PURGE)
    for note in chord.notes:
        if note:
            print("note name: " + note.name + " enharmonic equivalent: " + note.get_enharmonic_equivalent())
            winsound.PlaySound("piano_keys\\" + note.get_enharmonic_equivalent() + ".wav",winsound.SND_ASYNC)


def get_tile_speed(bpm,tile_height):
    seconds_in_one_beat = (1/bpm) * 60
    pixel_per_frame = (Tile.tile_height) * (1/FPS) * (1/seconds_in_one_beat)
    return round(pixel_per_frame)

def get_random_color():
    return RAINBOW[random.randint(0,len(RAINBOW)-1)]

def open_JSON_dir():
    return easygui.fileopenbox(msg="Please select a JSON file",default='C:\\Users\\keith\\coding-projects\\Python\\MIDI_To_Piano_Tiles_JSON\\songs\\*.json')

def update_text_on_text_display(text_display,text):
    text_display.text = pygame.font.Font(None,100).render(text,True,BLACK)


