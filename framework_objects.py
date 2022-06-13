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
    def clear_states(self):
        self.states = []

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
        self.screen_elements = []
        self.screen_elements.append(ImageScreenElement(len(self.screen_elements)+1,"piano.jpg",win))
        self.screen_elements.append(TextDisplay("PIANO TILES!",len(self.screen_elements)+1,self.win))
        self.screen_elements.append(Button("OPEN JSON FILE",len(self.screen_elements)+1,self.win,open_JSON_dir))
        self.screen_elements.append(Button("SETTINGS",len(self.screen_elements)+1,self.win,None))
    def update(self):

        for element in self.screen_elements:
            element.draw()
            if isinstance(element,Button):
                
                json_path = element.return_click_function_val()
                if json_path:
                    dict = {}
                    with open(json_path,"r") as openfile:
                        dict = json.load(openfile)
                    song = Song(dict["Info"][1][1],dict["Info"][0][1],None) 
                    Tile.speed = get_tile_speed(song.bpm,TILE_HEIGHT) #after the songs BPM has been figured out establish tile speed/AKA BPM
                    measures = []
                    for key in dict:
                        if key != "Info":
                            measures.append(dict[key])
                    
                    time_signature_denominator = float(dict["Info"][1][1][1]) #dict["Info"][1][1][1] this accesses the lower number of the time signature. for example, the 4 in 3/4
                    song.measures_readable = measures[0]
                    for i in range(0,len(song.measures_readable)):
                        song.measures.append(Measure(song.measures_readable[i]))
                    tile = createTile(self.win,song.measures_readable [0][1][0] * time_signature_denominator,[0,0],song)
                    self.game_state_manager.add_state(PlayingState(song,Screen([tile],self.win),Keyboard(),self.game_state_manager))
        return True

    def event_loop_update(self, event):
        return super().event_loop_update(event)

class PlayingState(GameState):
    def __init__(self,song,screen,keyboard,game_state_manager) -> None:
        super().__init__(game_state_manager)
        self.screen = screen
        self.keyboard = keyboard
        self.song = song
        
    def update(self):
        for tile in self.screen.tiles:
            tile.update()
            if pygame.time.get_ticks()- Tile.lastSpawnTime > NOTE_SPAWN_DELAY and abs(tile.rect.y) <= tile.speed/2: #if the tile has passed the threshold at the bottom of the screen spawn another one
                if len(self.song.measures[Tile.current_chord[0]].chords[Tile.current_chord[1]+1]) > 0 and Tile.current_chord[0] < len(self.song.measures) and Tile.current_chord[1]+1 < len(self.song.measures[Tile.current_chord[0]].chords):
                    #print("tile current beat %s" % (Tile.current_chord) )
                    self.screen.tiles.append(createTile(self.screen.surface,self.song.measures[Tile.current_chord[0]].chords[Tile.current_chord[1]+1][0] * self.song.timeSignature[1],Tile.current_chord,self.song,self.song.measures,self.keyboard))
                    Tile.lastSpawnTime = pygame.time.get_ticks()
            if not tile.ignore and tile.rect.top > HEIGHT: #if the player has not interacted with a certain tile and it has passed the threshold, then the player has lost
                self.game_state_manager.add_state(GameOverState(self.game_state_manager,self.screen.surface))
                return False
            if tile.rest and abs(HEIGHT - tile.rect.top) <= tile.speed/2 and pygame.time.get_ticks() - Tile.lastBeatUpdate > BEAT_UPDATE_DELAY: #if a rest cross the threshold, still advance the song
                self.keyboard.next_chord(self.song)
                Tile.lastBeatUpdate = pygame.time.get_ticks()
        return True
    def event_loop_update(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_w or event.key == pygame.K_e or event.key == pygame.K_r:
                    for tile in self.screen.tiles:
                        if tile.rect.bottom >= HEIGHT and tile.rect.top <= HEIGHT: #if the tile is near the bottom of the screen
                            if pygame.time.get_ticks() - self.keyboard.timeSinceLastKeyPress > KEY_PRESS_DELAY: #if enough time has passed
                                if not tile.ignore and self.keyboard.getCurrentBeat()[0] < len(self.song.measures) and self.keyboard.getCurrentBeat()[1] < len(self.song.measures[self.keyboard.getCurrentBeat()[0]].chords):
                                    if tile.horizontalPos == 0 and event.key == pygame.K_q:
                                        #print(self.song.measures[self.keyboard.getCurrentBeat()[0]].chords[self.keyboard.getCurrentBeat()[1]+1]) 
                                        tile.setIgnore(True)
                                        produceSound(self.song,self.keyboard.getCurrentBeat())
                                        self.keyboard.next_chord(self.song)
                                        self.keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
                                    elif tile.horizontalPos == 1 and event.key == pygame.K_w:
                                        #print(self.song.measures[self.keyboard.getCurrentBeat()[0]].chords[self.keyboard.getCurrentBeat()[1]+1])
                                        tile.setIgnore(True)
                                        produceSound(self.song,self.keyboard.getCurrentBeat())
                                        self.keyboard.next_chord(self.song)
                                        self.keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
                                    elif tile.horizontalPos == 2 and event.key == pygame.K_e:
                                        #print(self.song.measures[self.keyboard.getCurrentBeat()[0]].chords[self.keyboard.getCurrentBeat()[1]+1])
                                        tile.setIgnore(True)
                                        produceSound(self.song,self.keyboard.getCurrentBeat())
                                        self.keyboard.next_chord(self.song)
                                        self.keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()
                                    elif tile.horizontalPos == 3 and event.key == pygame.K_r:
                                       # print(self.song.measures[self.keyboard.getCurrentBeat()[0]].chords[self.keyboard.getCurrentBeat()[1]+1])
                                        tile.setIgnore(True)
                                        produceSound(self.song,self.keyboard.getCurrentBeat())
                                        self.keyboard.next_chord(self.song)
                                        self.keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()

class GameOverState(GameState):
    MAIN_MENU_Y_POS = 4
    def __init__(self,game_state_manager,win):
        super().__init__(game_state_manager)
        self.win = win
        self.screen_elements = []
        self.screen_elements.append(ImageScreenElement(len(self.screen_elements)+1,"gameover.jpg",self.win))
        self.screen_elements.append(TextDisplay("GAME OVER",len(self.screen_elements)+1,self.win))
        self.screen_elements.append(Button("RETRY?",len(self.screen_elements)+1,self.win,None))
        self.screen_elements.append(Button("MAIN MENU",len(self.screen_elements)+1,self.win,None))
    def update(self):
        for element in self.screen_elements:
            element.draw()
            if isinstance(element,Button): #is it a button?
                if element.y_pos == GameOverState.MAIN_MENU_Y_POS:
                    #this will clear the states stack and create a new main menu state
                    element.return_click_function_val(self.game_state_manager,MenuState(self.win,self.game_state_manager))

    def event_loop_update(self,event):
        pass

            

            
