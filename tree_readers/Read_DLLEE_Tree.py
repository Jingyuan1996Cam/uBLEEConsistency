##################################################
##This code tries to read files from DLLEE group##
##################################################
import ROOT as R
import pandas as pd
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

from uBLEEConsistency import NuEvent
from matplotlib import pyplot as plt

#################
##Reading files##
#################
default_files = ["/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/input_to_sbnfit_v48_Sep24_1mu1p_run1_Oct27.root",
                 "/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/input_to_sbnfit_v48_Sep24_1mu1p_run2_Oct27.root",
                 "/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/input_to_sbnfit_v48_Sep24_1mu1p_run3_Oct27.root"]#all files

mytreename = "sel_bnb_tree"

def get_frame(files=default_files):
  
  tree = R.TChain(mytreename)
  for f in files: tree.AddFile(f)
  
  #data_frame = pd.DataFrame()
  event_list = []
  
  for eventi in tree:
    myevent = NuEvent()
    
    myevent.run                  = eventi.run
    myevent.subrun               = eventi.subrun
    myevent.event                = eventi.event
    myevent.selection            = 1
    myevent.nu_pdg_init          = eventi.nu_pdg
    myevent.nu_pdg_final         = eventi.nu_pdg
    myevent.IsNC                 = eventi.nu_interaction_ccnc
    myevent.nu_interaction_mode  = eventi.nu_interaction_mode
    myevent.enu_true             = eventi.nu_energy_true
    myevent.enu_reco             = eventi.nu_energy_reco
    myevent.event_weight         = eventi.xsec_corr_weight#We acutally need one more term of correction from DLLEE group
    myevent.lepton_theta_reco    = eventi.lepton_theta_reco
    myevent.lepton_momentum_reco = -999.
    
    #data_frame.append(myevent)
    event_list.append(myevent)
    
  return pd.DataFrame(event_list)

#Strange grammar that you do not want to forget
#df[(df['enu_reco'] < 1200)& (df['nu_interaction_mode'] == 10)]

#############
##Selection##
#############

df_no_energy_cut = get_frame()#df now has all information
df=df_no_energy_cut[(df_no_energy_cut['enu_reco']<1200) & (df_no_energy_cut['enu_reco']>200)]
#df['reco_with_weight']     = df['enu_reco'] * df['event_weight'] #Bullshit

hknumuCCQE     = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 0)]#pdg == +-14 means muon and +-12 is electron
hknumuRes      = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 1)]#IsNC=0 means CC and 1 is NC
hknumuMEC      = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 10)]#interaction mode==0 is CCQE, 1 is Res, 10 is MEC
hknumuCCOther  = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] != 0) & (df['nu_interaction_mode'] != 1) & (df['nu_interaction_mode'] != 10)]
hknuEInclusive = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 12) | (df['nu_pdg_final']== -12))]
hkNCInclusive  = df[(df['IsNC']==1)]

#Calculate total entries and normalize according to it
total_counts = hknumuCCQE.event_weight.sum() + hknumuRes.event_weight.sum() + hknumuMEC.event_weight.sum() + hknumuCCOther.event_weight.sum() + hknuEInclusive.event_weight.sum() + hkNCInclusive.event_weight.sum()
df['norm'] = 1/total_counts
df['norm_weight'] = df['event_weight'] * df['norm']

hknumuCCQE_enu_reco     = df.enu_reco[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 0)]#pdg == +-14 means muon and +-12 is electron
hknumuRes_enu_reco      = df.enu_reco[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 1)]#IsNC=0 means CC and 1 is NC
hknumuMEC_enu_reco      = df.enu_reco[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 10)]#interaction mode==0 is CCQE, 1 is Res, 10 is MEC
hknumuCCOther_enu_reco  = df.enu_reco[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] != 0) & (df['nu_interaction_mode'] != 1) & (df['nu_interaction_mode'] != 10)]
hknuEInclusive_enu_reco = df.enu_reco[(df['IsNC']==0) & ((df['nu_pdg_final']== 12) | (df['nu_pdg_final']== -12))]
hkNCInclusive_enu_reco  = df.enu_reco[(df['IsNC']==1)]

hknumuCCQE_norm     = df.norm_weight[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 0)]#pdg == +-14 means muon and +-12 is electron
hknumuRes_norm      = df.norm_weight[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 1)]#IsNC=0 means CC and 1 is NC
hknumuMEC_norm      = df.norm_weight[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 10)]#interaction mode==0 is CCQE, 1 is Res, 10 is MEC
hknumuCCOther_norm  = df.norm_weight[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] != 0) & (df['nu_interaction_mode'] != 1) & (df['nu_interaction_mode'] != 10)]
hknuEInclusive_norm = df.norm_weight[(df['IsNC']==0) & ((df['nu_pdg_final']== 12) | (df['nu_pdg_final']== -12))]
hkNCInclusive_norm  = df.norm_weight[(df['IsNC']==1)]

x = [hknumuCCQE_enu_reco, hknumuRes_enu_reco, hknumuMEC_enu_reco, hknumuCCOther_enu_reco, hknuEInclusive_enu_reco, hkNCInclusive_enu_reco]
y = [hknumuCCQE_norm, hknumuRes_norm, hknumuMEC_norm, hknumuCCOther_norm, hknuEInclusive_norm, hkNCInclusive_norm]

x1 = np.empty(14)
for i in range(len(x1)):
    x1[i] = 200 + 71.35 * i + 35

##########################
##Reading digitized file##
##########################

y1 = np.empty(14)
f = open('/uboone/data/users/shijy/Consistency/nu_mu_CCQE_Content_digitized.txt',"r")
for i in range(len(y1)):
    y1[i] = f.readline()
#weight = np.empty(14)
#weght.fill(1/total)
total_y1 = 0
for i in range(len(y1)):
    total_y1 += y1[i]
y2 = y1
for i in range(len(y1)):
    y2[i] = y1[i]/total_y1

############
##Plotting##
############

plt.figure(figsize=(15,10))
labels= [r"BNB $\nu_{\mu}$ CCQE", r"BNB $\nu_{\mu}$ Res",r"BNB $\nu_{\mu}$ MEC",r"BNB $\nu_{\mu}$ CCOther",r"$\nu_{e}$ Inclusive","NC Inlcusive", 'DLLEE tech note']
#plt.hist(x, bins=500, stacked=True,label=labels)
plt.hist(x, bins=14, range=(200,1200), stacked=True,label=labels, weights=y)#Weights should have the same shape with data
plt.hist(x1,bins=14,range=(200,1200),weights=y2, histtype='step',label='digitized',linewidth=2,edgecolor='black')
plt.xlabel('Neutrino reconstructed energy [MeV]', fontsize=22)

##################
##Legend entries##
##################

hknumuCCQE_patch     = mpatches.Patch(color='tab:blue', label=r"BNB $\nu_{\mu}$ CCQE")
hknumuRes_patch      = mpatches.Patch(color='tab:orange', label=r"BNB $\nu_{\mu}$ Res")
hknumuMEC_patch      = mpatches.Patch(color='tab:green', label=r"BNB $\nu_{\mu}$ MEC")
hknumuCCOther_patch  = mpatches.Patch(color='tab:red', label=r"BNB $\nu_{\mu}$ CC Other")
hknuEInclusive_patch = mpatches.Patch(color='tab:purple', label=r"$\nu_{e}$ Inclusive")
hkNCInclusive_patch  = mpatches.Patch(color='tab:brown', label="NC Inlcusive")
x1_line              = Line2D([0], [0], color='k', linewidth=2, label="DLLEE tech note")

handle_me = [hknumuCCQE_patch,hknumuRes_patch,hknumuMEC_patch,hknumuCCOther_patch,hknuEInclusive_patch,hkNCInclusive_patch,x1_line]
plt.legend(handle_me, labels,fontsize=20)
#plt.yscale('log')
#plt.legend()
plt.suptitle('Neutrino reconstructed energy (GENIE weight included, normalized)',fontsize=22)
plt.rc('xtick',labelsize=22)
plt.rc('ytick',labelsize=22)
#plt.savefig('nu_energy_reco_truth_break_ccnc_py.png')
plt.show()
