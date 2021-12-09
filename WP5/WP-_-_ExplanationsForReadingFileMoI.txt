

# Defining the lists, copy this to the begin part of your code

y_lst = []
Izz_lst = []
Ixx_lst = []
Ixz_lst = []


#------------------------------------------------------------------------
# Reading the y positions from the file 

with open("ylst.dat", "r") as file : # Reads the y position file 
    y_lstRAW = file.readlines()

for line in y_lstRAW :
    y = line.replace(",", "")
    y = float(y)
    y_lst.append(y)


#------------------------------------------------------------------------
# Reading the 3 DAT files with the MoI of the wingbox ONLY. It will result in 3 lists called: Izz_lst, Ixx_lst and Ixy_lst

with open("Izz_lst_Wingbox.dat", "r") as file : 
    Izz_lstRAW = file.readlines()
    
for line in Izz_lstRAW :
    Izz = line.replace("\n", "")
    Izz = float(Izz)
    Izz_lst.append(Izz)


  
with open("Ixz_lst_Wingbox.dat", "r") as file : 
    Ixz_lstRAW = file.readlines()
    
for line in Ixz_lstRAW :
    Ixz = line.replace("\n", "")
    Ixz = float(Ixz)
    Ixz_lst.append(Ixz)




with open("Ixx_lst_Wingbox.dat", "r") as file : 
    Ixx_lstRAW = file.readlines()
    
for line in Ixx_lstRAW :
    Ixx = line.replace("\n", "")
    Ixx = float(Ixx)
    Ixx_lst.append(Ixx)


print(Ixx_lst, Ixz_lst, Izz_lst)
