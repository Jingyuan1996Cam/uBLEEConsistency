import uBLEEConsistency
#import the Read_PeLEE_Trees??

def get_datasets():

  df_numu_MC_BNB = get_frame([("/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/numu/mc.root", 0.159)], ["weightSplineTimesTune"])
  df_numu_DIRT   = get_frame([("/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/numu/dirt.root", 0.649)], ["weightSplineTimesTune"])
  df_numu_EXT    = get_frame([("/uboone/data/users/wospakrk/sbnfit_0928/numu/ext.root", 0.257)], ["weightTune"])
  
  df_numu = [df_numu_MC_BNB, df_numu_DIRT, df_numu_EXT]

  POT = 2.13#2.13E+20,now all dataframes are scaled to 1E+20, we only need to multiply the needed POT at the analysis level
  
  for df_i in df_numu:
      df_i.enu_reco *= 1000#Turns energy from GeV to MeV
      #df_i['enu_reco'] *= 1000#Will this also work?
      df_i.event_weight *= 1/POT

  df_numu_MC_BNB['IsDirt'] = 0
  df_numu_DIRT['IsDirt']   = 1
  df_numu_EXT['IsDirt']    = 2

  df_all = np.concat(df_numu)
  
  #hknumuCCQE     = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==0) & ((df_numu_MC_BNB['nu_pdg_final']== 14) | (df_numu_MC_BNB['nu_pdg_final']== -14))  & (df_numu_MC_BNB['nu_interaction_mode'] == 0)]#pdg == +-14 means muon and +-12 is electron
  #hknumuRes      = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==0) & ((df_numu_MC_BNB['nu_pdg_final']== 14) | (df_numu_MC_BNB['nu_pdg_final']== -14))  & (df_numu_MC_BNB['nu_interaction_mode'] == 1)]#IsNC=0 means CC and 1 is NC
  #hknumuMEC      = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==0) & ((df_numu_MC_BNB['nu_pdg_final']== 14) | (df_numu_MC_BNB['nu_pdg_final']== -14))  & (df_numu_MC_BNB['nu_interaction_mode'] == 10)]#interaction mode==0 is CCQE, 1 is Res, 10 is MEC
  #hknumuCCOther  = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==0) & ((df_numu_MC_BNB['nu_pdg_final']== 14) | (df_numu_MC_BNB['nu_pdg_final']== -14))  & (df_numu_MC_BNB['nu_interaction_mode'] != 0) & (df_numu_MC_BNB['nu_interaction_mode'] != 1) & (df_numu_MC_BNB['nu_interaction_mode'] != 10)]
  #hknuEInclusive = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==0) & ((df_numu_MC_BNB['nu_pdg_final']== 12) | (df_numu_MC_BNB['nu_pdg_final']== -12))]
  #hkNCInclusive  = df_numu_MC_BNB[(df_numu_MC_BNB['IsNC']==1)]
  
  #x = [hknumuCCQE, hknumuRes, hknumuMEC, hknumuCCOther, hknuEInclusive, hkNCInclusive, df_numu_DIRT, df_numu_EXT]
  
  return df_all

#May be we need to perform the function here??
