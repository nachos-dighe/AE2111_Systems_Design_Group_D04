i = int(input('Type 1 for OEW; Type 2 for OEW+MPL+fuel; Type 3 for OEW+MPL'))
i -= 1
rho = 0.3678 #keep it for cruise currently
speed = 243 #big fucking HAHA cos it is continuous, take cruise speed for now




class flight_cond:
    
    g = 9.80665
    m_pl = 9800
    m_oe = 20175
    m_mto = 33139
    m_f = m_mto - m_oe-m_pl
    
    W_ac_lst = [m_oe, m_mto, m_oe+m_pl]*g
    W_fuel_half_wing_lst = [0, 0.3*m_f, 0]
    
    n_pos = 2.5
    n_neg = -1
    
    S_wing = 76.29
    
    def __init__(self, i, rho): #only vary i and rho for sake of simplicity #take speed as discrete steps for now (v_a, v_cruise, v_dive). Later modify to cotinuous...
        self.W_ac = self.W_ac_lst[i]*self.g #requires modification
        self.rho = rho
        self.speed = speed  
    def wing_fuel(self):
        W_fuel_half_wing = self.W_fuel_half_wing_lst[i] #use self.var_name to call variables of the class without passing them as arguments in function
        return(W_fuel_half_wing)
    def C_l(self):
        C_l = self.W_ac/(0.5*self.rho*self.speed**2*self.S_wing)
        return(C_l)
        
        