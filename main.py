from math import prod
from tracemalloc import start
from mido import MidiFile
from numpy import append
from pygame import *
from framework_objects import *
from utils import *
import os
import xml.etree.ElementTree as ET
from processing import *

import pygame
import sys
import time as pytime

#TO DO:

#improve playability
    #the window to make a note sound is too short
    #add a menu and something that lets you restart the level
    #game over screen
        #TO DO 
            #main menu button on gameover screen just doenst work sometimes - seems to consistently take 2 clicks to work
    #issues arise near the end of a song for some reason 
    #slows down after a while
#make it look better
    #victory screen
        #apparently i need to fix my song creator first - random empty arrays at the end of jingle bells


#Fix unsavory code
    #clean up CreateTile method
    #make everything snake_case
    #lots of redundant code in the event update loop for the playing state



#game states

#font



appdata = os.getenv("APPDATA")
parent_dir = "XMLtoJSONConverter"
output_dir = "output"
music_xml_dir = "MusicXMLs"
abs_parent_dir = appdata + "\\" + parent_dir
abs_music_xml_dir = abs_parent_dir + "\\" + music_xml_dir
abs_output_dir = abs_parent_dir + "\\" + output_dir


#creates directory if not existent yet
if not os.path.exists(abs_parent_dir):
    os.mkdir(abs_parent_dir)
if not os.path.exists(abs_output_dir):
    os.mkdir(abs_output_dir)
if not os.path.exists(abs_music_xml_dir):
    os.mkdir(abs_music_xml_dir)

xmls_in_dir = False

#checks to see if XML dir is empty
for file in os.listdir(abs_music_xml_dir):
    if (len(file.split(".")) >= 2):
        if (file.split('.')[1] == "musicxml"):
            xmls_in_dir = True

if not xmls_in_dir:
    easygui.msgbox("No .musicxml files were found in MusicXMLs directory. Please insert .musicxmml files in this folder: \n%s." % (abs_music_xml_dir))
    sys.exit()

button_list = ("Open XML directory")

userChoice = easygui.msgbox(msg="Welcome to Piano Tiles! Please select a MusicXML file to get started.")

music_xml_file_name = easygui.fileopenbox(msg="Please select a MusicXML file",default=abs_music_xml_dir + '\\*.musicxml',filetypes=["*.musicxml"])

tree = ET.parse(music_xml_file_name.replace("\\","\\\\"))
root = tree.getroot()
#song_name = easygui.enterbox("Enter the name of the JSON file you would like to create",title="Enter text")
song = Song(tree,"song")

#writeJSON(song)



#########################


pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((WIDTH,HEIGHT))
win.fill(WHITE)
pygame.display.set_caption("Piano Tiles")

notes = []
running = True
noteSpawnDT = 0
game_state_manager = GameStateManager()
playing_state = PlayingState(song,Screen(win),Keyboard(),game_state_manager)
game_state_manager.add_state(playing_state)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        game_state_manager.peek().event_loop_update(event) 
    game_state_manager.peek().update()
    clock.tick(FPS)
    pygame.display.update()
    win.fill(WHITE)

pygame.quit()

