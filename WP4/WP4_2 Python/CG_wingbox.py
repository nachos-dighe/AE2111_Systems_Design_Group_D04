from math import tan, pi

def cg_calculation(Theta2, Theta3, b2, DeltaX):
    
    #intermediate outputs
    a = DeltaX * tan(Theta2)
    c = DeltaX * tan(Theta3)

    x1 = DeltaX / 2
    x2 = DeltaX / 3
    x3 = DeltaX /3

    z3 = DeltaX * 2/3
    z1 = z3 + (b2 /2 )
    z2 = z1 + (c/3)

    A1 = b2 * DeltaX
    A2 = 1/2 * a * DeltaX
    A3 = 1/2 * c * DeltaX

    #cg calculation
    CG_x = ((x1 * A1)+ (x2 * A2) + (x3 * A3))/(A1+ A2 + A3)
    CG_z = ((z1 * A1) + (z2 * A2) + (z3 * A3))/(A1 + A2 + A3)

    return CG_x, CG_z

# deg to rad
r = pi/180

#input variables
Theta2 = 2*r          #[deg]
Theta3 = 0.8*r          #[deg]
b2 = 1              #[m]
DeltaX = 1          #[m]


CG_x, CG_z = cg_calculation(Theta2, Theta3, b2, DeltaX)
print(CG_z)
