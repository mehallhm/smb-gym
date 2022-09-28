from py4j.java_gateway import JavaGateway
import py4j
import numpy as np
import sys
import os

class Bridge:
	"""
	A bridge between Python and the Java Mario Environment
	"""

	def __init__(self, visuals=False) -> None:
		self.visuals = visuals
		
		self._connect()
	
	def _connect(self) -> None:
		# self.gateway = JavaGateway(classpath="../lib/ai.jar" die_on_exit=True)
		path = os.path.abspath(r"./smbgym/lib/ap.jar")
		self.gateway = JavaGateway.launch_gateway(classpath=path, die_on_exit=True, redirect_stdout=sys.stdout, redirect_stderr=sys.stderr)
		self.root = self.gateway.jvm.PlayLevel()
		self.createGame()
	
	def createGame(self) -> None:
		if self.visuals == "human":
			self.root.initializeWithGraphics()
		else:
			self.root.initializeHeadless()

	def set_level(self, path) -> str:
		py4j.java_gateway.set_field(self.root, 'level', path)
		return path
	
	def initalize(self) -> None:
		self.agent = py4j.java_gateway.get_field(self.root, 'agent')
		self.game = py4j.java_gateway.get_field(self.root, 'game')

		self.world = py4j.java_gateway.get_field(self.game, "world")
		self.mario = py4j.java_gateway.get_field(self.world, "mario")

		self.game.step()

	
	def reset(self) -> None:
		self.createGame()
		self.initalize()

	def step(self, action) -> None:
		self.register_inputs(action)
		self.game.step()

	def _get_coins(self):
		"""
		Get the number of coins collected
		"""
		return py4j.java_gateway.get_field(self.world, "coins")

	def _get_lives(self):
		"""
		Get the number of remaining lives
		"""
		lives = py4j.java_gateway.get_field(self.world, "lives")
		if self._get_game_status() == "LOSE":
			lives -= 1
		return lives

	def _get_XY(self):
		"""
		Get the X and Y pos of Mario
		"""
		x = py4j.java_gateway.get_field(self.mario, "x")
		y = py4j.java_gateway.get_field(self.mario, "y")
		return (x, y)
	
	def _get_game_status(self):
		"""
		Get the status of the game (RUNNING, WIN, LOSE, TIME_OUT)
		"""
		return str(py4j.java_gateway.get_field(self.world, "gameStatus"))
	
	def _flag_get(self):
		"""
		Returns a Boolean on wheather the flag has been touched
		"""
		status = self._get_game_status()
		if status == "WIN":
			return True
		return False
	
	def _get_mario_status(self):
		"""
		Returns the status of Mario (fireball, big, small)
		"""
		large = py4j.java_gateway.get_field(self.mario, "isLarge")
		fire = py4j.java_gateway.get_field(self.mario, "isFire")
		if fire:
			return "fireball"
		elif large:
			return "big"
		else:
			return "small"
	
	def _get_time (self):
		return py4j.java_gateway.get_field(self.world, "currentTimer") / 1000

	def get_observation(self):
		xy = self._get_XY()
		x = xy[0]
		y = xy[1]
		return self.world.getMergedObservation(x, y)

	def shutdown(self) -> None:
		self.gateway.shutdown()
	
	def register_inputs(self, action):
		# [right, speed, left, down, jump]
		self.agent.clear()

		if action[0] == 1:
			self.agent.right()
		if action[1] == 1:
			self.agent.speed()
		if action[2] == 1:
			self.agent.left()
		if action[3] == 1:
			self.agent.down()
		if action[4] == 1:
			self.agent.jump()
	
	def get_human_observation(self):
		"""
		Returns an observation 
		"""
		screen = self.get_observation()
		screen = np.array(screen)
		return np.flip(np.rot90(screen, 1, (0,1)), 0)
	
	def get_info(self):
		"""
		Returns a Dictionary of information from the environment
		"""
		xy = self._get_XY()
		return dict(
			coins = self._get_coins(),
			flag_get = self._flag_get(),
			life = self._get_lives(),
			score = 0,
			stage = 0,
			status = self._get_mario_status(),
			time = self._get_time(),
			world = 0,
			x = xy[0],
			y = xy[1]
		)