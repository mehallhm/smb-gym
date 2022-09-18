from multiprocessing.dummy import Array
from typing import Tuple
from bridge import Bridge
import numpy as np
from helper.encode import encode
from py4j.java_gateway import JavaGateway
import gym

import time

class Env:
	"""
	Another environment for playing Super Mario Bros with OpenAI Gym

	Based on Gym Super Mario Bros (credit: Kautenja https://github.com/Kautenja) and Mario AI Framework (credit: amidos2006 https://github.com/amidos2006)
	You guys are awesome and this would not exist without you

	"""

	monitor = False

	def __init__(self) -> None:
		self.bridge = Bridge()

		self.bridge.visuals = self.monitor
		self.bridge.set_level("/home/micha/Source/smb-gym/original/lvl-1.txt")
		self.bridge.initalize()
	
	def _encode_state(self) -> list:
			conv = []
			for x, xl in enumerate(self.state):
				conv.append([])
				for y, yp in enumerate(xl):
					conv[x].append(encode[self.state[x][y]])
			self.state = conv
			return conv

	def step(self, action) -> tuple[list, float, bool, bool, dict]:
		self.bridge.step(action)
		return (
			self.bridge._get_observation(),
			0,
			False,
			False,
			self.bridge.get_info()
		)

	def reset(self) -> tuple[list, float, bool, bool, dict]:
		self.bridge.gateway.shutdown()
		# self.bridge.root.kill()

		self.bridge = Bridge()

		self.bridge.visuals = self.monitor
		self.bridge.set_level("/home/micha/Source/smb-gym/original/lvl-1.txt")
		self.bridge.initalize()
		return (
			self.bridge._get_observation(),
			0,
			False,
			False,
			self.bridge.get_info()
		)

env = Env()
while True:
	env.step([1, 0, 0, 0, 0])
	info = env.bridge.get_info()
	if info['life'] == 0:
		env.reset()
		# import time
		# time.sleep(10)
		# break
	print(info)
	
# print(get_agent)

# while True:
# 	print(py4j.java_gateway.get_field(get_agent, 'action'))
# 	py4j.java_gateway.set_field(get_agent, 'action')