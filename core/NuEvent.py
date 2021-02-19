from dataclasses import dataclass

int_default   = -1
float_default = -999.

@dataclass
class NuEvent:
  run:    int = int_default
  subrun: int = int_default
  event:  int = int_default

  selection:int = int_default
    
  nu_pdg_init:int = int_default#same with nu_pdg_final
  nu_pdg_final:int = int_default
  #nu_interaction_ccnc:int = int_default#IsNC?
  IsNC: int = int_default
  nu_interaction_mode:int = int_default

  enu_true:float = float_default
  enu_reco:float = float_default
  #nu_energy_true:float = float_default
  #nu_energy_reco:float = float_default
  event_weight:float = float_default#(xsec_corr_weight)
  lepton_theta_reco:float = float_default#reco lepton angle
  lepton_momentum_reco:float = float_default#Not yet needed
