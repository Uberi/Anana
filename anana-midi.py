#!/usr/bin/env python3

import time

import serial
import pygame.midi

"""
Glockenspiel
Music Box
Pipe Organ
Voice Oohs
French Horns
Synth Brass 1
Whistle
Fantasia
Crystal
Fiddle
JP Strings
Org Bell
Melted Choir
MC-500 Beep
"""

NOTES = [31, 36, 38, 39, 60, 61, 62, 63, 64, 65, 66, 67] # MIDI note numbers for each channel
NOTES = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59] # MIDI note numbers for each channel
NOTES = [62, 64, 66, 67, 69, 71, 72, 74, 56, 57, 58, 59] # MIDI note numbers for each channel
SERIAL_PORT = "/dev/ttyACM0"
CHANNEL_COUNT = 12

port = serial.Serial(SERIAL_PORT, 9600)

try:
    pygame.midi.init()
    player = pygame.midi.Output(0)
    previous_state = 0
    while True:
        state = int(port.readline().decode("utf-8").strip("\r\n"))
        for i in range(CHANNEL_COUNT):
            if (state >> i) & 1 != (previous_state >> i) & 1:
                print(state)
                if (state >> i) & 1:
                    player.note_on(NOTES[i], 127)
                else:
                    player.note_off(NOTES[i], 127)
        previous_state = state
except KeyboardInterrupt:
    del player
    pygame.midi.quit()