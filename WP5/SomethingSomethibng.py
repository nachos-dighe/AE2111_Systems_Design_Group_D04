

# Defining the lists, copy this to the begin part of your code

y_lst = []
I_xxReqNegLst = []
I_xxReqPosLst = []
I_xxReqNegPosRAW = []
I_xxReqPosRAW = []


#------------------------------------------------------------------------
# Reading the y positions from the file 

with open("ylst.dat", "r") as file : # Reads the y position file 
    y_lstRAW = file.readlines()

for line in y_lstRAW :
    y = line.replace(",", "")
    y = float(y)
    y_lst.append(y)


#------------------------------------------------------------------------
# Reading the the Moi required of the wingbox with 2 stringers up top and 2 stringers down

with open("WP5_1_RequierdMoILoadcasePos.dat", "r") as file : 
    I_xxReqNegRAW = file.readlines()
    
for line in I_xxReqNegPosRAW :
    I_xxNegPosReq = line.replace("\n", "")
    I_xxNegPosReq = float(I_xxNegPosReq)
    I_xxReqPosLst.append(I_xxNegPosReq)
  

# Above, positive loas case (2.5) , below negative load case (-1)


with open("WP5_1_RequierdMoILoadcaseNeg.dat", "r") as file : 
    I_xxReqPosRAW = file.readlines()
    
for line in I_xxReqNegRAW :
    I_xxNegReq = line.replace("\n", "")
    I_xxNegReq = float(I_xxNegReq)
    I_xxReqNegLst.append(I_xxNegReq) 
 

E1 = max(I_xxReqPosLst)
E2 = max(I_xxReqNegLst)

print("Pos laod case", E1, "Neg load case", E2)


