#Rho starts at 0 and goes up step wise
#For each rho calculate the safety margin
#safetymargin difference below 1%
#Perform this per y, so per geometry



rho = 0.001
while True:
    safety_margin1 = stress_concentration_factor (0.005, rho, 29*(10**6), stress_mom)
    rho = rho + 0.001
    safety_margin2 = stress_concentration_factor (0.005, rho, 29*(10**6), stress_mom)
    difference = ((safety_margin2 - safety_margin1)/safety_margin1)*100
    if difference <= 1:
        break
