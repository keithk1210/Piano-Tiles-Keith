from random import random
from resources import *
import pygame
import copy
import abc

class Screen:
	def __init__(self,surface):
		self.tiles = []
		self.surface = surface

class Measure:
    def __init__(self):
        self.chords = []
        self.shortest_rhythm_value = 9999
class Chord:
    def __init__(self):
        self.notes = []
        self.duration = None
    def set_duration(self,new_dur):
        self.duration = new_dur
    def notes_as_str(self):
        str = ""
        for note in self.notes:
            str += note.__str__()+ ", "
        return str
    def __str__(self) -> str:
        return "Notes: [" + self.notes_as_str() + "]"
class Note:
	def __init__(self,name):
		self.name = name
		self.duration = None
	def set_duration(self,new_dur):
		self.duration = new_dur
	def get_enharmonic_equivalent(self):
		if len(self.name) >= 3:
			octave = self.name[2]
			if self.name[0:2] == "Bb":
				return "A#" + octave
			elif self.name[0:2] == "Db":
				return "C#" + octave
			elif self.name[0:2] == "Eb":
				return "D#" + octave
			elif self.name[0:2] == "Gb":
				return "F#" + octave
			else:
				return self.name
		else:
			return self.name
	def __str__(self):
		return "Note name: " + self.name + " Duration: " + str(self.duration)

class Song:
	def __init__(self,tree,name):
		#song creation -> write measures
		self.tree = tree
		self.root = tree.getroot()
		self.bpm = None
		self.beats_per_second = None
		self.measures = []
		self.name = name
		self.selected_staff = 1
		self.write_measures()

	def get_rhythmic_val(self,type_str):
		if type_str == "whole":
			return 4
		elif type_str == "half":
			return 2
		elif type_str == "quarter":
			return 1
		elif type_str == "eighth":
			return .5
		elif type_str == "16th":
			return .25
		elif type_str == "32nd":
			return .125

	def new_note_str(self,note):
		new_note = ""
		for pitch in note.iter("pitch"):
			alter = 0
			for step in note.iter("step"):
				new_note += step.text
			for accidental in pitch.iter("alter"):
				if (int(accidental.text) == 1):
					new_note += "#"
					alter = int(accidental.text)
				elif (int(accidental.text) == -1):
					new_note += "b"
					alter = int(accidental.text)
			for octave in note.iter("octave"):
				new_note += octave.text
		return new_note

	def write_measures(self):
		time_sig = []
		for measure in self.root.iter("measure"):
			for attr in measure.iter("attributes"):
				for time in attr.iter("time"):
					for beats in time.iter("beats"):
						time_sig.append(int(beats.text))
					for beat_type in time.iter("beat-type"):
						time_sig.append(int(beat_type.text))
			new_measure = Measure()
			new_chord = None
			for note in measure.iterfind("note"):
				if note.find("staff") != None: #check we're looking at the right staff
					if int(note.find("staff").text) == self.selected_staff:
						new_note = None
						if note.find("rest") == None:
							new_note = Note(self.new_note_str(note))
						if note.find("type") != None and new_note:
							current_duration = self.get_rhythmic_val(note.find("type").text)
							#print("type: " + note.find("type").text + " current_duration: " + str(current_duration) + " adjusted duration: " +str(current_duration * (time_sig[1]/4)) )
							new_note.set_duration(current_duration * (time_sig[1]/4))
							if current_duration and current_duration < new_measure.shortest_rhythm_value:
								new_measure.shortest_rhythm_value = current_duration
						print(str(new_note) + " " + str(note.find("chord")))
						if new_note and note.find("chord") == None:
							new_chord = Chord()
							new_chord.set_duration(new_note.duration)
							new_chord.notes.append(new_note)
							new_measure.chords.append(new_chord)
						elif new_note:
							new_measure.chords[len(new_measure.chords)-1].notes.append(new_note)
			self.measures.append(new_measure)




class Tile(pygame.sprite.Sprite):
	lastSpawnTime = 0
	current_chord = [0,0] #should be actually called current chord because beats are irrevelant with this number
	#Tile.current_chord[0] represents the current MEASURE
	#Tile.current_chord[1] represents the current beat within that measure
	lastBeatUpdate = 0
	speed = 2

	height_multiplier_index = 0
	TILE_HEIGHT_MULTIPLIER_OPTIONS = [1,2,4,8,16,32,64]
	height_multiplier = TILE_HEIGHT_MULTIPLIER_OPTIONS[height_multiplier_index]
	tile_height =  (WIDTH // 4) * height_multiplier
	
	def __init__(self, x, y,height,horizontalPos,chord,color,win):
		super(Tile, self).__init__()

		self.win = win
		self.x, self.y = x, y
		self.color = color

		self.ignore = False
		self.rest = False

		self.surface = pygame.Surface((TILE_WIDTH, height), pygame.SRCALPHA)
		self.rect = self.surface.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.height = height
		self.horizontalPos = horizontalPos
		
		self.chord = chord #self.beat[0] -> measure, self.beat[1] --> beat in measure
		

		self.center = TILE_WIDTH//2, Tile.tile_height//2 + 15
		self.line_start = self.center[0], self.center[1]-18
		self.line_end = self.center[0], 20

	def update(self):
		self.rect.y += self.speed

		if not self.ignore:
			pygame.draw.rect(self.surface, self.color, (0,0, TILE_WIDTH, self.height),border_radius=TILE_WIDTH)
		elif self.rest:
			pygame.draw.rect(self.surface, SCREEN_COLOR, (0,0, TILE_WIDTH, self.height),border_radius=TILE_WIDTH)
		else:
			pygame.draw.rect(self.surface, SCREEN_COLOR, (0,0, TILE_WIDTH, self.height),border_radius=TILE_WIDTH)

		
		self.win.blit(self.surface, self.rect)
	def setIgnore(self,ignore):
		self.ignore = ignore

	def next_chord(song):
		#print("tile current chord before next_chord %s" % (Tile.current_chord))
		if Tile.current_chord[1] + 1 < len(song.measures[Tile.current_chord[0]].chords): 
			Tile.current_chord[1] += 1
		elif Tile.current_chord[0] + 1 < len(song.measures):
			Tile.current_chord[0] += 1
			Tile.current_chord[1] = 0
		#print("tile current chord after next_chord %s" % (Tile.current_chord))

	def reset():
		Tile.current_chord[0] = 0
		Tile.current_chord[1] = 0

	def next_multiplier_option(): #moves it along to the next 
	
		if Tile.height_multiplier_index + 1 < len(Tile.TILE_HEIGHT_MULTIPLIER_OPTIONS):
			#print("in here")
			Tile.height_multiplier_index += 1
		else:
			#print("in there")
			Tile.height_multiplier_index = 0

		Tile.height_multiplier = Tile.TILE_HEIGHT_MULTIPLIER_OPTIONS[Tile.height_multiplier_index]
		Tile.tile_height = (WIDTH // 4) * Tile.height_multiplier
		#print("tiLE HEIGHt in Tilenext_multiplier option %f" % (Tile.tile_height))

	

class Text(pygame.sprite.Sprite):
	def __init__(self, text, font, pos, win):
		super(Text, self).__init__()
		self.win = win

		self.x,self.y = pos
		self.initial = self.y
		self.image = font.render(text, True, (255, 255, 255))

	def update(self, speed):
		self.y += speed
		if self.y - self.initial >= 100:
			self.kill()

		self.win.blit(self.image, (self.x, self.y))

class Counter(pygame.sprite.Sprite):
	def __init__(self, win, font):
		super(Counter, self).__init__()

		self.win = win
		self.font = font
		self.index = 1
		self.count = 3

	def update(self):
		if self.index % 30 == 0:
			self.count -= 1

		self.index += 1

		if self.count > 0:
			self.image = self.font.render(f'{self.count}', True, (255, 255, 255))
			self.win.blit(self.image, (WIDTH//2-16, HEIGHT//2-25))

class ScreenElement(pygame.sprite.Sprite,metaclass=abc.ABCMeta):
	BUTTON_X = WIDTH // 2 - BUTTON_WIDTH //2 #this should be a class member of Button
	def __init__(self,y_pos):
		super().__init__()
		self.y_pos = y_pos


class Button(ScreenElement):
	def __init__(self,text,y_pos,win,click_function):
		super().__init__(y_pos)
		self.BUTTON_Y = y_pos * PADDING
		self.rect = pygame.Rect(ScreenElement.BUTTON_X,self.BUTTON_Y,BUTTON_WIDTH,BUTTON_HEIGHT)
		self.color = BLUE2
		self.font = pygame.font.Font(None,30)
		self.text = self.font.render(text,True,BLUE,None)
		self.text_x = ScreenElement.BUTTON_X + BUTTON_WIDTH // 2 -  self.font.size(text)[0] // 2
		self.text_y = (y_pos) * PADDING + BUTTON_HEIGHT // 2 - self.font.size(text)[1] // 2
		self.click_function = click_function
		self.win = win
		self.clicked = False

	def draw(self):		
		pygame.draw.rect(self.win,self.color,self.rect,border_radius=50)
		self.win.blit(self.text,(self.text_x,self.text_y))
	"""
	def return_click_function_val(self,game_state_manager=None,menu_state=None):
		print("left mouse button %s" % (pygame.mouse.get_pressed()[0]))
		if menu_state and game_state_manager: #if the gamestatemanger and menu state are provided as inputs then this means the player wants to go back to the main menu
			pos = pygame.mouse.get_pos()
			if self.rect.collidepoint(pos):
				if pygame.mouse.get_pressed()[0] and not self.clicked:
					action = True
					self.clicked = True
					game_state_manager.clear_states()
					game_state_manager.add_state(menu_state)
					return
				if not pygame.mouse.get_pressed()[0]:
					self.clicked = False
					return
			return

		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True
				return self.click_function()
			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False
	"""


class TextDisplay(ScreenElement):
	def __init__(self,text,y_pos,win):
		super().__init__(y_pos)
		self.text = text
		self.font = pygame.font.Font(None,100)
		self.text = self.font.render(text,True,BLACK)
		self.color = PURPLE

		self.win = win
		self.text_x = WIDTH//2 - self.font.size(text)[0] // 2
		self.text_y = (y_pos * PADDING) - self.font.size(text)[1] // 2

	def draw(self):
		self.win.blit(self.text,(self.text_x,self.text_y))

class ImageScreenElement(ScreenElement):
	def __init__(self, y_pos,img_name,win):
		super().__init__(y_pos)

		self.win = win
		self.image = pygame.image.load("images/%s" % (img_name))
		self.scaled_height = PADDING
		self.scaled_width = (self.image.get_width() / self.image.get_height()) * self.scaled_height
		self.image = pygame.transform.scale(self.image,(self.scaled_width,self.scaled_height))
		self.x = WIDTH//2 - self.scaled_width // 2
		self.y = (y_pos * PADDING) - self.scaled_height // 2

	def draw(self):
		self.win.blit(self.image,(self.x,self.y))

        
class Keyboard:
	def __init__(self):
		self.timeSinceLastKeyPress = 0
		self.current_chord = [0,0]
	def next_chord(self,song):
		if self.current_chord[1] + 1 < len(song.measures[self.current_chord[0]].chords): 
			self.current_chord[1] += 1
		elif self.current_chord[0] + 1 < len(song.measures):
			self.current_chord[0] += 1
			self.current_chord[1] = 0
		
	def get_current_chord(self):
		return self.current_chord

    

    