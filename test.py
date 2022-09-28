import gym
from gym import spaces
import numpy as np

thing = spaces.Box(low=0, high=100, shape=(64, 64))
print(thing)