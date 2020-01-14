#!/usr/bin/env python3
import time
import sys
import os
import tty
import termios


# init
ttyfd = os.open(os.ttyname(sys.stdout.fileno()), os.O_RDWR)
old_settings = termios.tcgetattr(ttyfd)
os.write(1, "\033[?1047h".encode()) #switch screen buffer
tty.setraw(ttyfd) # raw tty needs no enter to read

#get HxW 
os.write(1, "\033[18t".encode()) #reports HxW to tty
response = os.read(ttyfd,0xFF) # read and parse it
_, h,w = response[2:-1].decode().split(";")
h = int(h)
w = int(w)

os.write(1, "\033[?25l".encode()) #hide cursor
os.write(1, "\033[2J".encode()) # clear screen


def disco(colour):
	os.write(1, f"\033[{colour}m".encode()) # colour coding
	os.write(1, f"\033[{h};1H".encode()) # move to bottom row
	os.write(1, (" "*w).encode()) # make spce line
	os.write(1, "\033[1;1H".encode()) # got top left
	for x in range(h-1):
		os.write(1, (" "*w+ "\r\n").encode()) # now write lines to second last

for x in range(10):
	disco(41)
	time.sleep(0.05)

	os.write(1, "\033[2J".encode()) # clear screen
	time.sleep(0.05)

	disco(42)
	time.sleep(0.05)

	disco(44)
	time.sleep(0.05)

	disco(47)
	time.sleep(0.05)


#finish
os.write(1, "\033[?1047l".encode()) # restore old scren buffer
termios.tcsetattr(ttyfd, termios.TCSADRAIN, old_settings) #restore old terminal settings

