import random
import copy
import sys
from Observation import *
from Reward import *
from Action import *


class Environment:

	# The grid world
	# 1 = walls
	# 4 = goal (non-terminal)
	# 5 = goal (terminal)
	map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				 [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
				 [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
				 [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
				 [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
				 [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
				 [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 5, 1, 1],
				 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
		   
	# The current state
	currentState = []

	# The previous state
	previousState = []
	
	# Hard-coded initial state (used unless randomStart = True)
	# 0: bot x
	# 1: bot y
	startState = [1, 1]
	
	# Amount of reward at the goal
	reward = 10.0
	
	# Amount of penalty
	penalty = -1.0

	# The execution trace
	trace = []

	# Incremented every step
	counter = 0

	# Randomly generate a start state
	randomStart = False
	
	randGenerator=random.Random()
	lastActionValue = -1

	# Print debuggin information
	verbose = False

	# 0 = up
	# 1 = down
	# 2 = left
	# 3 = right
	
	def validActions(self):
		resultArray = [0, 1, 2, 3]
		return resultArray
	
	# Get the name of the action
	def actionToString(self, act):
		if act == 0:
			return "GoUp"
		elif act == 1:
			return "GoDown"
		elif act == 2:
			return "GoLeft"
		elif act == 3:
			return "GoRight"


	# Called to start the simulation
	def env_start(self):
		# Use hard-coded start state or randomly generated state?
		if self.randomStart:
			self.currentState = self.randomizeStart(self.map)
		else:
			self.currentState = self.startState[:]

		# Make sure counter is reset
		self.counter = 0

		if self.verbose:
			print "env_start", self.currentState

		# Reset previous state
		self.previousState = []

		# Get the first observation
		returnObs=Observation()
		returnObs.worldState=self.currentState[:]
		returnObs.availableActions = self.validActions()
		return returnObs

	# This creates a random initial state
	# Agent will not be placed on a wall
	def randomizeStart(self, map):
		bot = []
		while True:
			bot = [1, 1]
			if map[bot[1]][bot[0]] != 1:
				break
		state = bot
		return state

	# Update world state based on agent's action
	def env_step(self,thisAction):
		# Store previous state
		self.previousState = self.currentState[:]
		# Execute the action
		self.executeAction(thisAction.actionValue)

		# Get a new observation
		lastActionValue = thisAction.actionValue
		theObs=Observation()
		theObs.worldState=self.currentState[:]
		theObs.availableActions = self.validActions()
		
		# Check to see if agent entered a terminal state
		theObs.isTerminal = self.checkTerminal()
		
		if self.verbose:
			print "bot state:", self.currentState

		# Calculate the reward
		rewardValue = self.calculateReward(lastActionValue)
		reward = Reward(rewardValue)

		return theObs, reward

        
	# reset the environment
	def env_reset(self):
		# use random start or hard-coded start state?
		if self.randomStart:
			self.currentState = self.randomizeStart(self.map)
		else:
			self.currentState = self.startState[:]


	# Is agent in a terminal state?
	def checkTerminal(self):
		if self.map[self.currentState[1]][self.currentState[0]] == 5:
			return True
		#elif self.currentState[2] == False and self.map[self.currentState[4]][self.currentState[3]] == 2:
		#	# button working and agent is pressing it
		#	return True
		else:
			return False

	# Agent executes an action, update the state
	def executeAction(self, theAction):
		newpos = [self.currentState[0], self.currentState[1]]
		if (theAction == 0):#Move Up
			if self.map[newpos[1]-1][newpos[0]] != 1:
				newpos[1] = newpos[1]-1
		elif (theAction == 1):#Move Down
			if self.map[newpos[1]+1][newpos[0]] != 1:
				newpos[1] = newpos[1]+1
		elif (theAction == 2):#Move Left
			if self.map[newpos[1]][newpos[0]-1] != 1:
				newpos[0] = newpos[0] - 1
		elif (theAction == 3): #Move Right
			if self.map[newpos[1]][newpos[0]+1] != 1:
				newpos[0] = newpos[0] + 1
		self.currentState[0] = newpos[0]
		self.currentState[1] = newpos[1]
		

	# What reward should the agent get?
	def calculateReward(self, theAction):
		r = 0
		if self.map[self.currentState[1]][self.currentState[0]] == 5:
			r = r + self.reward
		elif self.map[self.currentState[1]][self.currentState[0]] == 4:
			r = r + self.reward
		else:
			r = r + self.penalty
		if self.verbose:
			print "reward", r
		return r





##########################################

if __name__=="__main__":
	EnvironmentLoader.loadEnvironment(environment())