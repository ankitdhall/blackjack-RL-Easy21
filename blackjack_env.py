import random
import numpy as np

DEBUG = False

class State:
	DEALER = 0
	PLAYER = 0

def draw():
	value = random.randint(1,10)
	if 3*random.uniform(0,1) < 1.0:
		value = value*-1
	return int(value)

# action {0: stick, 1: hit}
def step(state, action):
	global DEBUG

	if action == 1:
		x = draw()
		state.PLAYER = state.PLAYER + x
		
		if DEBUG:
			print "player drew:", x
			print "D  P"
			print state.DEALER, state.PLAYER

		if state.PLAYER < 1 or state.PLAYER > 21:
			if DEBUG:
				print "player lost"
			return "terminal", -1.0

		else:
			return state, 0.0

	elif action == 0:
		while state.DEALER < 17:
			x = draw()
			state.DEALER = state.DEALER + x

			if state.DEALER < 1 or state.DEALER > 21:
				if DEBUG:
					print "player WON"
				return "terminal", 1.0

		if DEBUG:
			print "dealer drew:"
			print "D  P"
			print state.DEALER, state.PLAYER

		if state.PLAYER > state.DEALER:
			if DEBUG:
					print "player WON"
			return "terminal", 1.0
		elif state.DEALER > state.PLAYER:
			if DEBUG:
				print "player lost"
			return "terminal", -1.0
		else:
			if DEBUG:
				print "game drew"
			return "terminal", 0.0

