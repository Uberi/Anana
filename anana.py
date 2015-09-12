#!/usr/bin/env python3

import time

import serial
import pygame

SERIAL_PORT = "/dev/ttyACM0"
CHANNEL_COUNT = 12

port = serial.Serial(SERIAL_PORT, 9600)

pygame.mixer.init()
sounds = [
    pygame.mixer.Sound("sounds/707 closed HH.wav"),
    pygame.mixer.Sound("sounds/707 crash cymbal.wav"),
    pygame.mixer.Sound("sounds/707 Dry Clap.wav"),
    pygame.mixer.Sound("sounds/707 Dry SD2.wav"),
    pygame.mixer.Sound("sounds/707 high tom.wav"),
    pygame.mixer.Sound("sounds/707 kick 1l.wav"),
    pygame.mixer.Sound("sounds/707 low tom.wav"),
    pygame.mixer.Sound("sounds/707 mid tom.wav"),
    pygame.mixer.Sound("sounds/707 opened HH.wav"),
    pygame.mixer.Sound("sounds/707 ride.wav"),
    pygame.mixer.Sound("sounds/707 sn1.wav"),
    pygame.mixer.Sound("sounds/707 sn2.wav"),
]

def on(index): sounds[index].play()
def off(index): sounds[index].fadeout(1000)

previous_state = 0
while True:
    line = port.readline().decode("utf-8")
    try: state = int(line.strip("\r\n"))
    except ValueError: continue # ignore bad lines
    for i in range(CHANNEL_COUNT):
        if (state >> i) & 1 != (previous_state >> i) & 1:
            print(state)
            if (state >> i) & 1: on(i)
            else: off(i)
    previous_state = state