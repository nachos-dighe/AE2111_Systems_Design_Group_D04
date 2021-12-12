from WP4_XFLR5_Raw_Data import *
from WP4_XFLR5_Raw_Data import xlst_0
from WP4_1_main import *
from WP4_1_main import Vres_poscrit, Vres_negcrit, TMres_poscrit ,TMres_negcrit


##xlst = xlst_0
##
### shear flow due to shear
##
### tau_av = V / ( h_f * t_f + h_r * t_r )
### ==> multipy with appropriate k_v
### ==> multiply with saftey factor
##
##t_f = 0.00198
##t_r = 0.00198
##
##def shearstress_ave (Vlst, t_f, t_r ):
##    tau_av_lst = Vlst / ( 0.0865 * xlst * t_f + 0.0542 * xlst * t_r)
##    return tau_av_lst
##
##def shearstress_T (t, Tlst):
##    q = Tlst / ( ( 0.0856 * xlst + 0.0542 * xlst ) * 0.55 * xlst )
##    tau_T = q / t
##    return tau_T
##
##tau_tot_f_pos = shearstress_ave(Vres_poscrit, t_f, t_r) * 1.5 + shearstress_T(t_f, TMres_negcrit)


# criticial stress


