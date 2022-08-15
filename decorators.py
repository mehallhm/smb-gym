def gg(p):
	class Wrap1:
		def __init__(self, env):
			self.wrap = p(env)
		
		def call(self):
			print("1")

	return Wrap1

def decorate(cls):
	class Wrap:
		def __init__(self, x) -> None:
			self.wrap = cls(x)
		
		def call(self) -> None:
			print("Called!")
	
	return Wrap

# class Wrap2:
# 	def __init__(self, env) -> None:
# 		pass

# 	def call(self):
# 		print("2")

# @gg
# @Wrap2
@decorate
class Say:
	def __init__(self, y):
		pass


env = Say(1)
# say = Wrap1(say)
# say = Wrap2(say)
env.call()


# decorator accepts a class as 
# a parameter
def decorator(cls):
      
    class Wrapper:
          
        def __init__(self, x):
              
            self.wrap = cls(x)
              
        def get_name(self):
              
            # fetches the name attribute
            return self.wrap.name
          
    return Wrapper
  
@decorator
class C:
    def __init__(self, y):
        self.name = y
  
# its equivalent to saying
# C = decorator(C)
i = C("Geeks")
print(i.get_name())   