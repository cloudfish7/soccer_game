import pygame
import time

pygame.mixer.init()
pygame.mixer.music.load('./music/kick_sound.mp3')
pygame.mixer.music.play()

time.sleep(2)
