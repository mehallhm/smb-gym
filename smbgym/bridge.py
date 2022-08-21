from py4j.java_gateway import JavaGateway
import py4j
import numpy as np

class Bridge:
	"""
	A bridge between Python and the Java Mario Environment
	"""
	def __init__(self) -> None:
		gateway = JavaGateway()

		self.root = gateway.entry_point
		self.root.initialize()

		self.agent = py4j.java_gateway.get_field(self.root, 'agent')
		self.game = py4j.java_gateway.get_field(self.root, 'game')

		self.world = py4j.java_gateway.get_field(self.game, "world")
		self.mario = py4j.java_gateway.get_field(self.world, "mario")
	
	def register_inputs(self):
		pass

	def _get_coins(self):
		"""
		Get the number of coins collected
		"""
		return py4j.java_gateway.get_field(self.world, "coins")

	def _get_lives(self):
		"""
		Get the number of remaining lives
		"""
		return py4j.java_gateway.get_field(self.world, "lives")

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

	def _get_info(self):
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
			time = 0,
			world = 0,
			x = xy[0],
			y = xy[1]
		)

	def get_combined_observation(self, x, y, world_detail=1, enemy_detail=1):
		return self.world.getMergedObservation(x, y, world_detail, enemy_detail)
	
	def return_human_observation(self, x, y):
		"""
		Returns a human readable observation
		"""
		screen = self.get_combined_observation(x, y)
		screen = np.array(screen)
		return np.flip(np.rot90(screen, 1, (0,1)), 0)