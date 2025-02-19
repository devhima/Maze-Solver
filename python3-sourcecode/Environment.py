'''
Maze Solver - using reinforcement learning.
by Dev. Ibrahim Said Elsharawy (www.devhima.tk)
'''

'''
MIT License

Copyright (c) 2019 Ibrahim Said Elsharawy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import copy
import sys
from Observation import *
from Reward import *
from Action import *
import subprocess as sp

class Environment:

	# The grid world
	# 1 = walls
	# 4 = goal (non-terminal)
	# 5 = goal (terminal)
	# 2 = start position
	startPosition = []
	map = []
	
	# Read map from maze file
	text_file = open("maze.txt", "r")
	lines = text_file.read().split('\n')
	xP = 0
	yP = 0
	for i in lines:
		yP = 0
		ml = i.split(' ')
		nml=[]
		for x in ml:
		    z=x.replace('\r','')
		    if z=='#':
			    z=1
		    if z=='2':
			    startPosition = [yP, xP]
			    z=0
		    z=int(z)
		    nml.append(z)
		    yP+=1
		map.append(nml)
		xP+=1
	
	# The current state
	currentState = []

	# The previous state
	previousState = []
	
	# Hard-coded initial state (get startPosition from maze file)
	startState = copy.deepcopy(startPosition)
	
	# Amount of reward at the goal
	reward = 10.0
	
	# Amount of penalty
	penalty = -1.0

	# The execution trace
	trace = []

	# Incremented every step
	counter = 0

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
		# Use hard-coded start state 
		self.currentState = self.startState[:]

		# Make sure counter is reset
		self.counter = 0

		if self.verbose:
			print("env_start", self.currentState)

		# Reset previous state
		self.previousState = []

		# Get the first observation
		returnObs=Observation()
		returnObs.worldState=self.currentState[:]
		returnObs.availableActions = self.validActions()
		return returnObs

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
			self.env_print(self.currentState)
			print("bot state:", self.currentState)
			

		# Calculate the reward
		rewardValue = self.calculateReward(lastActionValue)
		reward = Reward(rewardValue)

		return theObs, reward

        
	# reset the environment
	def env_reset(self):
		# use hard-coded start state?
		self.currentState = self.startState[:]


	# print the environment
	def env_print(self, agentState):
		sp.call('clear',shell=True)
		pX = 0
		pY = 0
		for i1 in self.map:
			pY = 0
			for i2 in i1:
				#print "(" + str(pX) + ", " + str(pY) + ")",
				if pX == agentState[1] and pY == agentState[0]:
					if i2 != 1:
						print("X ", end=' ')
				elif i2 == 1:
					print("# ", end=' ')
				else:
					if i2 == 0:
						print("  ", end=' ')
					else:
						print(str(i2) + " ", end=' ')
				pY+=1
			print("\n")
			pX+=1


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
			print("reward", r)
		return r





##########################################

if __name__=="__main__":
	EnvironmentLoader.loadEnvironment(environment())

