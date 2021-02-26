import sys, getopt
#import pandas as pd
import numpy as np
import uBLEEConsistency.datasets as da#if you do"from uBLEEConsistency import datasets" it will fail

import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import matplotlib

from matplotlib import pyplot as plt

#########################################################################
##An interesting way of importing datasets.PeLEE_numu_v08_00_00_48_0928##
#########################################################################
#import importlib
#DATASET = "uBLEEConsistency.datasets.PeLEE_numu_v08_00_00_48_0928"
#mymodule = importlib.import_module(DATASET)
#df_all = mymodule.get_datasets()

######################
##Reading arguements##
######################
full_cmd_arguments = sys.argv
# Keep all but the first, since the first is the fileneme
argument_list = full_cmd_arguments[1:]
print(argument_list)

short_options = "l:u:d:p:"
long_options = ["min-energy=", "max-energy=", "dataset=", "POT="]
#--min-energy 0.15 --max-energy 1.5 --dataset PeLEE_1mu_v08 --pot 6.37
try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    # Output error, and return with an error code
    print (str(err))
    sys.exit(2)
for current_argument, current_value in arguments:
    if current_argument in ("-l", "--min-energy"):
        print ("The lower limit of energy is: %s MeV" %current_value)
        LOWER_LIMIT = float(current_value)
    elif current_argument in ("-u", "--max-energy"):
        print ("The upper limit of energy is: %s MeV" %current_value)
        UPPER_LIMIT = float(current_value)
    elif current_argument in ("-d", "--dataset"):
        print ("The version of the dataset is: %s" %current_value)
        DATASET = current_value
    elif current_argument in ("-p", "--POT"):
        print ("The POT is: %sE+20" %current_value)
        INPUT_POT = float(current_value)
#Note that all current_value is a string, you need float() to change their type

NORMALIZATION = True
PLOT_DIGITIZED = True

################################################
##Use DATASET to call the correct get_datasets##
################################################
df_all = getattr(da,DATASET).get_datasets()
df_all['event_weight'] *= INPUT_POT#POT scaling according to the input POT
df_with_energy_cut = df_all[(df_all['enu_reco']<UPPER_LIMIT) & (df_all['enu_reco']>LOWER_LIMIT)]
df_numu_MC_BNB = df_with_energy_cut[(df_with_energy_cut['IsDirt']==0)]#With a strange selection cut
df_numu_DIRT   = df_with_energy_cut[(df_with_energy_cut['IsDirt']==1)]
df_numu_EXT    = df_with_energy_cut[(df_with_energy_cut['IsDirt']==2)]

#########################
##Drawing CCQE,CCRes...##
#########################
hknumuCCQE     = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==0) & ((df_numu_MC_BNB['nu_pdg_final']== 14) | (df_numu_MC_BNB['nu_pdg_final']== -14))  & (df_numu_MC_BNB['nu_interaction_mode'] == 0)]#pdg == +-14 means muon and +-12 is electron
hknumuRes      = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==0) & ((df_numu_MC_BNB['nu_pdg_final']== 14) | (df_numu_MC_BNB['nu_pdg_final']== -14))  & (df_numu_MC_BNB['nu_interaction_mode'] == 1)]#IsNC=0 means CC and 1 is NC
hknumuMEC      = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==0) & ((df_numu_MC_BNB['nu_pdg_final']== 14) | (df_numu_MC_BNB['nu_pdg_final']== -14))  & (df_numu_MC_BNB['nu_interaction_mode'] == 10)]#interaction mode==0 is CCQE, 1 is Res, 10 is MEC
hknumuCCOther  = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==0) & ((df_numu_MC_BNB['nu_pdg_final']== 14) | (df_numu_MC_BNB['nu_pdg_final']== -14))  & (df_numu_MC_BNB['nu_interaction_mode'] != 0) & (df_numu_MC_BNB['nu_interaction_mode'] != 1) & (df_numu_MC_BNB['nu_interaction_mode'] != 10)]
hknuEInclusive = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==0) & ((df_numu_MC_BNB['nu_pdg_final']== 12) | (df_numu_MC_BNB['nu_pdg_final']== -12))]
hkNCInclusive  = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==1)]

x = [df_numu_DIRT, hkNCInclusive, hknuEInclusive, hknumuCCQE, hknumuMEC, hknumuRes, hknumuCCOther, df_numu_EXT]
data = []
y = []
z = []
total = 0
if NORMALIZATION is True:
    total = 0
    total = sum([h_i.event_weight.sum() for h_i in x])
    for h_i in x:
      h_i.event_weight *= 1/total
for h_i in x:
  data.append(h_i.enu_reco)
  y.append(h_i.event_weight)
  z.append("{:.2f}".format(h_i.event_weight.sum()))

######################
##Drawing CC x pi...##
######################

################################
##PeLEE tech note digitization##
################################
if DATASET is 'PeLEE_numu_v08_00_00_48_0928':
  x1 = np.empty(14)
  for i in range(len(x1)):
      x1[i] = 200 + 100 * i
  
  y1 = np.empty(14)
  f = open('/uboone/data/users/shijy/Consistency/PeLEE_reco_nu_energy_digitized.csv',"r")
  for i in range(len(y1)):
      y1[i] = f.readline()
  
  if NORMALIZATION is True:
      total_y1 = 0
      for i in range(len(y1)):
          total_y1 += y1[i]
  
      y2 = y1
      for i in range(len(y1)):
          y2[i] = y1[i]/total_y1
  else:
      total_y1 = 0
      for i in range(len(y1)):
          total_y1 += y1[i]
      y2 = y1
else:
  print('No digitized data yet.')

############
##Plotting##
############
plt.figure(figsize=(15,10))
plt.rc('xtick',labelsize=22)
plt.rc('ytick',labelsize=22)
#labels = [r"BNB $\nu_{\mu}$ CCQE", r"BNB $\nu_{\mu}$ Res", r"BNB $\nu_{\mu}$ MEC", r"BNB $\nu_{\mu}$ CCOther", r"$\nu_{e}$ Inclusive", "NC Inlcusive", 'EXT', "DIRT"]
labels = ["DIRT: %s"%z[0], "NC Inlcusive: %s"%z[1], r"$\nu_{e}$ Inclusive: %s"%z[2], r"BNB $\nu_{\mu}$ CCQE: %s"%z[3], r"BNB $\nu_{\mu}$ MEC: %s"%z[4], r"BNB $\nu_{\mu}$ Res: %s"%z[5], r"BNB $\nu_{\mu}$ CCOther: %s"%z[6], 'EXT: %s'%z[7]]
#plt.hist(x, bins=14, range=(LOWER_LIMIT, UPPER_LIMIT), stacked=True,label=labels, weights=y)#Weights should have the same shape with data
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray']
n, bins, patches = plt.hist(data, 14,histtype='bar',stacked=True, weights=y,
                        color=colors,
                        label=labels)

hatches = [' ',' ',' ',' ',' ',' ',' ',' ']
for patch_set, hatch in zip(patches, hatches):
    for patch in patch_set.patches:
        patch.set_hatch(hatch)
if PLOT_DIGITIZED is True:
  plt.hist(x1,bins=14,range=(LOWER_LIMIT, UPPER_LIMIT),weights=y2, histtype='step',label='PeLEE tech note',linewidth=2,edgecolor='black')
plt.xlabel('Neutrino reconstructed energy [MeV]', fontsize=22)

##################
##Legend entries##
##################

hdirt_patch          = mpatches.Patch(color=colors[0], label="DIRT")
hkNCInclusive_patch  = mpatches.Patch(color=colors[1], label="NC Inlcusive")
hknuEInclusive_patch = mpatches.Patch(color=colors[2], label=r"$\nu_{e}$ Inclusive")
hknumuCCQE_patch     = mpatches.Patch(color=colors[3], label=r"BNB $\nu_{\mu}$ CCQE")
hknumuMEC_patch      = mpatches.Patch(color=colors[4], label=r"BNB $\nu_{\mu}$ MEC")
hknumuRes_patch      = mpatches.Patch(color=colors[5], label=r"BNB $\nu_{\mu}$ Res")
hknumuCCOther_patch  = mpatches.Patch(color=colors[6], label=r"BNB $\nu_{\mu}$ CC Other")
hext_patch           = mpatches.Patch(color=colors[7], label="EXT")
#hext_patch           = mpatches.Patch(fill=False, hatch='\\')#If you want the tech note hatch
x1_line              = Line2D([0], [0], color='k', linewidth=2, label="PeLEE tech note")

handle_me = [hdirt_patch, hkNCInclusive_patch, hknuEInclusive_patch, hknumuCCQE_patch, hknumuMEC_patch, hknumuRes_patch, hknumuCCOther_patch, hext_patch]
if PLOT_DIGITIZED is True:
  handle_me.append(x1_line)
  if NORMALIZATION is True:
    labels.append("PeLEE tech note")
  else:
    total = "{:.2f}".format(total_y1)
    labels.append("PeLEE tech note: %s"%total)#################################

plt.legend(handle_me, labels,fontsize=19)
#plt.yscale('log')
#plt.legend()
DATASET_TITLE =  "{:.10s}".format(DATASET)#It is taking the first 10 elements, might not work if we have wirecell stuff
if NORMALIZATION is True:
    plt.suptitle(r'%s $\nu$ reconstructed energy (GENIE, POT weight included, normalized)'%DATASET_TITLE,fontsize=22)
else:
    plt.suptitle(r'%s $\nu$ reconstructed energy (GENIE, POT weight included)'%DATASET_TITLE,fontsize=22)
#plt.savefig('nu_energy_reco_PeLEE_numu_v08_00_00_48_0928_inter_mode_digi_norm.png')
plt.show()

