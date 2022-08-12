from py4j.java_gateway import JavaGateway
import py4j

gateway = JavaGateway()

root = gateway.entry_point
root.initialize()

agent = py4j.java_gateway.get_field(root, 'agent')
game = py4j.java_gateway.get_field(root, 'game')

# game.gameLoop(30)
while True:
	inp = input("Continue? ")
	if inp == "":
		game.step()
	inp = None

# print(get_agent)

# while True:
# 	print(py4j.java_gateway.get_field(get_agent, 'action'))
# 	py4j.java_gateway.set_field(get_agent, 'action')