import abc

import pygame

from utils import *
from resources import *

class GameStateManager:
    def __init__(self) -> None:
        self.states = []
    def add_state(self,state):
        self.states.append(state)
    def back_one_state(self):
        self.states.pop()
    def peek(self):
        return self.states[len(self.states)-1]

class GameState(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        pass
    @abc.abstractmethod
    def update(self):
        pass
    @abc.abstractmethod
    def event_loop_update(self,event):
        pass

class MenuState(GameState):
    def __init__(self,win):
        self.win = win
        self.buttons = []
        self.buttons.append(Button(BUTTON_X,BUTTON_HEIGHT + (BUTTON_HEIGHT * .5),"Open JSON File to Play",open_JSON_dir))
    def update(self):
        for button in self.buttons:
            if button.draw(self.win):
                print("button clicked")
    def event_loop_update(self, event):
        return super().event_loop_update(event)

class PlayingState(GameState):
    def __init__(self,song,screen,keyboard) -> None:
        super().__init__()
        self.screen = screen
        self.self.keyboard = self.keyboard
        self.song = song
    def update(self):
        for tile in self.screen.tiles:
            tile.update()
            if pygame.time.get_ticks()- Tile.lastSpawnTime > NOTE_SPAWN_DELAY and abs(tile.rect.y) <= tile.speed/2:
                self.screen.tiles.append(createTile(self.screen.surface,notes[Tile.currentBeat][0] * self.song.timeSignature[1],Tile.currentBeat,notes,self.keyboard))
                Tile.lastSpawnTime = pygame.time.get_ticks()
            if not tile.ignore and tile.rect.top > HEIGHT:
                print(tile.rect.y)
                print(tile)
                running = False
                print("You lose!")
            if tile.rest and abs(HEIGHT - tile.rect.top) <= tile.speed/2 and pygame.time.get_ticks() - Tile.lastBeatUpdate > BEAT_UPDATE_DELAY:
                self.keyboard.nextBeat()
                Tile.lastBeatUpdate = pygame.time.get_ticks()
    def event_loop_update(self,event):
        notes = []
        if event.key == pygame.K_q or event.key == pygame.K_w or event.key == pygame.K_e or event.key == pygame.K_r:
                for tile in self.screen.tiles:
                    if tile.rect.bottom >= HEIGHT and tile.rect.bottom <= HEIGHT + tile.height:
                        if pygame.time.get_ticks() - self.keyboard.timeSinceLastKeyPress > KEY_PRESS_DELAY:
                            if not tile.ignore:
                                if tile.horizontalPos == 0 and event.key == pygame.K_q:
                                    print(notes[self.keyboard.getCurrentBeat()])
                                    tile.setIgnore(True)
                                    produceSound(notes,self.keyboard.getCurrentBeat())
                                    self.keyboard.nextBeat()
                                    self.keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
                                elif tile.horizontalPos == 1 and event.key == pygame.K_w:
                                    print(notes[self.keyboard.getCurrentBeat()])
                                    tile.setIgnore(True)
                                    produceSound(notes,self.keyboard.getCurrentBeat())
                                    self.keyboard.nextBeat()
                                    self.keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
                                elif tile.horizontalPos == 2 and event.key == pygame.K_e:
                                    print(notes[self.keyboard.getCurrentBeat()])
                                    tile.setIgnore(True)
                                    produceSound(notes,self.keyboard.getCurrentBeat())
                                    self.keyboard.nextBeat()
                                    self.keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
                                elif tile.horizontalPos == 3 and event.key == pygame.K_r:
                                    print(notes[self.keyboard.getCurrentBeat()])
                                    tile.setIgnore(True)
                                    produceSound(notes,self.keyboard.getCurrentBeat())
                                    self.keyboard.nextBeat()
                                    self.keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
        

        
