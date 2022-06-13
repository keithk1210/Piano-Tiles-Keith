from random import random
from resources import *
from utils import *
import pygame
import copy
import abc
class Screen:
	def __init__(self,tiles,surface):
		self.tiles = tiles
		self.surface = surface

class Measure:
	def __init__(self,chords):
		self.chords = chords

class Song:
	def __init__(self,timeSignature,bpm,name):
		self.timeSignature = timeSignature
		self.bpm = bpm
		self.beats_per_second = bpm / 60
		self.chordsReadable = []
		self.measures_readable = []
		self.chords = []
		self.name = name
		self.measures = []

class Tile(pygame.sprite.Sprite):
	lastSpawnTime = 0
	current_chord = [0,0] #should be actually called current chord because beats are irrevelant with this number
	#Tile.current_chord[0] represents the current MEASURE
	#Tile.current_chord[1] represents the current beat within that measure
	lastBeatUpdate = 0
	speed = 2
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
		

		self.center = TILE_WIDTH//2, TILE_HEIGHT//2 + 15
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
		if Tile.current_chord[1] + 1 < len(song.measures[Tile.current_chord[0]].chords)-1: #subtract one because the array represending the notes of the chord holds info about how long the chord should be held.
			Tile.current_chord[1] += 1
		elif Tile.current_chord[0] + 1 < len(song.measures):
			Tile.current_chord[0] += 1
			Tile.current_chord[1] = 0

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

	def return_click_function_val(self,game_state_manager=None,menu_state=None):
		if menu_state and game_state_manager: #if the gamestatemanger and menu state are provided as inputs then this means the player wants to go back to the main menu
			pos = pygame.mouse.get_pos()
			if self.rect.collidepoint(pos):
				if pygame.mouse.get_pressed()[0] and not self.clicked:
					action = True
					self.clicked = True
					game_state_manager.clear_states()
					game_state_manager.add_state(menu_state)
				if not pygame.mouse.get_pressed()[0]:
					self.clicked = False
			
		elif self.click_function:
			action = False
			pos = pygame.mouse.get_pos()
			if self.rect.collidepoint(pos):
				if pygame.mouse.get_pressed()[0] and not self.clicked:
					action = True
					self.clicked = True
					return self.click_function()
				if not pygame.mouse.get_pressed()[0]:
					self.clicked = False


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
		if self.current_chord[1] + 1 < len(song.measures[self.current_chord[0]].chords) - 1: #subtract one because the array represending the notes of the chord holds info about how long the chord should be held.
			self.current_chord[1] += 1
		elif self.current_chord[0] + 1 < len(song.measures):
			self.current_chord[0] += 1
			self.current_chord[1] = 0
		
	def getCurrentBeat(self):
		return self.current_chord

    

    