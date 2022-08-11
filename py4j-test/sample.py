from py4j.java_gateway import JavaGateway
import py4j

gateway = JavaGateway()                   # connect to the JVM


# random = gateway.jvm.java.util.Random()   # create a java.util.Random instance
# number1 = random.nextInt(10)              # call the Random.nextInt method
# number2 = random.nextInt(10)

# print(number1, number2)

# addition_app = gateway.entry_point               # get the AdditionApplication instance
bridge = gateway.entry_point


# value = addition_app.addition(number1, number2) # call the addition method

print(value)

field_value = py4j.java_gateway.get_field(addition_app, 'strange')
print(field_value)

gateway.shutdown()