from math import sin, cos, tan

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


def moi_stringers(nr_top, nr_bot, L_s, t, t_s, alpha, beta, b, deltax):
    
#Intermediate outputs for the moment of inertia
    A = (2*L_s*t_s)-(t_s**2)                        #Area of one stringer
    cg = (1.5*L_s*L_s - L_s*t_s)/(2*L_s - t_s)

#Positions cg of stringers in terms of x
#x1 until x4 being the corner stringers measured from the bottem left outer corner of the wingbox
    x1 = t+(cg)
    x2 = t+(cg)
    x3 = deltax - (t+(cg))
    x4 = deltax - (t+(cg))

#spacing of the stringers and introducing this into the dimensions
    L_top = (deltax/cos(alpha)) - (2*t) - cg         #Length from cg of left to right corner stringer
    L_bot = (deltax/cos(beta)) - (2*t) - cg       
    s_top = L_top/(nr_top-1)                         #Length from cg to cg of the stringers
    s_bot = L_bot/(nr_bot-1)

    xlst = []
    for i in range(0,nr_top):
        xsquare = (x1 + i * (s_top * cos(alpha)))**2
        xlst.append(xsquare)
    for j in range(0,nr_bot):
        xsquare = (x1 + j * (s_bot * cos(beta)))**2
        xlst.append(xsquare)
                    

#calculation of additional moment of inertia due to stringers
    Is_xx = 0
    for m in range(0,len(xlst)):
        Is_xx = Is_xx + (A*xlst[m]*xlst[m])

    return Is_xx, A, s_top, s_bot

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




