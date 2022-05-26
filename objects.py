from random import random
from resources import *
import pygame

class Screen:
	def __init__(self,tiles,surface):
		self.tiles = tiles
		self.surface = surface


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
        self.duration = duration

class Song:
	def __init__(self,timeSignature,tempo,chords,name):
		self.timeSignature = timeSignature
		self.tempo = tempo
		self.chords = chords
		self.chordsReadable = []
		self.name = name
	def writeChordsReadable(self):
		for i in range(0,len(self.chords)):
			notesList = []
			if i + 1 < len(self.chords):
				notesList.append(self.chords[i+1].duration)
			for j in range(0,len(self.chords[i].notes)):
				notesList.append(self.chords[i].notes[j].noteName)
			self.chordsReadable.append(notesList)

class Tile(pygame.sprite.Sprite):
	lastSpawnTime = 0
	def __init__(self, x, y,height,horizontalPos,beat, win):
		super(Tile, self).__init__()

		self.win = win
		self.x, self.y = x, y
		self.color = WHITE
		self.ignore = False

		self.surface = pygame.Surface((TILE_WIDTH, height), pygame.SRCALPHA)
		self.rect = self.surface.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.height = height
		self.horizontalPos = horizontalPos
		self.speed = 2
		self.beat = beat
		

		self.center = TILE_WIDTH//2, TILE_HEIGHT//2 + 15
		self.line_start = self.center[0], self.center[1]-18
		self.line_end = self.center[0], 20

	def update(self):
		self.rect.y += self.speed

		if not self.ignore:
			pygame.draw.rect(self.surface, self.color, (0,0, TILE_WIDTH, TILE_HEIGHT))
			pygame.draw.rect(self.surface, PURPLE, (0,0, TILE_WIDTH, TILE_HEIGHT), 4)
			pygame.draw.rect(self.surface, BLUE2, (0,0, TILE_WIDTH, TILE_HEIGHT), 2)
			pygame.draw.line(self.surface, BLUE, self.line_start, self.line_end, 3)
			pygame.draw.circle(self.surface, BLUE, self.center, 15, 3)
		else:
			pygame.draw.rect(self.surface, PURPLE, (0,0, TILE_WIDTH, TILE_HEIGHT))

			
		self.win.blit(self.surface, self.rect)
	def setIgnore(self,ignore):
		self.ignore = ignore

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
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()
		
		self.scale = scale
		self.image = pygame.transform.scale(img, self.scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

	def update_image(self, img):
		self.image = pygame.transform.scale(img, self.scale)

	def draw(self, win):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		win.blit(self.image, self.rect)
		return action
        
class Keyboard():
	def __init__(self):
		self.timeSinceLastKeyPress = 0

    

    