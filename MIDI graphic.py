from resources import *
import pygame
import mido
import rtmidi

pygame.init()

BLACK = [  0,   0,   0]
WHITE = [255, 255, 255]
note_list = []
note_list_off = []

outport=mido.open_output()

SIZE = [380, 380]
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Python MIDI Program by Wilson Chao")
clock = pygame.time.Clock()
done = False

while done == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
    screen.fill(BLACK)
    msg = mido.Message('note_on', note = 0, velocity = 64)
    outport.send(msg)
    """
    for i in range(len(note_list)):
        pygame.draw.circle(screen, WHITE, note_list[i], 10)
        note_list[i][1] += 1
    pygame.display.flip()
    for i in range(len(note_list_off)):
        pygame.draw.circle(screen, BLACK, note_list_off[i], 10)
        note_list_off[i][1] += 1   
    clock.tick(200)
    """     
    
pygame.quit ()