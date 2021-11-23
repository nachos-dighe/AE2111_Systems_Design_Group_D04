from WP4_1_shear_moment_torsion_function import shear,moment, torsion
import matplotlib.pyplot as plt
from WP4_XFLR5_Raw_Data import xlst_0, ylst_0, Llst_des, Llst_negcrit, Llst_poscrit, Fzreslst_des, Fzreslst_poscrit, Fzreslst_negcrit,Ltot_des, Ltot_poscrit, Ltot_negcrit

#shear
Vres_des=shear(ylst_0,Llst_des, Fzreslst_des, Ltot_des)
Vres_poscrit=shear(ylst_0,Llst_poscrit, Fzreslst_poscrit, Ltot_poscrit)
Vres_negcrit=shear(ylst_0,Llst_negcrit, Fzreslst_negcrit, Ltot_negcrit)

#bending moment
BMres_des=moment(Vres_des,ylst_0)
BMres_poscrit=moment(Vres_poscrit,ylst_0)
BMres_negcrit=moment(Vres_negcrit,ylst_0)

#torsional moment
TMres_des=torsion(ylst_0,Llst_des,xlst_0, Ltot_des)
TMres_poscrit=torsion(ylst_0,Llst_poscrit,xlst_0, Ltot_poscrit)
TMres_negcrit=torsion(ylst_0,Llst_negcrit,xlst_0, Ltot_negcrit)


def internal_plots(ylst,Vlst, BMlst, TMlst):
    
    #print('Total lift is', Ltot, ' ' ,'Total drag is', Dtot, ' ' , 'Total moment is', Mtot, ' ' ,sep ='\n')

    fig, axs = plt.subplots(3, figsize=(8,8), sharex= True)
    axs[0].plot(ylst,Vlst)
    axs[0].set_title('Shear Force')
    axs[1].plot(ylst,BMlst)
    axs[1].set_title('Bending Moment')
    axs[2].plot(ylst,TMlst)
    axs[2].set_title('Torsional Moment')
    fig.suptitle('Internal Force Digrams', fontsize=16)
    fig.tight_layout()
    plt.show()
    return()


#internal load plots: design and critical conditions (uncomment)

internal_plots(ylst_0,Vres_des, BMres_des, TMres_des)
internal_plots(ylst_0, Vres_poscrit,BMres_poscrit,TMres_poscrit)
internal_plots(ylst_0, Vres_negcrit,BMres_negcrit,TMres_negcrit)





