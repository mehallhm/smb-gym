from py4j.java_gateway import JavaGateway
import py4j

class Env:
	"""
	Another environment for playing Super Mario Bros with OpenAI Gym

	Based on Gym Super Mario Bros (credit: Kautenja https://github.com/Kautenja) and Mario AI Framework (credit: amidos2006 https://github.com/amidos2006)
	You guys are awesome and this would not exist without you
	
	"""

	# the legal range of rewards for each step
	reward_range = (-15, 15)
	
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
		return py4j.java_gateway.get_field(self.world, "coins")

	def _get_lives(self):
		return py4j.java_gateway.get_field(self.world, "lives")

	def _get_XY(self):
		x = py4j.java_gateway.get_field(self.mario, "x")
		y = py4j.java_gateway.get_field(self.mario, "y")
		return (x, y)

	def _get_info(self):
		xy = self._get_XY()
		return dict(
			coins = self._get_coins(),
			lives = self._get_lives(),
			x = xy[0],
			y = xy[1]
		)

	def getCombinedObservation(self, x, y, world_detail=1, enemy_detail=1):
		return self.world.getMergedObservation(x, y, world_detail, enemy_detail)

env = Env()

# tacky gameloop
while True:
	inp = input("Action: ")

	info = env._get_info()
	print(info)

	screen = env.getCombinedObservation(info["x"], info["y"])

	print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
	  for row in screen]))


	if inp == "l":
		env.agent.left()
	elif inp == "r":
		env.agent.right()
	elif inp == "d":
		env.agent.down()
	elif inp == "s":
		env.agent.speed()
	elif inp == "j":
		env.agent.jump()
	elif inp == "q":
		break

	env.game.step()
	inp = None
	env.agent.clear()

# print(get_agent)

# while True:
# 	print(py4j.java_gateway.get_field(get_agent, 'action'))
# 	py4j.java_gateway.set_field(get_agent, 'action')



"""Static action sets for binary to discrete action space wrappers."""


# actions for the simple run right environment
RIGHT_ONLY = [
    ['NOOP'],
    ['right'],
    ['right', 'A'],
    ['right', 'B'],
    ['right', 'A', 'B'],
]


# actions for very simple movement
SIMPLE_MOVEMENT = [
    ['NOOP'],
    ['right'],
    ['right', 'A'],
    ['right', 'B'],
    ['right', 'A', 'B'],
    ['A'],
    ['left'],
]


# actions for more complex movement
COMPLEX_MOVEMENT = [
    ['NOOP'],
    ['right'],
    ['right', 'A'],
    ['right', 'B'],
    ['right', 'A', 'B'],
    ['A'],
    ['left'],
    ['left', 'A'],
    ['left', 'B'],
    ['left', 'A', 'B'],
    ['down'],
    ['up'],
]