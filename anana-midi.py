#!/usr/bin/env python3

import time

import serial
import pygame.midi

"""
My favourite MIDI programs for Anana:

* Glockenspiel
* Music Box
* Pipe Organ
* Voice Oohs
* French Horns
* Synth Brass 1
* Whistle
* Fantasia
* Crystal
* Fiddle
* JP Strings
* Org Bell
* Melted Choir
* MC-500 Beep
"""

NOTES = [31, 36, 38, 39, 60, 61, 62, 63, 64, 65, 66, 67] # MIDI note numbers for each channel
SERIAL_PORT = "/dev/ttyACM0" # path to the serial port used by the Arduino
MIDI_OUTPUT = 0 # index of the MIDI output device to use
CHANNEL_COUNT = 12 # number of capacitive touch channels

port = serial.Serial(SERIAL_PORT, 9600)

try:
    pygame.midi.init()
    player = pygame.midi.Output(MIDI_OUTPUT)
    previous_state = 0
    while True:
        line = port.readline().decode("utf-8")
        try: state = int(line.strip("\r\n"))
        except ValueError: continue # ignore bad lines
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