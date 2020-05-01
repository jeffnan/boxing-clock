import time
from turtle import *
import os
import subprocess
import applescript

#Update with new GUI
#Should this be dynamic for any music player?
#Should I build function for the ringing?

class Round:
	"""
	A class used to represent a round of a workout.
	...
	Attributes
	----------
	minutes: int
		total minutes in the round
	seconds: int
		total seconds in the round
	color: str
		color to display on GUI for this round
	roundDuration: int
		total duration of the round in seconds
	"""
	def __init__(self, minutes, seconds, color):
		self.minutes = minutes
		self.seconds = seconds
		self.color = color
		self.roundDuration = (minutes * 60) + seconds

	def __repr__(self):
		#Shown when class is called
		return(f"Class: {self.__class__.__name__}, Minutes: {self.minutes}, Seconds: {self.seconds}, Color: {self.color}, RoundDuration: {self.roundDuration} seconds")

	def __str__(self):
		#Shown when using print()
		return(f"{self.__class__.__name__}({self.minutes}, {self.seconds}, {self.color})")

def play_pause():
	"""Tells Spotify to playpause"""
	playPauseScript = """tell app "Spotify" to playpause"""
	subprocess.call(['osascript', '-e', playPauseScript])

def get_player_state():
	"""Gets the current player state (if Spotify is playing or paused)"""
	currentMusicStateScript = """tell app "Spotify" to get player state"""
	currentMusicState = subprocess.run(['osascript', '-e', currentMusicStateScript], capture_output = True).stdout.decode('UTF-8').strip()
	return currentMusicState

def current_volume_script():
	"""Gets the current volume and returns it as a string/script"""
	currentVolScript = """output volume of (get volume settings)"""
	currentVol = int(subprocess.run(['osascript', '-e', currentVolScript], capture_output = True).stdout.decode('UTF-8'))
	normVolScript = """set volume output volume """ + str(currentVol)
	return normVolScript

def change_volume(volume: str):
	"""Changes volume to input volume"""
	subprocess.call(['osascript', '-e', volume])

def play_alarm():
	"""Plays alarm at max volume"""
	subprocess.call(['osascript', '-e', """set volume output volume 70"""])
	os.system('afplay /System/Library/Sounds/Blow.aiff')

def roundChangeAlarm(rings: int, normal_vol: str):
	"""Pauses music if music is playing, changes to max volume to ring alarm, sets volume back to normal and continues music"""
	if get_player_state() == 'paused':
		for _ in range(rings):
			play_alarm()
		change_volume(normal_vol)
	else:
		play_pause()
		for _ in range(rings):
			play_alarm()
		change_volume(normal_vol)
		play_pause()

def screenDisplay(colorDisplay: str, minutesDisplay: int, secondsDisplay: int, roundTime: int, t1: Turtle, t1Screen: Screen):
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

def main():
	normal_vol = current_volume_script()

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
		screenDisplay(boxing.color, boxing.minutes, boxing.seconds, boxing.roundDuration, t1, t1Screen)
		roundChangeAlarm(2, normal_vol)

		screenDisplay(speed.color, speed.minutes, speed.seconds, speed.roundDuration, t1, t1Screen)
		roundChangeAlarm(1, normal_vol)

		screenDisplay(rest.color, rest.minutes, rest.seconds, rest.roundDuration, t1, t1Screen)
		roundChangeAlarm(3, normal_vol)


if __name__ == "__main__":
	main()

# 1. Put most code into a function or class.
# 	- when interpreter encounters def or class keywords, it only stores those for later use and doesn't execute them until you tell it to
# 2. Use __name__ to control execution of your code.
# 3. Create a function called main() to contain the code you want to run.
# 4. Call other functions from main().




#__repr__ and __str__
#https://dbader.org/blog/python-repr-vs-str

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
