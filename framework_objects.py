import abc
import json
from pickle import MEMOIZE

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
    def __init__(self, game_state_manager) -> None:
        self.game_state_manager = game_state_manager
        pass
    @abc.abstractmethod
    def update(self):
        pass
    @abc.abstractmethod
    def event_loop_update(self,event):
        pass

class MenuState(GameState):
    def __init__(self,win,game_state_manager):
        super().__init__(game_state_manager)
        self.win = win
        self.buttons = []
        self.buttons.append(Button(BUTTON_X,
        BUTTON_HEIGHT + (BUTTON_HEIGHT * .5),"Open JSON File",open_JSON_dir))
    def update(self):
        for button in self.buttons:
            json_path = button.draw(self.win)
            if json_path:
                print(json_path)
                dict = {}
                with open(json_path,"r") as openfile:
                    dict = json.load(openfile)
                song = Song(dict["Info"][1],dict["Info"][0],None)
                measures = []
                for key in dict:
                    if key != "Info":
                        measures.append(dict[key])
                
                time_signature_denominator = float(dict["Info"][1][1][1]) #dict["Info"][1][1][1] this accesses the lower number of the time signature. for example, the 4 in 3/4
                song.measuresReadable = measures[0]
                print(song.measuresReadable[0][1][0])
                tile = createTile(self.win,song.measuresReadable[0][1][0] * time_signature_denominator,[0,0])
                self.game_state_manager.add_state(PlayingState(song,Screen([tile],self.win),Keyboard(),self.game_state_manager))

    def event_loop_update(self, event):
        return super().event_loop_update(event)

class PlayingState(GameState):
    def __init__(self,song,screen,keyboard,game_state_manager) -> None:
        super().__init__(game_state_manager)
        self.screen = screen
        self.keyboard = keyboard
        self.song = song
        self.measures = []
        for i in range(0,len(song.measuresReadable)):
            self.measures.append(Measure(song.measuresReadable[i]))
        for i in range(0,len(self.measures)):
            print(self.measures[i].chords)
    def update(self):
        for tile in self.screen.tiles:
            tile.update()
            print(Tile.currentBeat)
            if pygame.time.get_ticks()- Tile.lastSpawnTime > NOTE_SPAWN_DELAY and abs(tile.rect.y) <= tile.speed/2: #if the tile has passed the threshold at the bottom of the screen spawn another one
                self.screen.tiles.append(createTile(self.screen.surface,self.measures[Tile.currentBeat[0]].chords[Tile.currentBeat[1]] * self.song.timeSignature[1],Tile.currentBeat,self.notes,self.keyboard))
                Tile.lastSpawnTime = pygame.time.get_ticks()
            if not tile.ignore and tile.rect.top > HEIGHT: #if the player has not interacted with a certain tile and it has passed the threshold, then the player has lost
                #print(tile.rect.y)
                #print(tile)
                running = False
                print("You lose!")
            if tile.rest and abs(HEIGHT - tile.rect.top) <= tile.speed/2 and pygame.time.get_ticks() - Tile.lastBeatUpdate > BEAT_UPDATE_DELAY: #if a rest cross the threshold, still advance the song
                self.keyboard.nextBeat()
                Tile.lastBeatUpdate = pygame.time.get_ticks()
    def event_loop_update(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_w or event.key == pygame.K_e or event.key == pygame.K_r:
                    for tile in self.screen.tiles:
                        if tile.rect.bottom >= HEIGHT and tile.rect.bottom <= HEIGHT + tile.height: #if the tile is near the bottom of the screen
                            if pygame.time.get_ticks() - self.keyboard.timeSinceLastKeyPress > KEY_PRESS_DELAY: #if enough time has passed
                                if not tile.ignore: #this is just to avoid unecessary stuff
                                    if tile.horizontalPos == 0 and event.key == pygame.K_q:
                                        print(self.song.measures[self.keyboard.getCurrentBeat()[0]][self.keyboard.getCurrentBeat()[1]])
                                        tile.setIgnore(True)
                                        produceSound(self.song.measures,self.keyboard.getCurrentBeat())
                                        self.keyboard.nextBeat()
                                        self.keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
                                    elif tile.horizontalPos == 1 and event.key == pygame.K_w:
                                        print(self.song.measures[self.keyboard.getCurrentBeat()[0]][self.keyboard.getCurrentBeat()[1]])
                                        tile.setIgnore(True)
                                        produceSound(self.song.measures,self.keyboard.getCurrentBeat())
                                        self.keyboard.nextBeat()
                                        self.keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
                                    elif tile.horizontalPos == 2 and event.key == pygame.K_e:
                                        print(self.song.measures[self.keyboard.getCurrentBeat()[0]][self.keyboard.getCurrentBeat()[1]])
                                        tile.setIgnore(True)
                                        produceSound(self.song.measures,self.keyboard.getCurrentBeat())
                                        self.keyboard.nextBeat()
                                        self.keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
                                    elif tile.horizontalPos == 3 and event.key == pygame.K_r:
                                        print(self.song.measures[self.keyboard.getCurrentBeat()[0]][self.keyboard.getCurrentBeat()[1]])
                                        tile.setIgnore(True)
                                        produceSound(self.song.measures,self.keyboard.getCurrentBeat())
                                        self.keyboard.nextBeat()
                                        self.keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
            

            
