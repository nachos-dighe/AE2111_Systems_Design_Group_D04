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
    A = (2*L_s*t_s)-(t_s**2)      #Area of one stringer
    cg = (1.5*L_s*L_s - L_s*t_s)/(2*L_s - t_s)

#Positions cg of stringersin terms of x and z of the stringers
#(1-4 being the corner stringers) measured from the bottem left outer corner of the wingbox
    x1 = t+(cg)
    z1 = t+(cg)
    x2 = t+(cg)
    z2 = b + deltax*(tan(beta)+tan(alpha)) - (t+(cg))
    x3 = deltax - (t+(cg))
    z3 = b + deltax*tan(beta) - (t+(cg))
    x4 = deltax - (t+(cg))
    z4 = deltax*tan(beta) + (t+(cg))

#spacing of the stringers and introducing this into the dimensions
    L_top = (deltax/cos(alpha)) - (2*t) - cg         #Length of top/bottem of wingbox where a stringer can be placed (from cg of left corner stringer to cg of left corner stringer)
    L_bot = (deltax/cos(beta)) - (2*t) - cg       
    s_top = L_top/(nr_top-1)                         #Length from cg to cg of the stringers
    s_bot = L_bot/(nr_bot-1)

    lst_stringers = []
    for i in range(0,nr_top):
        x = x1 + i * (s_top * cos(alpha))
        z = z1 - i * (s_top * sin(alpha))
        d = ((x*x)+(z*z))**0.5
        lst_stringers.append(d)
    for j in range(0,nr_bot):
        x = x1 + j * (s_bot * cos(beta))
        z = z1 + j * (s_bot * sin(beta))
        d = ((x*x)+(z*z))**0.5
        lst_stringers.append(d)

#calculation of additional moment of inertia due to stringers
    I_s = 0
    for m in range(0,len(lst_stringers)):
        I_s = I_s + (A*m*m)

#Checking feasibility of overlap stringers (printed the results)
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
    

    return I_s, A
#Need to have a list of the positions of the stringers, x and z

print(moi_stringers(nr_top, nr_bot, L_s, t, t_s, alpha, beta, b, deltax))




