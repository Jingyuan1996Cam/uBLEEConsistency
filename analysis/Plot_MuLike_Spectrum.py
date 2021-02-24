##Now that you have dataframes from datasets/PeLEE_numu_......
import sys, getopt
######################
##Reading arguements##
######################
full_cmd_arguments = sys.argv
# Keep all but the first, since the first is the fileneme
argument_list = full_cmd_arguments[1:]
print argument_list

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
        LOWER_LIMIT = current_value
    elif current_argument in ("-u", "--max-energy"):
        print ("The upper limit of energy is: %s MeV" %current_value)
        UPPER_LIMIT = current_value
    elif current_argument in ("-d", "--dataset"):
        print ("The version of the dataset is: %s" %current_value)
        DATASET = current_value
    elif current_argument in ("-p", "--POT"):
        print ("The POT is %sE+20" %current_value)
        INPUT_POT = current_value

NORMALIZATION = False

################################################
##Use DATASET to call the correct get_datasets##
################################################

df_all.event_weight *= INPUT_POT#POT scaling according to the input POT
df_with_energy_cut=df_all[(df_all['enu_reco']<UPPER_LIMIT) & (df_all['enu_reco']>LOWER_LIMIT)]

df_numu_MC_BNB = df_with_energy_cut[df_with_energy_cut['IsDirt']==0]
df_numu_DIRT   = df_with_energy_cut[df_with_energy_cut['IsDirt']==1]
df_numu_EXT    = df_with_energy_cut[df_with_energy_cut['IsDirt']==2]

#########################
##Drawing CCQE,CCRes...##
#########################
hknumuCCQE     = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==0) & ((df_numu_MC_BNB['nu_pdg_final']== 14) | (df_numu_MC_BNB['nu_pdg_final']== -14))  & (df_numu_MC_BNB['nu_interaction_mode'] == 0)]#pdg == +-14 means muon and +-12 is electron
hknumuRes      = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==0) & ((df_numu_MC_BNB['nu_pdg_final']== 14) | (df_numu_MC_BNB['nu_pdg_final']== -14))  & (df_numu_MC_BNB['nu_interaction_mode'] == 1)]#IsNC=0 means CC and 1 is NC
hknumuMEC      = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==0) & ((df_numu_MC_BNB['nu_pdg_final']== 14) | (df_numu_MC_BNB['nu_pdg_final']== -14))  & (df_numu_MC_BNB['nu_interaction_mode'] == 10)]#interaction mode==0 is CCQE, 1 is Res, 10 is MEC
hknumuCCOther  = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==0) & ((df_numu_MC_BNB['nu_pdg_final']== 14) | (df_numu_MC_BNB['nu_pdg_final']== -14))  & (df_numu_MC_BNB['nu_interaction_mode'] != 0) & (df_numu_MC_BNB['nu_interaction_mode'] != 1) & (df_numu_MC_BNB['nu_interaction_mode'] != 10)]
hknuEInclusive = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==0) & ((df_numu_MC_BNB['nu_pdg_final']== 12) | (df_numu_MC_BNB['nu_pdg_final']== -12))]
hkNCInclusive  = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==1)]

x      = [hknumuCCQE, hknumuRes, hknumuMEC, hknumuCCOther, hknuEInclusive, hkNCInclusive, df_numu_DIRT, df_numu_EXT]
data   = [hknumuCCQE.enu_reco, hknumuRes.enu_reco, hknumuMEC.enu_reco, hknumuCCOther.enu_reco, hknuEInclusive.enu_reco, hkNCInclusive.enu_reco, df_numu_DIRT.enu_reco, df_numu_EXT.enu_reco]
if NORMALIZATION is True:
    total = 0
    total = sum([h_i.event_weight.sum() for h_i in x])
    for h_i in x:
      h_i.event_weight *= 1/total #h_i.event_weight *= 1/total for h_i in x?
weight = [hknumuCCQE.event_weight, hknumuRes.event_weight, hknumuMEC.event_weight, hknumuCCOther.event_weight, hknuEInclusive.event_weight, hkNCInclusive.event_weight, df_numu_DIRT.event_weight, df_numu_EXT.event_weight]
#Do it in a loop? Use append to add new elements to a []??

######################
##Drawing CC x pi...##
######################

############
##Plotting##
############
plt.figure(figsize=(15,10))
labels= [r"BNB $\nu_{\mu}$ CCQE", r"BNB $\nu_{\mu}$ Res",r"BNB $\nu_{\mu}$ MEC",r"BNB $\nu_{\mu}$ CCOther",r"$\nu_{e}$ Inclusive","NC Inlcusive", 'EXT', 'DIRT']
#labels= [r"BNB $\nu_{\mu}$ CCQE 0.368", r"BNB $\nu_{\mu}$ Res 0.262",r"BNB $\nu_{\mu}$ MEC 0.136",r"BNB $\nu_{\mu}$ CCOther 0.052",r"$\nu_{e}$ Inclusive 0.007","NC Inlcusive 0.060", 'EXT 0.085', 'DIRT 0.028','PeLEE tech note']#This is the label for normalized histogram
#labels= [r"BNB $\nu_{\mu}$ CCQE 4655.96", r"BNB $\nu_{\mu}$ Res 3310.37",r"BNB $\nu_{\mu}$ MEC 1725.66",r"BNB $\nu_{\mu}$ CCOther 656.83",r"$\nu_{e}$ Inclusive 95.32","NC Inlcusive 762.95", 'EXT 1077.77', 'DIRT 353.85','PeLEE tech note 50925.99']#'f' is used to print variables
#labels= [r"BNB $\nu_{\mu}$ CCQE 13924.17", r"BNB $\nu_{\mu}$ Res 9900.03",r"BNB $\nu_{\mu}$ MEC 5160.79",r"BNB $\nu_{\mu}$ CCOther 1964.31",r"$\nu_{e}$ Inclusive 285.07","NC Inlcusive 2281.70", 'EXT 3223.19', 'DIRT 1058.23','PeLEE tech note 50925.99']#With POT scaling 6.37/2.13
#plt.hist(x, bins=14, range=(LOWER_LIMIT, UPPER_LIMIT), stacked=True,label=labels, weights=y)#Weights should have the same shape with data
n, bins, patches = plt.hist(x, 14,histtype='bar',stacked=True, weights=y,
                        color=['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray'],
                        label=[r"BNB $\nu_{\mu}$ CCQE", r"BNB $\nu_{\mu}$ Res",r"BNB $\nu_{\mu}$ MEC",r"BNB $\nu_{\mu}$ CCOther",r"$\nu_{e}$ Inclusive","NC Inlcusive", 'EXT', 'DIRT'])

hatches = [' ',' ',' ',' ',' ',' ',' ',' ']
for patch_set, hatch in zip(patches, hatches):
    for patch in patch_set.patches:
        patch.set_hatch(hatch)

#plt.hist(x1,bins=14,range=(LOWER_LIMIT, UPPER_LIMIT),weights=y2, histtype='step',label='PeLEE tech note',linewidth=2,edgecolor='black')
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
#x1_line              = Line2D([0], [0], color='k', linewidth=2, label="PeLEE tech note")

handle_me = [hknumuCCQE_patch,hknumuRes_patch,hknumuMEC_patch,hknumuCCOther_patch,hknuEInclusive_patch,hkNCInclusive_patch,hext_patch,hdirt_patch]
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

