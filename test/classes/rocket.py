class rocketparameters: #ensure that the class name is different from the file or module name! Otherwise, Python gets confused
    
    #class constant 
    mass = 30 

    #class function, returning variables 
    def _init_(self,diameter): #define an initialisation or _init_ function that always take itself _self_ as the first parameter   #if only a method is used, no need to use return, othrewie use return for paratemers
        self.area = diameter*2
        return (self.area)  #must have return
       
    #class function, running a method 
    def rocket_greetings(self):
        print('Rocket says Hi')
        #no need to have return
    
        
    
