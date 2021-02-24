##################################################
##This code tries to read files from PeLEE group##
##################################################
import ROOT as R
import pandas as pd
import numpy as np
from uBLEEConsistency import NuEvent

mytreename = "NeutrinoSelectionFilter"

################################
##examples only, don't include##
################################
#files_with_weights = [
#   ("/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/nue.root", 0.00355),
#   ("/uboone/data/users/davidc/searchingfornues/v08_00_00_48/0928/SBNFit/1eNp_fullMC/mc.root" , 0.187)
# ]
#
#weight_branches_bnb = ["weightSplineTimesTune"]
#weight_branches_ext = ["weightTune"]
################################
################################
################################

# list of files and their associated weight [(filename,wght),(filename,wght)]
# weight branches is list of branch names containing weights
def get_frame(files_with_weights,weight_branches):

  event_list = []
  for i,(filename,input_weight) in enumerate(files_with_weights):
    myfile = R.TFile(filename)
    assert(myfile.IsOpen())
    tree = myfile.Get(mytreename)

  #data_frame = pd.DataFrame()
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
      myevent.lepton_theta_reco    = -999#Not sure
      myevent.lepton_momentum_reco = -999.

      myevent.event_weight = input_weight * np.prod([getattr(eventi,b) for b in weight_branches])
      #getattr(eventi,b) is eventi.b, while for ext files, b should be weightTune.

      #data_frame.append(myevent)
      event_list.append(myevent)

  return pd.DataFrame(event_list)
