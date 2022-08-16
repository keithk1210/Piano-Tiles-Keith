import abc
import json
from pickle import MEMOIZE
import sys

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
        Tile.last_spawn_time = pygame.time.get_ticks()
        self.keyboard = keyboard
        self.song = song
    def update(self):
        for tile in self.screen.tiles:
            tile.update()
            last_chord = Tile.get_last_chord_index(self.song)
            last_chord_duration_in_ms = self.song.measures[last_chord[0]].chords[last_chord[1]].duration * (1/self.song.bpm) * 60 * 1000
            #print("last chord duration in ms: " + str(last_chord_duration_in_ms))
            #print("time since last tile spawn: " + str(pygame.time.get_ticks()- Tile.last_spawn_time))
            if pygame.time.get_ticks()- Tile.last_spawn_time >= last_chord_duration_in_ms: #if the tile has passed the threshold at the bottom of the screen spawn another one
                if len(self.song.measures[Tile.current_chord[0]].chords[Tile.current_chord[1]].notes) > 0 and Tile.current_chord[0] < len(self.song.measures) and Tile.current_chord[1] < len(self.song.measures[Tile.current_chord[0]].chords):
                    self.screen.tiles.append(create_tile(self.screen.surface,self.song.measures[Tile.current_chord[0]].chords[Tile.current_chord[1]],Tile.current_chord,self.song,True))
                    #print("TILE SPEED %f" % (Tile.speed))
                    Tile.last_spawn_time = pygame.time.get_ticks()
            if not tile.ignore and not tile.rest and tile.rect.top > HEIGHT: #if the player has not interacted with a certain tile and it has passed the threshold, then the player has lost
                self.game_state_manager.add_state(GameOverState(self.game_state_manager,self.screen.surface))
            if tile.rest:
                next_chord = self.keyboard.get_next_chord_index(self.song)
                next_rest_duration = self.song.measures[next_chord[0]].chords[next_chord[1]].duration * (1/self.song.bpm) * 60 * 1000
                if abs(HEIGHT - tile.rect.bottom) <= tile.speed/2 and pygame.time.get_ticks() - Tile.last_beat_update > next_rest_duration: #if a rest cross the threshold, still advance the song
                    self.keyboard.next_chord(self.song)
                    Tile.last_beat_update = pygame.time.get_ticks()
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
        

    def update(self):
        choice = None
        while choice == None or choice == "Settings":
            go_choices = ["Quit","Try Again!","Settings","Main Menu"]
            choice = easygui.buttonbox(msg="Game over!",choices = go_choices)
            if choice == go_choices[0]:
                sys.exit()
            elif choice == go_choices[1]:
                last_song = None
                for state in self.game_state_manager.states:
                    if isinstance(state,PlayingState):
                        last_song = state.song
                Tile.reset()
                self.game_state_manager.clear_states()
                self.game_state_manager.add_state(PlayingState(last_song,Screen(self.win),Keyboard(),self.game_state_manager))
            elif choice == go_choices[2]:
                self.game_state_manager.add_state(SettingsMenuState(self.game_state_manager))
    def event_loop_update(self, event):
        pass
    

class SettingsMenuState(GameState):

    TILE_HEIGHT_MULTIPLIER_Y_POS = 3
    BACK_Y_POS = 5

    def __init__(self, game_state_manager) -> None:
        super().__init__(game_state_manager)
        choice = None
        while choice != "Back":
            settings_choices = ["Change BPM","Change Tile Height","Back"]
            choice = easygui.buttonbox("What setting would you like to modify?",choices = settings_choices)
            if choice == settings_choices[0]:
                for state in game_state_manager.states:
                    if isinstance(state,PlayingState):
                        new_bpm = easygui.integerbox(msg="Enter new BPM. Original BPM = " + str(state.song.bpm),upperbound= None)
                        state.song.bpm = new_bpm
            elif choice == settings_choices[1]:
                mult = easygui.integerbox(msg="Enter Tile height multiplier:",upperbound=None)
                Tile.height_multiplier = mult
                bpm = None
                for state in game_state_manager.states:
                    if isinstance(state,PlayingState):
                        bpm = state.song.bpm
                Tile.speed = get_tile_speed(bpm,Tile.tile_height*mult)
                print("Tile height multiplier changed to: " + str(Tile.height_multiplier))
        game_state_manager.back_one_state()


    def update(self):
        pass
    
    def event_loop_update(self, event):
        pass

            
