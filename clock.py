import time
import os
import subprocess
import applescript

from turtle import *

from boxing_round import Round

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
