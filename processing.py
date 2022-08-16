import json
from objects import Song
import mido
import os




def myround(x, base=5):
    return int(base * round(float(x)/base))


def write_json(song):
    measuresSerializable = []
    for i in range(0,len(song.measures)):
        measuresSerializable.append("")
        for j in range(0,len(song.measures[i].chords)):
            measuresSerializable[len(measuresSerializable)-1] += song.measures[i].chords[j].__str__() + ", "
        measuresSerializable.append( song.measures[i].shortest_rhythm_value)
    dictionary = {
        song.name : measuresSerializable
    }
    json_object = json.dumps(dictionary, indent = 1)
    with open(os.getenv("APPDATA") + "\\PianoTilesKeith\\output\\" + song.name + ".json","w") as outfile:
        outfile.write(json_object)


def openJSON(jsonFileName):
    notes_dict = {}
    with open(jsonFileName.replace("\\","\\\\"),"r") as outfile:
        notes_dict = json.load(outfile)
    return notes_dict

    


