from rocket import rocketparameters



#calling a const/variable from a class
b = rocketparameters.mass*2
print(b) #testing works


#calling a function from a class
rocket_Ares = rocketparameters()  #first, define the object using the class 
diameter = rocketparameters._init_(rocket_Ares,50) #once object is defined, its own (self) instances can be inputted as the first parameter in every function. The object_name (in main program) replaces self (as written in class))
print(diameter) #testing works

#calling a method from class
rocket_nuna = rocketparameters()
rocketparameters.rocket_greetings(rocket_nuna) #testing works