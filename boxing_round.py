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
		return(f"Class: {self.__class__.__name__}, Minutes: {self.minutes}, Seconds: {self.seconds}, Color: {self.color}, RoundDuration: {self.roundDuration} seconds")

	def __str__(self):
		return(f"{self.__class__.__name__}({self.minutes}, {self.seconds}, {self.color})")
