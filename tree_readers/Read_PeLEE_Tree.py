##################################################
##This code tries to read files from PeLEE group##
##################################################
import ROOT as R
import pandas as pd
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import matplotlib

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

#df_no_energy_cut = get_frame()#df now has all information
#df_no_energy_cut_ext = get_frame_ext()

##########################################################################################################################

df_1enp_nue    = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/nue.root"])
df_1enp_MC_BNB = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/mc.root"])
df_1enp_CC0pi  = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/ccnopi.root"])
df_1enp_CCpi0  = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/ccpi0.root"])
df_1enp_NCCpi  = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/nccpi.root"])
df_1enp_NC0pi  = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/ncnopi.root"])
df_1enp_NCpi0  = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/ncpi0.root"])
df_1enp_CCCpi  = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/cccpi.root"])
df_1enp_EXT    = get_frame_ext(["/uboone/data/users/wospakrk/sbnfit_0928/1eNp/ext.root"])

df_1enp_nue['POT_weight']    = 0.00355
df_1enp_MC_BNB['POT_weight'] = 0.187
df_1enp_CC0pi['POT_weight']  = 0.0305
df_1enp_CCpi0['POT_weight']  = 0.0692
df_1enp_NCCpi['POT_weight']  = 0.0107
df_1enp_NC0pi['POT_weight']  = 0.0237
df_1enp_NCpi0['POT_weight']  = 0.0494
df_1enp_CCCpi['POT_weight']  = 0.0227
df_1enp_EXT['POT_weight']    = 0.371#Check if the number in python is long enough

df_1e0p_nue    = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/nue.root"])
df_1e0p_MC_BNB = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/mc.root"])
df_1e0p_CC0pi  = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/ccnopi.root"])
df_1e0p_CCpi0  = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/ccpi0.root"])
df_1e0p_NCCpi  = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/nccpi.root"])
df_1e0p_NC0pi  = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/ncnopi.root"])
df_1e0p_NCpi0  = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/ncpi0.root"])
df_1e0p_CCCpi  = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/cccpi.root"])
df_1e0p_DIRT   = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1e0p_fullMC/dirt.root"])
df_1e0p_EXT    = get_frame_ext(["/uboone/data/users/wospakrk/sbnfit_0928/1e0p/ext.root"])

df_1e0p_nue['POT_weight']    = 0.00355
df_1e0p_MC_BNB['POT_weight'] = 0.187
df_1e0p_CC0pi['POT_weight']  = 0.0305
df_1e0p_CCpi0['POT_weight']  = 0.0692
df_1e0p_NCCpi['POT_weight']  = 0.0107
df_1e0p_NC0pi['POT_weight']  = 0.0237
df_1e0p_NCpi0['POT_weight']  = 0.0494
df_1e0p_CCCpi['POT_weight']  = 0.0227
df_1e0p_DIRT['POT_weight']   = 0.428
df_1e0p_EXT['POT_weight']    = 0.371

df_numu_MC_BNB = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/numu/mc.root"])
df_numu_DIRT   = get_frame(["/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/numu/dirt.root"])
df_numu_EXT    = get_frame_ext(["/uboone/data/users/wospakrk/sbnfit_0928/numu/ext.root"])

df_numu_MC_BNB['POT_weight'] = 0.159
df_numu_DIRT['POT_weight']   = 0.649
df_numu_EXT['POT_weight']    = 0.257

##########################################################################################################################

frames = [df_1enp_nue, df_1enp_MC_BNB, df_1enp_CC0pi, df_1enp_CCpi0, df_1enp_NCCpi, df_1enp_NC0pi, df_1enp_NCpi0, df_1enp_CCCpi,
          df_1e0p_nue, df_1e0p_MC_BNB, df_1e0p_CC0pi, df_1e0p_CCpi0, df_1e0p_NCCpi, df_1e0p_NC0pi, df_1e0p_NCpi0, df_1e0p_CCCpi,
          df_numu_MC_BNB]
frames_dirt = [df_1e0p_DIRT,df_numu_DIRT]
frames_ext = [df_1enp_EXT, df_1e0p_EXT, df_numu_EXT]
df_no_energy_cut_total = pd.concat(frames)
df_no_energy_cut_ext = pd.concat(frames_ext)
df_no_energy_cut_dirt = pd.concat(frames_dirt)
df_no_energy_cut_total.enu_reco *= 1000#Now the reco energy is in [MeV]
df_no_energy_cut_ext.enu_reco *= 1000
df_no_energy_cut_dirt.enu_reco *= 1000

df_no_energy_cut_total['POT_Times_weight'] = df_no_energy_cut_total['POT_weight'] * df_no_energy_cut_total['event_weight']
df_no_energy_cut_ext['POT_Times_weight'] = df_no_energy_cut_ext['POT_weight'] * df_no_energy_cut_ext['event_weight']
df_no_energy_cut_dirt['POT_Times_weight'] = df_no_energy_cut_dirt['POT_weight'] * df_no_energy_cut_dirt['event_weight']

################
##Energy range##
################

UPPER_LIMIT = 1550
LOWER_LIMIT = 150

df=df_no_energy_cut_total[(df_no_energy_cut_total['enu_reco']<UPPER_LIMIT) & (df_no_energy_cut_total['enu_reco']>LOWER_LIMIT)]
df_ext=df_no_energy_cut_ext[(df_no_energy_cut_ext['enu_reco']<UPPER_LIMIT) & (df_no_energy_cut_ext['enu_reco']>LOWER_LIMIT)]
df_dirt=df_no_energy_cut_dirt[(df_no_energy_cut_dirt['enu_reco']<UPPER_LIMIT) & (df_no_energy_cut_dirt['enu_reco']>LOWER_LIMIT)]
#df['reco_with_weight']     = df['enu_reco'] * df['event_weight'] #Bullshit

hknumuCCQE     = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 0)]#pdg == +-14 means muon and +-12 is electron
hknumuRes      = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 1)]#IsNC=0 means CC and 1 is NC
hknumuMEC      = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 10)]#interaction mode==0 is CCQE, 1 is Res, 10 is MEC
hknumuCCOther  = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] != 0) & (df['nu_interaction_mode'] != 1) & (df['nu_interaction_mode'] != 10)]
hknuEInclusive = df[(df['IsNC']==0) & ((df['nu_pdg_final']== 12) | (df['nu_pdg_final']== -12))]
hkNCInclusive  = df[(df['IsNC']==1)]

#Calculate total entries and normalize according to it
#total_counts = hknumuCCQE.event_weight.sum() + hknumuRes.event_weight.sum() + hknumuMEC.event_weight.sum() + hknumuCCOther.event_weight.sum() + hknuEInclusive.event_weight.sum() + hkNCInclusive.event_weight.sum()+df_ext.event_weight.sum()
Normalization = False
if Normalization is True:
    total_counts = hknumuCCQE.POT_Times_weight.sum() + hknumuRes.POT_Times_weight.sum() + hknumuMEC.POT_Times_weight.sum() + hknumuCCOther.POT_Times_weight.sum() + hknuEInclusive.POT_Times_weight.sum() + hkNCInclusive.POT_Times_weight.sum()+df_ext.POT_Times_weight.sum()+df_dirt.POT_Times_weight.sum()
    df['norm'] = 1/total_counts
    df['norm_weight'] = df['POT_Times_weight'] * df['norm']
    
    df_ext['norm'] = 1/total_counts
    df_ext['norm_weight'] = df_ext['POT_Times_weight'] * df_ext['norm']

    df_dirt['norm'] = 1/total_counts
    df_dirt['norm_weight'] = df_dirt['POT_Times_weight'] * df_dirt['norm']
else:
    df['norm_weight'] = df['POT_Times_weight'] *6.37/2.13#6.37 over 2.13 is the POT scaling?
    df_ext['norm_weight'] = df_ext['POT_Times_weight'] *6.37/2.13
    df_dirt['norm_weight'] = df_dirt['POT_Times_weight'] * 6.37/2.13

hknumuCCQE_enu_reco     = df.enu_reco[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 0)]#pdg == +-14 means muon and +-12 is electron
hknumuRes_enu_reco      = df.enu_reco[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 1)]#IsNC=0 means CC and 1 is NC
hknumuMEC_enu_reco      = df.enu_reco[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 10)]#interaction mode==0 is CCQE, 1 is Res, 10 is MEC
hknumuCCOther_enu_reco  = df.enu_reco[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] != 0) & (df['nu_interaction_mode'] != 1) & (df['nu_interaction_mode'] != 10)]
hknuEInclusive_enu_reco = df.enu_reco[(df['IsNC']==0) & ((df['nu_pdg_final']== 12) | (df['nu_pdg_final']== -12))]
hkNCInclusive_enu_reco  = df.enu_reco[(df['IsNC']==1)]
hext_enu_reco           = df_ext.enu_reco
hdirt_enu_reco          = df_dirt.enu_reco

hknumuCCQE_norm     = df.norm_weight[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 0)]#pdg == +-14 means muon and +-12 is electron
hknumuRes_norm      = df.norm_weight[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 1)]#IsNC=0 means CC and 1 is NC
hknumuMEC_norm      = df.norm_weight[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] == 10)]#interaction mode==0 is CCQE, 1 is Res, 10 is MEC
hknumuCCOther_norm  = df.norm_weight[(df['IsNC']==0) & ((df['nu_pdg_final']== 14) | (df['nu_pdg_final']== -14))  & (df['nu_interaction_mode'] != 0) & (df['nu_interaction_mode'] != 1) & (df['nu_interaction_mode'] != 10)]
hknuEInclusive_norm = df.norm_weight[(df['IsNC']==0) & ((df['nu_pdg_final']== 12) | (df['nu_pdg_final']== -12))]
hkNCInclusive_norm  = df.norm_weight[(df['IsNC']==1)]
hext_norm           = df_ext.norm_weight
hdirt_norm          = df_dirt.norm_weight

x = [hknumuCCQE_enu_reco, hknumuRes_enu_reco, hknumuMEC_enu_reco, hknumuCCOther_enu_reco, hknuEInclusive_enu_reco, hkNCInclusive_enu_reco, hext_enu_reco, hdirt_enu_reco]
y = [hknumuCCQE_norm, hknumuRes_norm, hknumuMEC_norm, hknumuCCOther_norm, hknuEInclusive_norm, hkNCInclusive_norm, hext_norm, hdirt_norm]

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

if Normalization is True:
    total_y1 = 0
    for i in range(len(y1)):
        total_y1 += y1[i]

    y2 = y1
    for i in range(len(y1)):
        y2[i] = y1[i]/total_y1
else:
    y2 = y1

############
##Plotting##
############

plt.figure(figsize=(15,10))
#labels= [r"BNB $\nu_{\mu}$ CCQE", r"BNB $\nu_{\mu}$ Res",r"BNB $\nu_{\mu}$ MEC",r"BNB $\nu_{\mu}$ CCOther",r"$\nu_{e}$ Inclusive","NC Inlcusive", 'EXT', 'DIRT','PeLEE tech note']
#labels= [r"BNB $\nu_{\mu}$ CCQE 0.368", r"BNB $\nu_{\mu}$ Res 0.262",r"BNB $\nu_{\mu}$ MEC 0.136",r"BNB $\nu_{\mu}$ CCOther 0.052",r"$\nu_{e}$ Inclusive 0.007","NC Inlcusive 0.060", 'EXT 0.085', 'DIRT 0.028','PeLEE tech note']#This is the label for normalized histogram
#labels= [r"BNB $\nu_{\mu}$ CCQE 4655.96", r"BNB $\nu_{\mu}$ Res 3310.37",r"BNB $\nu_{\mu}$ MEC 1725.66",r"BNB $\nu_{\mu}$ CCOther 656.83",r"$\nu_{e}$ Inclusive 95.32","NC Inlcusive 762.95", 'EXT 1077.77', 'DIRT 353.85','PeLEE tech note 50925.99']#'f' is used to print variables
labels= [r"BNB $\nu_{\mu}$ CCQE 13924.17", r"BNB $\nu_{\mu}$ Res 9900.03",r"BNB $\nu_{\mu}$ MEC 5160.79",r"BNB $\nu_{\mu}$ CCOther 1964.31",r"$\nu_{e}$ Inclusive 285.07","NC Inlcusive 2281.70", 'EXT 3223.19', 'DIRT 1058.23','PeLEE tech note 50925.99']#With POT scaling 6.37/2.13
#plt.hist(x, bins=500, stacked=True,label=labels)
#plt.hist(x, bins=14, range=(LOWER_LIMIT, UPPER_LIMIT), stacked=True,label=labels, weights=y)#Weights should have the same shape with data
n, bins, patches = plt.hist(x, 14,histtype='bar',stacked=True, weights=y,
                        color=['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray'],
                        label=[r"BNB $\nu_{\mu}$ CCQE", r"BNB $\nu_{\mu}$ Res",r"BNB $\nu_{\mu}$ MEC",r"BNB $\nu_{\mu}$ CCOther",r"$\nu_{e}$ Inclusive","NC Inlcusive", 'EXT', 'DIRT'])

hatches = [' ',' ',' ',' ',' ',' ',' ',' ']
for patch_set, hatch in zip(patches, hatches):
    for patch in patch_set.patches:
        patch.set_hatch(hatch)

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
hext_patch           = mpatches.Patch(color='tab:pink', label="EXT")
hdirt_patch          = mpatches.Patch(color='tab:gray', label="DIRT")
#hext_patch           = mpatches.Patch(fill=False, hatch='\\')#If you want the tech note hatch
x1_line              = Line2D([0], [0], color='k', linewidth=2, label="PeLEE tech note")

handle_me = [hknumuCCQE_patch,hknumuRes_patch,hknumuMEC_patch,hknumuCCOther_patch,hknuEInclusive_patch,hkNCInclusive_patch,hext_patch,hdirt_patch,x1_line]
plt.legend(handle_me, labels,fontsize=20)
#plt.yscale('log')
#plt.legend()
if Normalization is True:
    plt.suptitle('PeLEE Neutrino reconstructed energy (GENIE, POT weight included, normalized)',fontsize=22)
else:
    plt.suptitle('PeLEE Neutrino reconstructed energy (GENIE, POT weight included)',fontsize=22)
plt.rc('xtick',labelsize=22)
plt.rc('ytick',labelsize=22)
params = {'axes.labelsize': 22,'axes.titlesize':22, 'legend.fontsize': 20, 'xtick.labelsize': 22, 'ytick.labelsize': 22}#text.fontsize
matplotlib.rcParams.update(params)
#plt.savefig('PeLEE_nu_energy_reco_truth_break_EXT_py.png')
plt.show()
