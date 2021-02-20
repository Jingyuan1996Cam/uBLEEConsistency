##################################################
##This code tries to read files from PeLEE group##
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
default_files = ["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/nue.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/mc.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/ccnopi.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/ccpi0.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/nccpi.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/ncnopi.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/ncpi0.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/cccpi.root",
                 #"/uboone/data/users/wospakrk/sbnfit_0928/1eNp/ext.root",#All EXT files don't have "weightSplineTimesTune"
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/nue.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/mc.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/ccnopi.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/ccpi0.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/nccpi.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/ncnopi.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/ncpi0.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/cccpi.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/dirt.root",
                 #"/uboone/data/users/wospakrk/sbnfit_0928/1e0p/ext.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/numu/mc.root",
                 "/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/numu/dirt.root",
                 #"/uboone/data/users/wospakrk/sbnfit_0928/numu/ext.root" #all file names is at https://docs.google.com/spreadsheets/d/1jETunEFA60ZTmg69QANDyytbrS_oXb8f6kbmidfBTME/edit#gid=0
                 ]

ext_files = ["/uboone/data/users/wospakrk/sbnfit_0928/1eNp/ext.root",
             "/uboone/data/users/wospakrk/sbnfit_0928/1e0p/ext.root",
             "/uboone/data/users/wospakrk/sbnfit_0928/numu/ext.root"
            ]

mytreename = "NeutrinoSelectionFilter"

def get_frame(files=default_files):
  
  tree = R.TChain(mytreename)
  for f in files: tree.AddFile(f)
  
  #data_frame = pd.DataFrame()
  event_list = []
  
  for eventi in tree:
    myevent = NuEvent()
    
    myevent.run                  = eventi.run
    myevent.subrun               = eventi.sub
    myevent.event                = eventi.evt
    myevent.selection            = 1
    myevent.nu_pdg_init          = eventi.nu_pdg
    myevent.nu_pdg_final         = eventi.nu_pdg
    myevent.IsNC                 = eventi.ccnc
    myevent.nu_interaction_mode  = eventi.interaction
    myevent.enu_true             = eventi.nu_e
    myevent.enu_reco             = eventi.reco_e#It is in [GeV] in PeLEE files
    myevent.event_weight         = eventi.weightSplineTimesTune#GENIE weight only, consistent with DLLEE
    myevent.lepton_theta_reco    = -999#Not sure
    myevent.lepton_momentum_reco = -999.
    
    #data_frame.append(myevent)
    event_list.append(myevent)
    
  return pd.DataFrame(event_list)

def get_frame_ext(files=ext_files):
  
  tree = R.TChain(mytreename)
  for f in files: tree.AddFile(f)
  
  #data_frame = pd.DataFrame()
  event_list = []
  
  for eventi in tree:
    myevent = NuEvent()

    myevent.run                  = eventi.run
    myevent.subrun               = eventi.sub
    myevent.event                = eventi.evt
    myevent.selection            = 1
    myevent.nu_pdg_init          = eventi.nu_pdg
    myevent.nu_pdg_final         = eventi.nu_pdg
    myevent.IsNC                 = eventi.ccnc
    myevent.nu_interaction_mode  = eventi.interaction
    myevent.enu_true             = eventi.nu_e
    myevent.enu_reco             = eventi.reco_e#It is in [GeV] in PeLEE files
    myevent.event_weight         = eventi.weightTune#They should all be 1 for ext files
    myevent.lepton_theta_reco    = -999#Not sure
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
df_no_energy_cut_ext = get_frame_ext()
frames = [df_no_energy_cut, df_no_energy_cut_ext]
df_no_energy_cut_total = pd.concat(frames)
df_no_energy_cut_total.enu_reco *= 1000#Now the reco energy is in [MeV]

################
##Energy range##
################

UPPER_LIMIT = 1550
LOWER_LIMIT = 150

df=df_no_energy_cut_total[(df_no_energy_cut_total['enu_reco']<UPPER_LIMIT) & (df_no_energy_cut_total['enu_reco']>LOWER_LIMIT)]
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

#########################
##Reading the text file##
#########################

x1 = np.empty(14)
for i in range(len(x1)):
    x1[i] = 200 + 100 * i

y1 = np.empty(14)
f = open('/uboone/data/users/shijy/Consistency/PeLEE_reco_nu_energy_digitized.csv',"r")
for i in range(len(y1)):
    y1[i] = f.readline()

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
labels= [r"BNB $\nu_{\mu}$ CCQE", r"BNB $\nu_{\mu}$ Res",r"BNB $\nu_{\mu}$ MEC",r"BNB $\nu_{\mu}$ CCOther",r"$\nu_{e}$ Inclusive","NC Inlcusive", 'PeLEE tech note']
#plt.hist(x, bins=500, stacked=True,label=labels)
plt.hist(x, bins=14, range=(LOWER_LIMIT, UPPER_LIMIT), stacked=True,label=labels, weights=y)#Weights should have the same shape with data
plt.hist(x1,bins=14,range=(LOWER_LIMIT, UPPER_LIMIT),weights=y2, histtype='step',label='PeLEE tech note',linewidth=2,edgecolor='black')
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
x1_line              = Line2D([0], [0], color='k', linewidth=2, label="PeLEE tech note")

handle_me = [hknumuCCQE_patch,hknumuRes_patch,hknumuMEC_patch,hknumuCCOther_patch,hknuEInclusive_patch,hkNCInclusive_patch,x1_line]
plt.legend(handle_me, labels,fontsize=20)
#plt.yscale('log')
#plt.legend()
plt.suptitle('PeLEE Neutrino reconstructed energy (GENIE weight included, normalized)',fontsize=22)
plt.rc('xtick',labelsize=22)
plt.rc('ytick',labelsize=22)
#plt.savefig('nu_energy_reco_truth_break_ccnc_py.png')
plt.show()
