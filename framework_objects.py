import abc
import json
from pickle import MEMOIZE

import pygame
from objects import *

from utils import *
from resources import *


class GameStateManager:
    def __init__(self) -> None:
        self.states = []
    def add_state(self,state):
        self.states.append(state)
        #print("---")
        for state in self.states:
            print(state.__class__.__name__)
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
    OPEN_JSON_FILE_Y_POS = 3
    SETTINGS_Y_POS = 4
    def __init__(self,win,game_state_manager):
        super().__init__(game_state_manager)
        self.win = win
        self.screen_elements = []
        self.screen_elements.append(ImageScreenElement(len(self.screen_elements)+1,"piano.jpg",win)) 
        self.screen_elements.append(TextDisplay("PIANO TILES!",len(self.screen_elements)+1,self.win))
        self.screen_elements.append(Button("OPEN JSON FILE",len(self.screen_elements)+1,self.win,placeholder()))
        self.screen_elements.append(Button("SETTINGS",len(self.screen_elements)+1,self.win,placeholder()))
    def update(self):
        for element in self.screen_elements:
            element.draw()
    def event_loop_update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for element in self.screen_elements:
                if isinstance(element,Button) and element.rect.collidepoint(pygame.mouse.get_pos()):
                    if element.y_pos == MenuState.OPEN_JSON_FILE_Y_POS: #if the place where you clicked is located at a certain Y position
                        json_path = open_JSON_dir()
                        if json_path:
                            dict = {}
                            with open(json_path,"r") as openfile:
                                dict = json.load(openfile)
                            Tile.reset() #tile data has to be reset before a new song is made
                            song = Song(dict["Info"][1][1],dict["Info"][0][1],None) 
                            Tile.speed = get_tile_speed(song.bpm,Tile.tile_height) #after the songs BPM has been figured out establish tile speed/AKA BPM
                            measures = []
                            for key in dict:
                                if key != "Info":
                                    measures.append(dict[key])
                            
                            time_signature_denominator = float(dict["Info"][1][1][1]) #dict["Info"][1][1][1] this accesses the lower number of the time signature. for example, the 4 in 3/4
                            song.measures_readable = measures[0]
                            for i in range(0,len(song.measures_readable)):
                                song.measures.append(Measure(song.measures_readable[i]))
                            tile = create_tile(self.win,song.measures_readable [0][1][0],[0,0],song)
                            self.game_state_manager.add_state(PlayingState(song,Screen([tile],self.win),Keyboard(),self.game_state_manager))
                    elif element.y_pos == MenuState.SETTINGS_Y_POS: 
                        self.game_state_manager.add_state(SettingsMenuState(self.game_state_manager,self.win))

class PlayingState(GameState):
    def __init__(self,song,screen,keyboard,game_state_manager) -> None:
        super().__init__(game_state_manager)
        self.screen = screen
        self.screen.tiles.append(create_tile(self.screen.surface,song.measures[0].chords[0],[0,0],song,False))
        self.keyboard = keyboard
        self.song = song
    def update(self):
        for tile in self.screen.tiles:
            tile.update()
            if pygame.time.get_ticks()- Tile.lastSpawnTime > NOTE_SPAWN_DELAY and abs(tile.rect.y) <= tile.speed/2: #if the tile has passed the threshold at the bottom of the screen spawn another one
                if len(self.song.measures[Tile.current_chord[0]].chords[Tile.current_chord[1]].notes) > 0 and Tile.current_chord[0] < len(self.song.measures) and Tile.current_chord[1] < len(self.song.measures[Tile.current_chord[0]].chords):
                    self.screen.tiles.append(create_tile(self.screen.surface,self.song.measures[Tile.current_chord[0]].chords[Tile.current_chord[1]],Tile.current_chord,self.song,True))
                    print("TILE SPEED %f" % (Tile.speed))
                    Tile.lastSpawnTime = pygame.time.get_ticks()
            if not tile.ignore and tile.rect.top > HEIGHT: #if the player has not interacted with a certain tile and it has passed the threshold, then the player has lost
                self.game_state_manager.add_state(GameOverState(self.game_state_manager,self.screen.surface))
            if tile.rest and abs(HEIGHT - tile.rect.top) <= tile.speed/2 and pygame.time.get_ticks() - Tile.lastBeatUpdate > BEAT_UPDATE_DELAY: #if a rest cross the threshold, still advance the song
                self.keyboard.next_chord(self.song)
                Tile.lastBeatUpdate = pygame.time.get_ticks()
    def event_loop_update(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_w or event.key == pygame.K_e or event.key == pygame.K_r:
                    for tile in self.screen.tiles:
                        if tile.rect.bottom >= HEIGHT and tile.rect.top <= HEIGHT: #if the tile is near the bottom of the screen
                            if pygame.time.get_ticks() - self.keyboard.timeSinceLastKeyPress > KEY_PRESS_DELAY: #if enough time has passed
                                if not tile.ignore and not tile.rest and self.keyboard.get_current_chord()[0] < len(self.song.measures) and self.keyboard.get_current_chord()[1] < len(self.song.measures[self.keyboard.get_current_chord()[0]].chords):
                                    if tile.horizontalPos == 0 and event.key == pygame.K_q:
                                        self.play_sound(tile)
                                    elif tile.horizontalPos == 1 and event.key == pygame.K_w:
                                        self.play_sound(tile)
                                    elif tile.horizontalPos == 2 and event.key == pygame.K_e:
                                        self.play_sound(tile)
                                    elif tile.horizontalPos == 3 and event.key == pygame.K_r:
                                        self.play_sound(tile)
                                        
    def play_sound(self,tile):
        #might want to check if the the tile's chord and the keyboard chord line up!
        tile.setIgnore(True)
        self.screen.tiles.remove(tile)
        produce_sound(self.song,self.keyboard.get_current_chord())
        if self.keyboard.next_chord(self.song) == SONG_END_KEY:
            print("YOU DID IT!")
        self.keyboard.timeSinceLastKeyPress = pygame.time.get_ticks()


class GameOverState(GameState):
    MAIN_MENU_Y_POS = 4
    def __init__(self,game_state_manager,win):
        super().__init__(game_state_manager)
        self.win = win
        self.screen_elements = []
        self.screen_elements.append(ImageScreenElement(len(self.screen_elements)+1,"gameover.jpg",self.win))
        self.screen_elements.append(TextDisplay("GAME OVER",len(self.screen_elements)+1,self.win))
        self.screen_elements.append(Button("RETRY?",len(self.screen_elements)+1,self.win,placeholder()))
        self.screen_elements.append(Button("MAIN MENU",len(self.screen_elements)+1,self.win,None))
    
    def update(self):
        for element in self.screen_elements:
            element.draw()
            

    def event_loop_update(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for element in self.screen_elements:
                if isinstance(element,Button) and element.rect.collidepoint(pygame.mouse.get_pos()): #is it a button?
                    if element.y_pos == GameOverState.MAIN_MENU_Y_POS:
                        #this will clear the states stack and create a new main menu state
                        element.return_click_function_val(self.game_state_manager,MenuState(self.win,self.game_state_manager))

class SettingsMenuState(GameState):

    TILE_HEIGHT_MULTIPLIER_Y_POS = 3
    BACK_Y_POS = 5

    def __init__(self, game_state_manager,win) -> None:
        super().__init__(game_state_manager)
        self.win = win
        self.screen_elements = []
        self.screen_elements.append(ImageScreenElement(len(self.screen_elements)+1,"settings_icon.png",self.win))
        self.screen_elements.append(TextDisplay("SETTINGS",len(self.screen_elements)+1,self.win))
        self.screen_elements.append(Button("TILE HEIGHT MULTIPLIER:",len(self.screen_elements)+1,self.win,placeholder()))
        self.screen_elements.append(TextDisplay(f"x{Tile.height_multiplier}",len(self.screen_elements)+1,self.win))
        self.screen_elements.append(Button("BACK",len(self.screen_elements)+1,self.win,placeholder()))

    def update(self):
        for element in self.screen_elements:
            element.draw()
    
    def event_loop_update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for element in self.screen_elements:
                if isinstance(element,Button) and element.rect.collidepoint(pygame.mouse.get_pos()):
                    if element.y_pos == SettingsMenuState.TILE_HEIGHT_MULTIPLIER_Y_POS:
                        Tile.next_multiplier_option()
                        update_text_on_text_display(self.screen_elements[3],f"x{Tile.height_multiplier}")
                    elif element.y_pos == SettingsMenuState.BACK_Y_POS:
                        self.game_state_manager.back_one_state()

            
