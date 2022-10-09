from smbgym.bridge import Bridge
import numpy as np
from smbgym.helper.encode import encode
import gym
from os import path
import random

import time

class Env(gym.Env):
	"""
	Another environment for playing Super Mario Bros with OpenAI Gym

	Based on Gym Super Mario Bros (credit: Kautenja https://github.com/Kautenja) and Mario AI Framework (credit: amidos2006 https://github.com/amidos2006)
	You guys are awesome and this would not exist without you

	"""

	metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}


	def __init__(self, level_mode="random", render_mode="human") -> None:
		self.bridge = Bridge(render_mode)

		self.level_mode = level_mode
		self._set_level()

		self.bridge.initalize()

		info = self._get_info()
		self.mario_inital_x = info["x"]

		self.action_space = gym.spaces.Discrete(12)

		assert render_mode is None or render_mode in self.metadata["render_modes"]
		self.render_mode = render_mode

	def _set_level(self):
		dir_path = path.join(path.dirname(__file__), "../original")
		if self.level_mode == "random":
			num = random.randint(1, 15)
			level = path.join(dir_path, "./" + "lvl-" + str(num) + ".txt")
			self.bridge.set_level(level)
		else:
			level = path.join(dir_path, "./" + self.level_mode)
			self.bridge.set_level(level)
	
	def _encode_state(self, obs) -> list:
		indexer = np.array([encode.get(i, [0,0,0]) for i in range(0, 255)])
		return indexer[(obs)]
	
	def _get_observation(self) -> list:
		obs = self.bridge.get_observation()
		obs = self._encode_state(obs)
		return np.array(obs, dtype=np.uint8)
	
	def _get_info(self) -> dict:
		return self.bridge.get_info()
	
	def _calculate_reward(self, info) -> float:
		v = info["x"] - self.mario_inital_x
		t = -0.1
		d = 0
		if info["life"] == 0:
			d = -15
		
		r = v + t + d
		
		if -15 > r:
			r = -15
		if 15 < r:
			r = 15

		return r

	def close(self) -> None:
		if self.render_mode == "human":
			self.bridge.root.closeWindow()
		self.bridge.gateway.close()


	def step(self, action) -> tuple[list, float, bool, bool, dict]:

		self.bridge.step(action)

		obs = self._get_observation()
		info = self._get_info()
		reward = self._calculate_reward(info)
		if (info["flag_get"] == True or info["life"] == 0) or (info["time"] == 0):
			terminated = True
		else:
			terminated = False

		return (
			obs,
			reward,
			terminated,
			False,
			info
		)

	def reset(self) -> tuple[list, float, bool, bool, dict]:
		self._set_level()
		self.bridge.reset()

		return (
			self._get_observation(),
			self._get_info()
		)

if __name__ == "__main__":
	env = Env()
	while True:
		obs, reward, term, trunc, info = env.step([1, 0, 0, 0, 0])
		print(obs.shape)
		print(info)
		if info['life'] == 0:
			info = env.reset()
			break