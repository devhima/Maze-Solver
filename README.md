# Maze-Solver

Maze Solver using reinforcement learning - By. Ibrahim Said Elsharawy (www.devhima.tk)

Reinforcement learning (RL) is an area of machine learning concerned with how software agents ought to take actions in an environment so as to maximize some notion of cumulative reward. So it's basically trial-and-error learning. 
The agent tries different actions in different situations and gets rewarded or punished for its actions. Over time, it figures out which actions in which situations leads to more reward.
AI researchers are interested in reinforcement learning because agents can __program__ themselves through this process of trial and error. All that is needed is a simulation environment in which the agent can try over and over, thousands of millions of times.
One of the reasons agent like reinforcement learning is because it can learn to behave in environments that have some randomness to them. The challenge of reinforcement learning: choose an action given that it doesn't know exactly what will happen once it performs it.
While learning by trial and error it is sometimes making random actions in the hope of stumbling on something good, but not knowing whether it got lucky with the random move or whether it is really a good move to do all the time.

Reinforcement learning solves a type of problem called a Markov Decision Process (MDP).
This just means that the optimal action can be determined by only looking at the current situation the agent is in. A MDP is made up of:

- States: a state is an unique configuration of the environment.
- Actions: all the things the agent can do.
- Transition function: This tells the agent the probability of ending up in a particular state when executing a particular action from another state.
- Reward function: This tells the agent how many points the agent gets for being in a particular state, or for performing a particular action in a particular state.

When reinforcement learning is performed, the agent creates what is called a policy. The policy simply indicates which action should be performed in each state. It is a look-up table. Reinforcement learning agents are fast, once training is complete.

Here is some screenshots from the __Controller.py__ file: 

- Here you can set main properties for the simulation:

![img1](https://github.com/devhima/Maze-Solver/raw/master/Images/IMG_20190301_025913.jpg)

- This is where learning happens:

![img2](https://github.com/devhima/Maze-Solver/raw/master/Images/IMG_20190301_025817.jpg)

- This is where our agent executing policy:

![img2](https://github.com/devhima/Maze-Solver/raw/master/Images/IMG_20190301_025827.jpg)
