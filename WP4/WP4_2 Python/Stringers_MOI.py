#inputs
nr_top = 3      #This is the number of stringers on the top side of the wingbox)
nr_bot = 3      #Nr of stringers on the bottem side)
#(how to do do the stringer distribution over the span, but should be an input as well)
L_s  = 0.1      #Length [m] of the base and height of the stringers, assuming it's symmetric
t = 0.0015      #Thickness [m] of the wingbox
t_s = 0.001     #Thickness [m] of the stringer
alpha = 1
beta = 1
b = 1
deltax = 1

from math import sin, cos, tan

def moi_stringers(nr_top, nr_bot, L_s, t, t_s, alpha, beta, b, deltax):
    
#Intermediate outputs for the moment of inertia
    A = (2*L_s*t_s)-(t_s**2)                    #Area of one stringer
    cg = (1.5*L_s*L_s - L_s*t_s)/(2*L_s - t_s)  #cg location stringer (w.r.t local datum)

#Positions cg of corner stringers in terms of x and z from wingbox datum
    z1 = t+(cg) 
    z2 = b + deltax*(tan(alpha)+tan(beta)) - (t + cg)
    x1 = t+(cg)
    x2 = deltax - (t+(cg))

#spacing of the stringers and introducing this into the dimensions
    L_top = (x2-x1)/cos(alpha)                  #Distance right->left corner stringer
    L_bot = (x2-x1)/cos(beta)      
    s_top = L_top/(nr_top-1)                    #Length from cg to cg of the stringers
    s_bot = L_bot/(nr_bot-1)

    zlst = []
    for i in range(0,nr_top):
        zsquare = (z1 + i * (s_top * sin(alpha)))**2
        zlst.append(zsquare)
    for j in range(0,nr_bot):
        zsquare = (z1 + j * (s_bot * sin(beta)))**2
        zlst.append(zsquare)


#calculation of additional moment of inertia due to stringers
    Is_xx = 0
    for m in range(0,len(zlst)):
        Is_xx = Is_xx + (A*zlst[m]*zlst[m])

    return Is_xx

a = moi_stringers(nr_top, nr_bot, L_s, t, t_s, alpha, beta, b, deltax)

#function feasibility of the stringers space wize
def feasibility_stringers(s_top, s_bot, nr_top, nr_bot, L_s):
    feas_top = s_top - (nr_top*L_s)
    feas_bot = s_bot - (nr_bot*L_s)
    s = 0
    if feas_top < 0 :
        s = s+1
    if feas_bot < 0 :
        s = s+1
    if s > 0:
        print("design is unfeasible stringer overlap wise")
    if s == 0:
        print("design is feasible stringer overlap wise")
#Need to have a list of the positions of the stringers, x and z

## print(moi_stringers(nr_top, nr_bot, L_s, t, t_s, alpha, beta, b, deltax))




