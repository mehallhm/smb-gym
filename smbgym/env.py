from multiprocessing.dummy import Array
from typing import Tuple
from bridge import Bridge
import numpy as np
from helper.encode import encode
from py4j.java_gateway import JavaGateway
import gym

import time

class Env(gym.Env):
	"""
	Another environment for playing Super Mario Bros with OpenAI Gym

	Based on Gym Super Mario Bros (credit: Kautenja https://github.com/Kautenja) and Mario AI Framework (credit: amidos2006 https://github.com/amidos2006)
	You guys are awesome and this would not exist without you

	"""

	metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}


	def __init__(self, render_mode="human") -> None:
		self.bridge = Bridge(render_mode)

		self.bridge.set_level("/home/micha/Source/smb-gym/original/lvl-1.txt")
		self.bridge.initalize()

		# Observations are dictionaries with the agent's and the target's location.
		# Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
		# self.observation_space = gym.spaces.Box()

		# We have 4 actions, corresponding to "right", "up", "left", "down"
		self.action_space = gym.spaces.Discrete(5)

		"""
		The following dictionary maps abstract actions from `self.action_space` to 
		the direction we will walk in if that action is taken.
		Format: [right, speed, left, down, jump]
		"""
		self._action_to_direction = {
			0: np.array([1, 0, 0, 0, 0]),
			1: np.array([0, 1, 0, 0, 0]),
			2: np.array([0, 0, 1, 0, 0]),
			3: np.array([0, 0, 0, 1, 0]),
			4: np.array([0, 0, 0, 0, 1])
		}

		assert render_mode is None or render_mode in self.metadata["render_modes"]
		self.render_mode = render_mode
	
	def _encode_state(self, obs) -> list:
			conv = []
			for x, xl in enumerate(obs):
				conv.append([])
				for y, yp in enumerate(xl):
					conv[x].append(encode[obs[x][y]])
			return conv
			# conv = []
			# for cell in obs.flatten():
			# 	conv.append([])
			# 	conv[x].append(encode[obs[x][y]])
			# return conv
			# return obs
	
	def _get_observation(self) -> list:
		obs = self.bridge.get_observation()
		obs = self._encode_state(obs)
		return obs
	
	def _get_info(self) -> dict:
		return self.bridge.get_info()
	
	def _calculate_reward(self, info) -> float:
		pass

	def close(self) -> None:
		self.bridge.jvm.kill()
		self.bridge.close()

	def step(self, action) -> tuple[list, float, bool, bool, dict]:
		self.bridge.step(action)

		obs = self._get_observation()
		info = self._get_info()
		reward = self._calculate_reward(info)
		terminated = False

		return (
			obs,
			reward,
			terminated,
			False,
			info
		)

	def reset(self) -> tuple[list, float, bool, bool, dict]:
		self.bridge.set_level("/home/micha/Source/smb-gym/original/lvl-1.txt")
		self.bridge.reset()

		return (
			self._get_observation(),
			0,
			False,
			False,
			self._get_info()
		)

env = Env()
while True:
	env.step([1, 0, 0, 0, 0])
	info = env.bridge.get_info()
	print(info)
	if info['life'] == 0:
		info = env.reset()
		# break
	
# print(get_agent)

# while True:
# 	print(py4j.java_gateway.get_field(get_agent, 'action'))
# 	py4j.java_gateway.set_field(get_agent, 'action')