import json
from objects import *
import mido

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

def myround(x, base=5):
    return int(base * round(float(x)/base))

def createChords(mid):
    chords = []
    tempo = 0
    timeSignature = (0,0)
    for msg in mid:
        if msg.type == "time_signature":
            timeSignature = (msg.dict()['numerator'],msg.dict()['denominator'])
        if msg.type == "set_tempo":
            tempo = msg.dict()['tempo']
        if not msg.is_meta and msg.type == "note_on" or msg.type == "note_off":
            if "note" in msg.dict():
                note = Note(getFrequency(msg.dict()['note']),msg.dict()['note'],numToNote(msg.dict()['note']))
                duration = (mido.second2tick(msg.time,mid.ticks_per_beat,tempo)/mid.ticks_per_beat)/timeSignature[1]
                if msg.time > 0:
                    if msg.type == "note_on":
                        chords.append(Chord([note],duration))
                    elif msg.type == "note_off":
                        if len(chords) == 0:
                            chords.append(Chord([note],duration))
                        else:
                            chords.append(Chord([],duration))
                elif msg.type == "note_on" and msg.time <= 0:
                    lastIndex = len(chords) - 1
                    if lastIndex >= 0:
                        chords[lastIndex].notes += [note]
                    elif lastIndex < 0:
                        chords.append(Chord([note],1))
    return chords

def createSong(mid):
    tempo = 0
    timeSignature = (0,0)
    name = ""
    for msg in mid: 
        if msg.type == "time_signature":
            timeSignature = (msg.dict()['numerator'],msg.dict()['denominator'])
        if msg.type == "set_tempo":
            tempo = msg.dict()['tempo']
        if msg.type == 'track_name':
            name = msg.dict()['name']
        
    return Song(timeSignature,tempo,createChords(mid),name)


    

def writeJSON(song):

    song.writeChordsReadable()

    dictionary = {
        song.name : song.chordsReadable
    }

    json_object = json.dumps(dictionary, indent = 1)

    with open(f"songs/{song.name}.json","w") as outfile:
        outfile.write(json_object)
    


