#treat this file as a blackbox
#def Define_Aircraft():
    
import pandas as pd
f = pd.read_excel('Parametric_Aircraft_Model.xlsx', sheet_name= "Aircraft",dtype={'Aircraft_Parameter': str, 'Aircraft_Parameter_Value': float}, engine='openpyxl')
#print(f, type(f)) #testing #works #pandas imports excel workbook as a dataframe
'''
    #print(f.iloc[2]) #testing works
    
    #print(f.loc[2,'Aircraft_Parameter']) #testing works
    #print(f.iloc[2,'Aircraft_Parameter']) #testing does not work
    
    #loc and iloc difference:
    #iloc refers to index of datafram, while loc refers to item in dataframe
'''    
    
for i in range(0, len(f)):
    value = f.iloc[i]['Aircraft_Parameter_Value']
    var_name = f.iloc[i]['Aircraft_Parameter']
    #print(var_name, value, type(var_name), type(value)) #testing works
    #exec("%s = %d" % (var_name,value)) #works but only returns integer values
    globals()[var_name] = value
    #print(Wingspan)   #testing works 
    #return()
        












#IGNORE CODE BELOW (USELESS AND DUMB)
'''
for i in range(0, len(f)):
    value = f.iloc[i]['Aircraft_Parameter_Value']
    var_name = f.iloc[i]['Aircraft_Parameter']
    print(var_name, value, type(var_name), type(value)) #testing works
    exec("%s = %d" % (str(var_name),value))    #locals()[var_name] = 90.89 #globals method used for now. It is possible to use locals or exec too (not sure about differences at this stage) #GLOBALS/LOCALS RETURNS STRING INSTEAD OF VARIABLE VALUE
    #exec("%s = %d" % (var_name,value)) #DOES NOT WORK
    #exec("%s = %d" % (f.iloc[i]['Aircraft_Parameter'],f.iloc[i]['Aircraft_Parameter_Value'])) #DOES NOT WORK
    #print(var_name)

print(Cruise_Attack_Angle)


    

value = f.loc[80,'Aircraft_Parameter_Value']
var_name = f.loc[80,'Aircraft_Parameter']

exec("%s = %d" % (var_name,value))
#globals()[var_name] = value #globals method used for now. It is possible to use locals or exec too (not sure about differences at this stage)
print(var_name)
'''


'''
for i in range(0, len(f)):
    value = f.iloc[i]['Aircraft_Parameter_Value']
    var_name = f.iloc[i]['Aircraft_Parameter']
    globals()[var_name] = value #globals method used for now. It is possible to use locals or exec too (not sure about differences at this stage)
    print(var_name)

#testing 

for i in range(0, len(f)):
    var_name = f.iloc[i]['Aircraft_Parameter']
    print(var_name)    
'''
#input("Press enter to exit")

