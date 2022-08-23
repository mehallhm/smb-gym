from bridge import Bridge
import numpy as np
from helper.encode import encode

import time

class Env():
	"""
	Another environment for playing Super Mario Bros with OpenAI Gym

	Based on Gym Super Mario Bros (credit: Kautenja https://github.com/Kautenja) and Mario AI Framework (credit: amidos2006 https://github.com/amidos2006)
	You guys are awesome and this would not exist without you

	"""

	def __init__(self) -> None:
		self.bridge = Bridge()
	
	def step(self, action) -> tuple:
		pass
	
	def _encode_state(self) -> np.ndarray:
		pass

	def reset(self) -> None:
		pass




env = Bridge()


def timer(func):
	def wrap(*args, **kwargs):
		start = time.time()
		func(*args, **kwargs)
		end = time.time()
		print(end - start)
	return wrap

# print(env.return_human_observation(info["x"], info["y"]))


@timer
def take_steps(steps):
	for letter in steps:
		if letter == "l":
			env.agent.left()
		elif letter == "r":
			env.agent.right()
		elif letter == "d":
			env.agent.down()
		elif letter == "s":
			env.agent.speed()
		elif letter == "j":
			env.agent.jump()
		elif letter == "q":
			break
		env.game.step()

	env.agent.clear()

take_steps("rrrrrrrrrr")

# print(get_agent)

# while True:
# 	print(py4j.java_gateway.get_field(get_agent, 'action'))
# 	py4j.java_gateway.set_field(get_agent, 'action')