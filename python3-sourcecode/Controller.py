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

import sys
from Observation import *
from Reward import *
from Action import *
from Agent import *
from Environment import *
import numpy
import copy


# Training episodes;
episodes = 700

trainingReportRate = 700

# How many memories can the agent have?
numMemories = 1

# Reverie mode is false by default
reverie = False

# Retrain the agent after reverie?
retrain = False

#Max reward received in any iteration
maxr = None

# Set up environment for initial training
gridEnvironment = Environment()
gridEnvironment.verbose = False

# Set up agent
gridAgent = Agent(gridEnvironment)
gridAgent.verbose = False

# This is where learning happens
for i in range(episodes):
	# Train
	gridAgent.agent_reset()
	gridAgent.qLearn(gridAgent.initialObs)
	# Test
	gridAgent.agent_reset()
	gridAgent.executePolicy(gridAgent.initialObs)
	# Report
	totalr = gridAgent.totalReward
	if maxr == None or totalr > maxr:
		maxr = totalr
	
	if i%(episodes/trainingReportRate) == 0:
		print("iteration:", i, "max reward:", maxr)


# Reset the environment for policy execution
gridEnvironment.verbose = True
gridAgent.verbose = True

# Make a number of memories. Also doubles as testing
print("---")
for i in range(numMemories):
	print("Execute Policy", i)
	gridAgent.agent_reset()
	gridAgent.executePolicy(gridAgent.initialObs)
	print("total reward", gridAgent.totalReward)
	gridAgent.memory.append(gridAgent.trace)
	print("---")


# Reverie mode
if reverie:
	# get agent ready to learn from memories
	gridAgent.lastAction=Action()
	gridAgent.lastObservation=Observation()

	gridAgent.verbose = True
	gridEnvironment.verbose = True

	# Replaying memories creates the value table that the agent would have if all it had to go on was the memories
	print("Replaying memories", len(gridAgent.memory))
	counter = 0
	print("---")
	for m in gridAgent.memory:
		obs = m[0][0].worldState
		print("Learn from memory", counter)
		print("init state", obs)
		gridEnvironment.startState = obs
		gridAgent.agent_reset()
		gridAgent.lastAction=Action()
		gridAgent.lastObservation=Observation()
		gridAgent.gridEnvironment = gridEnvironment
		gridAgent.initialObs = gridEnvironment.env_start()
		gridAgent.initializeInitialObservation(gridEnvironment)
		gridAgent.replayMemory(gridAgent.initialObs, m)
		# Report
		print("replay", counter, "total reward", gridAgent.totalReward)
		print("---")
		counter = counter + 1

	# Reset the environment for policy execution
	gridEnvironment = Environment()
	gridEnvironment.verbose = True

	gridAgent.gridEnvironment = gridEnvironment
	gridAgent.agent_reset()

	gridAgent.verbose = True


	# Test new v table
	print("---")
	for i in range(100):
		print("Execute Post-Reverie Policy", i)
		gridAgent.initialObs = gridEnvironment.env_start()
		gridAgent.initializeInitialObservation(gridEnvironment)
		gridAgent.agent_reset()
		gridAgent.executePolicy(gridAgent.initialObs)
		print("total reward", gridAgent.totalReward)
		gridAgent.memory.append(gridAgent.trace)
		print("---")


# Retrain the agent
if retrain:
	maxr = None
	for i in range(0):
		# Train
		gridAgent.agent_reset()
		gridAgent.qLearn(gridAgent.initialObs)
		# Test
		gridAgent.agent_reset()
		gridAgent.executePolicy(gridAgent.initialObs)
		# Report
		totalr = gridAgent.totalReward
		if maxr == None or totalr > maxr:
			maxr = totalr
		
		if i%(episodes/trainingReportRate) == 0:
			print("iteration:", i, "max reward:", maxr)

	# Reset the environment for policy execution
	gridEnvironment.verbose = True
	gridAgent.agent_reset()
	
	# Test new v table
	print("---")
	for i in range(numMemories):
		print("Execute Policy", i)
		gridAgent.initialObs = gridEnvironment.env_start()
		gridAgent.initializeInitialObservation(gridEnvironment)
		gridAgent.agent_reset()
		gridAgent.executePolicy(gridAgent.initialObs)
		print("total reward", gridAgent.totalReward)
		gridAgent.memory.append(gridAgent.trace)

# Print the best behavior
print("The best behavior is: ")
print("-------")
for act in range(len(gridAgent.trace)):
		print(gridEnvironment.actionToString(gridAgent.trace[act][1].actionValue))

