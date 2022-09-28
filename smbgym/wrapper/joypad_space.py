"""An environment wrapper to convert binary to discrete action space."""
import gym
from gym import Env
from gym import Wrapper

class JoypadSpace(Wrapper):
	"""An environment wrapper to convert binary to discrete action space"""

	# a mapping of buttons to binary values
	_button_map = {
		'right':  [1,0,0,0,0],
		'left':   [0,0,0,0,0],
		'down':   [0,0,0,0,0],
		'up':	 [0,0,0,0,0],
		'start':  [0,0,0,0,0],
		'select': [0,0,0,0,0],
		'B':	  [0,0,0,0,0],
		'A':	  [0,0,0,0,0],
		'NOOP':   [0,0,0,0,0],
	}

	def __init__(self, env: Env, actions: list):
		"""
		Initialize a new binary to discrete action space wrapper.
		Args:
			env: the environment to wrap
			actions: an ordered list of actions (as lists of buttons).
				The index of each button list is its discrete coded value
		Returns:
			None
		"""
		super().__init__(env)
		# create the new action space
		self.action_space = gym.spaces.Discrete(len(actions))
		# create the action map from the list of discrete actions
		self._action_map = {}
		self._action_meanings = {}
		# iterate over all the actions (as button lists)
		for action, button_list in enumerate(actions):
			# the value of this action's bitmap
			byte_action = 0
			# iterate over the buttons in this button list
			for button in button_list:
				byte_action |= self._button_map[button]
			# set this action maps value to the byte action value
			self._action_map[action] = byte_action
			self._action_meanings[action] = ' '.join(button_list)

	def step(self, action):
		env = self.env.step(self._action_map[action])
		return env

	def reset(self):
		"""Reset the environment and return the initial observation."""
		return self.env.reset()