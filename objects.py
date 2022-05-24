class Note:
    def __init__(self,frequency,midiNum,noteName):
        self.frequency = frequency
        self.midiNum = midiNum
        self.noteName = noteName
    def __eq__(self, obj) -> bool:
        return isinstance(obj,Note) and self.noteName == obj.noteName

class Chord:
    def __init__(self,notes,duration):
        self.notes = notes
        self.duration = duration * 1000
    