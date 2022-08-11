from py4j.java_gateway import JavaGateway
import py4j

gateway = JavaGateway()

agent = gateway.entry_point
agent.play()

# print(py4j.java_gateway.get_field(agent, 'agent'))