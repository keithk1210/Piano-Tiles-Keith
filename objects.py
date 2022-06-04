from random import random
from resources import *
import pygame
import copy
class Screen:
	def __init__(self,tiles,surface):
		self.tiles = tiles
		self.surface = surface

class Measure:
	def __init__(self,chords):
		self.chords = chords

class Song:
    def __init__(self,timeSignature,tempo,name):
        self.timeSignature = timeSignature
        self.tempo = tempo
        self.measuresReadable = []
        self.chordsReadable = []
        self.chords = []
        self.name = name
        self.measures = 0

class Tile(pygame.sprite.Sprite):
	lastSpawnTime = 0
	currentBeat = [0,0]
	lastBeatUpdate = 0
	speed = 2
	def __init__(self, x, y,height,horizontalPos,beat, win):
		super(Tile, self).__init__()

		self.win = win
		self.x, self.y = x, y
		self.color = BLUE

		self.ignore = False
		self.rest = False

		self.surface = pygame.Surface((TILE_WIDTH, height), pygame.SRCALPHA)
		self.rect = self.surface.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.height = height
		self.horizontalPos = horizontalPos
		
		self.beat = beat #self.beat[0] -> measure, self.beat[1] --> beat in measure
		

		self.center = TILE_WIDTH//2, TILE_HEIGHT//2 + 15
		self.line_start = self.center[0], self.center[1]-18
		self.line_end = self.center[0], 20

	def update(self):
		self.rect.y += self.speed

		if not self.ignore:
			pygame.draw.rect(self.surface, self.color, (0,0, TILE_WIDTH, self.height),border_radius=25)
		elif self.rest:
			pygame.draw.rect(self.surface, SCREEN_COLOR, (0,0, TILE_WIDTH, self.height),border_radius=25)
		else:
			pygame.draw.rect(self.surface, PURPLE, (0,0, TILE_WIDTH, self.height),border_radius=25)

		
		self.win.blit(self.surface, self.rect)
	def setIgnore(self,ignore):
		self.ignore = ignore

	def nextBeat(song):
		if Tile.currentBeat[1] + 1 < song.timeSignature[0]:
			Tile.currentBeat[1] += 1
		else:
			Tile.currentBeat[0] += 1
			Tile.currentBeat[1] = 0

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

class Button(pygame.sprite.Sprite):
	def __init__(self, x, y,text,click_function):
		super(Button, self).__init__()
		
		self.surface = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA)
		self.rect = self.surface.get_rect()
		self.rect.center  = (WIDTH // 2, HEIGHT // 2)
		self.rect.x = x
		self.rect.y = y
		self.font = pygame.font.Font(None,20)
		self.text = self.font.render(text,True,BLUE,BLUE2)
		self.text.get_rect().center = (WIDTH // 2, HEIGHT // 2)
		self.click_function = click_function
		self.clicked = False

	def draw(self, win):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True
				return self.click_function()
			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False
		win.blit(self.text,self.rect)
		return action

        
class Keyboard:
	def __init__(self):
		self.timeSinceLastKeyPress = 0
		self.beat = [0,0]
	def nextBeat(self,song):
		if self.beat[1] + 1 < song.timeSignature[0]:
			self.beat[1] += 1
		else:
			self.beat[0] += 1
			self.beat[1] = 0
		
	def getCurrentBeat(self):
		return self.beat

    

    