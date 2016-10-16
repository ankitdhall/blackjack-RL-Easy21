import random
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

global LOST
LOST = 0

from blackjack_env import *

value = np.zeros((2, 11, 22))
counter = np.zeros((2, 11, 22))


def myround(a, decimals=2):
     return np.around(a-10**(-(decimals+5)), decimals=decimals)

def ALPHA(n):
	if DEBUG:
		print "ALPHA:", 1.0/n
	return 1.0/n

def EPSILON(n):
	if DEBUG:
		print "EPSILON:",100.0/(100.0 + n)
	return 100.0/(100.0 + n)

def MC():
	state = State()
	state.DEALER = random.randint(1,10)
	state.PLAYER = random.randint(1,10)
	if DEBUG:
		print "\n------- new game ---------"

	total_reward = 0
	visited = []

	while state!="terminal":
		if DEBUG:
			print "Dealer has:", state.DEALER
			print "Player has:", state.PLAYER

		if random.random() < EPSILON(np.sum(counter[:, state.DEALER, state.PLAYER], axis=0)):
			action = random.randint(0,1)
			if DEBUG:
				print "selected random action:", action
		else:
			action = np.argmax(value[:, state.DEALER, state.PLAYER])
			if DEBUG:
				print "selected argmax action:", action

		counter[action, state.DEALER, state.PLAYER]+=1
		visited.append((action, state.DEALER, state.PLAYER))

		if DEBUG:
			print "appending...", (action, state.DEALER, state.PLAYER)

		state, reward = step(state, action)
		total_reward += reward

	#print reward
	for action, dealer, player in visited:
		value[action, dealer, player] = value[action, dealer, player] + ALPHA(counter[action, dealer, player])*(total_reward - value[action, dealer, player])

	# keep count of all losses
	if total_reward == -1:
		return 1
	return 0

for i in range(1000000):
	if i%50000 == 0:
		print "\n-------------------------"
		print "In iteration: ", i
		print "Games LOST:", LOST*100.0/(0.00001 + i)
		#DEBUG = True
	
	LOST += MC()
	DEBUG = False



if DEBUG:
	for i in value:
		print "------------------------------------"
		for j in i:
			print myround(j)
			print ""


def plott():
	q = np.max(value, axis=0)
	print q
	# plot monte-carlo value func
	bestval = np.amax(value, axis=0)
	fig = plt.figure()
	ha = fig.add_subplot(111, projection='3d')
	x = range(10)
	y = range(21)
	X, Y = np.meshgrid(y, x)
	ha.plot_wireframe(X+1, Y+1, bestval[1:,1:])
	ha.set_ylabel("dealer starting card")
	ha.set_xlabel("player current sum")
	ha.set_zlabel("value of state")
	plt.show()

plott()
		