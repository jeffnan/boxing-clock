import time
from turtle import *
import os
import subprocess
import applescript

#Update with new GUI
#Should this be dynamic for any music player?
#Should I build function for the ringing?

class Round:
	def __init__(self, minutes, seconds, color):
		self.minutes = minutes
		self.seconds = seconds
		self.color = color
		self.roundDuration = (minutes * 60) + seconds

playPauseScript = """tell app "Spotify" to playpause"""
currentMusicStateScript = """tell app "Spotify" to get player state"""

currentVolScript = """output volume of (get volume settings)"""
maxVolScript = """set volume output volume 100"""

def roundChangeAlarm(rings: int):
	"""Pauses music if music is playing, changes to max volume to ring alarm, sets volume back to normal and continues music"""
	currentVol = int(subprocess.run(['osascript', '-e', currentVolScript], capture_output = True).stdout.decode('UTF-8'))
	normVolScript = """set volume output volume """ + str(currentVol)
	currentMusicState = subprocess.run(['osascript', '-e', currentMusicStateScript], capture_output = True).stdout.decode('UTF-8').strip()

	if currentMusicState == 'paused':
		subprocess.call(['osascript', '-e', maxVolScript])
		for _ in range(rings):
		    os.system('afplay /System/Library/Sounds/Blow.aiff')
		subprocess.call(['osascript', '-e', normVolScript])
	else:
		subprocess.call(['osascript', '-e', playPauseScript])
		subprocess.call(['osascript', '-e', maxVolScript])
		for _ in range(rings):
		    os.system('afplay /System/Library/Sounds/Blow.aiff')
		subprocess.call(['osascript', '-e', normVolScript])
		subprocess.call(['osascript', '-e', playPauseScript])

def screenDisplay(colorDisplay: str, minutesDisplay: int, secondsDisplay: int, roundTime: int):
	"""Displays GUI with countdown clock"""
	t1Screen.bgcolor(colorDisplay)
	while roundTime > 0:
		t1.clear()
		t1.write(str(minutesDisplay).zfill(2) + ":" + str(secondsDisplay).zfill(2), font = ("arial", 100, "normal"), move = False, align = "center")
		time.sleep(1)
		if secondsDisplay == 0:
			minutesDisplay -= 1
			secondsDisplay = 60
		roundTime -= 1
		secondsDisplay -= 1

setup()
t1 = Turtle()

t1Screen = Screen()
t1.hideturtle()
t1Screen.setup(width=1.0, height=1.0)

minutesBoxing = int(t1Screen.numinput(title = "Boxing Round", prompt = "How many minutes would you like your boxing round to be?", default = None, minval = 0, maxval = 5))
secondsBoxing = int(t1Screen.numinput(title = "Boxing Round", prompt = "How many seconds would you like your boxing round to be?", default = None, minval = 0, maxval = 60))

minutesSpeed = int(t1Screen.numinput(title = "Speed Round", prompt = "How many minutes would you like your speed round to be?", default = None, minval = 0, maxval = 5))
secondsSpeed = int(t1Screen.numinput(title = "Speed Round", prompt = "How many seconds would you like your speed round to be?", default = None, minval = 0, maxval = 60))

minutesRest = int(t1Screen.numinput(title = "Rest", prompt = "How many minutes would you like your rest to be?", default = None, minval = 0, maxval = 5))
secondsRest = int(t1Screen.numinput(title = "Rest", prompt = "How many seconds would you like your rest to be?", default = None, minval = 0, maxval = 60))

numOfRounds = int(t1Screen.numinput(title = "Total Round", prompt = "How many round do you want to box for?", default = None, minval = 0, maxval = 20))

green = "#94f000"
yellow = "#f0e000"
red = "#ff0000"

boxing = Round(minutesBoxing, secondsBoxing, green)
speed = Round(minutesSpeed, secondsSpeed, yellow)
rest = Round(minutesRest, secondsRest, red)

for _ in range(numOfRounds):
	screenDisplay(boxing.color, boxing.minutes, boxing.seconds, boxing.roundDuration)
	roundChangeAlarm(2)

	screenDisplay(speed.color, speed.minutes, speed.seconds, speed.roundDuration)
	roundChangeAlarm(1)

	screenDisplay(rest.color, rest.minutes, rest.seconds, rest.roundDuration)
	roundChangeAlarm(3)

#GitHub
#https://towardsdatascience.com/getting-started-with-git-and-github-6fcd0f2d4ac6

# AppleScript
# https://alvinalexander.com/apple/itunes-applescript-examples-scripts-mac-reference/
# https://256stuff.com/gray/docs/misc/itunes_applescript_commands/
# https://dougscripts.com/itunes/itinfo/info03.php
# https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/introduction/ASLR_intro.html#//apple_ref/doc/uid/TP40000983-CH208-SW1

# Subprocess
# https://docs.python.org/3/library/subprocess.html

#Play aiff file
#https://ss64.com/osx/afplay.html

#Redo project with Tkinter/PyQT/any other GUI
#https://techsore.com/best-python-gui/
#https://medium.com/teamresellerclub/the-6-best-python-gui-frameworks-for-developers-7a3f1a41ac73
#https://dev.to/codesharedot/best-python-framework-for-building-a-desktop-application-and-gui-58n5
#https://techsore.com/best-python-gui/
