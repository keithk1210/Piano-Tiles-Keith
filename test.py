from threading import Thread
import threading
from tracemalloc import start
from mido import MidiFile
from numpy import append
from resources import *
from pygame import *
from objects import *
import mido
import pygame
import rtmidi
import sys
import time as pytime
import json
import gensound


pygame.init()

FPS = 60
clock = pygame.time.Clock()

mid = MidiFile('C:\\Users\\keith\\coding-projects\\Python\\MIDO\\MIDI\\Ode-To-Joy.mid', clip=True)

port = mido.open_output()

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)

currentMessageIndex = 0
currentTick = 0
lenMsgs = 0
msgs = []

tracksIndex = 1

flag = False
starttime = 0
song = []

def numToNote(num):
    str = ""
    remainder = (num - 21) % 12
    octave = (num - 12) // 12
    if remainder == 0:
        str += "A"
    elif remainder == 1:
        str += "Bb"
    elif remainder == 2:
        str += "B"
    elif remainder == 3:
        str += "C"
    elif remainder == 4:
        str += "C#"
    elif remainder == 5:
        str += "D"
    elif remainder == 7:
        str += "E"
    elif remainder == 8:
        str += "F"
    elif remainder == 9:
        str += "F#"
    elif remainder == 10:
        str += "G"
    elif remainder == 11:
        str += "A"
    return "%s%d" % (str,octave)

def getFrequency(note):
    return (2 ** ((note - 69)/12)) * 440

"""
for msg in mid:
    if not msg.is_meta and msg.type == "note_on":
        if "note" in msg.dict():
            note = numToNote(msg.dict()['note'])
            print(msg.dict)
            #("%s %d %f" % (note,msg.note,msg.time))
            if msg.time > 0:
                song.append([note])
            else:
                lastIndex = len(song) - 1
                if lastIndex >= 0:
                    song[lastIndex] += [note]
                elif lastIndex < 0:
                    song.append([note])
"""
sustainedNotes = []

for msg in mid:
   
    if not msg.is_meta and msg.type == "note_on" or msg.type == "note_off":
        print(msg.dict())
        if "note" in msg.dict():
            note = Note(getFrequency(msg.dict()['note']),msg.dict()['note'],numToNote(msg.dict()['note']))
            if msg.time > 0:
                if msg.type == "note_on":
                    song.append(Chord([note],msg.time))
                elif msg.type == "note_off":
                    song.append(Chord([],msg.time))
            elif msg.type == "note_on" and msg.time <= 0:
                lastIndex = len(song) - 1
                if lastIndex >= 0:
                    song[lastIndex].notes += [note]
                elif lastIndex < 0:
                    song.append(Chord([note],1))
                

notes = []

for chord in song:
    print(chord.notes)
    if not chord.notes or chord.notes[0] == None:
        song.remove(chord)



for i in range(0,len(song)):
    notesList = []
    if song[i].notes:
        for j in range(0,len(song[i].notes)):
            if (song[i].notes[j]):
                notesList.append(song[i].notes[j].noteName)
    if notesList:
        notes.append(notesList)




print(notes)

songs = {
    "Mary had a little lamb" : notes
}

json_object = json.dumps(songs, indent = 1)

with open("sample.json","w") as outfile:
    outfile.write(json_object)

running = True

currentBeat = 0


def play_notes(notePath):
    note = pygame.mixer.Sound(notePath)
    note.play()

#print(song)

while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_q:
                    chord = notes[currentBeat]
                    sound = gensound.Sine(0,0)
                    
                    for note in chord:
                        if note:
                            print(note)
                            sound += gensound.Sine(note,.95e3)
                    if currentBeat - 1 > 0:
                            print("duration %d" % (song[currentBeat-1].duration))
                    
                    if chord[0]:
                        sound.play(max_amplitude = .25)
                        if currentBeat - 1 > 0:
                            #pygame.time.delay(int(song[currentBeat-1].duration) * 2)
                            pygame.time.delay(100)
                    currentBeat += 1

    
pygame.quit()



