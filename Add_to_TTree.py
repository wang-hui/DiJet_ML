import ROOT
ROOT.ROOT.EnableImplicitMT()
ROOT.gInterpreter.Declare('#include "Add_to_TTree.h"')

#InputList = [500]
InputList = [500, 600, 700, 800, 900, 1000, 1250, 1500, 1750, 2000, 2500, 3000]
#InputList = ["QCD_1M_stride70"]

InputDir = "/eos/uscms/store/user/huiwang/Dijet/ML_TTree/"
OutputDir = "ML_TTree/"

LvecJ1 = "pt_ordered_jet1_pt, pt_ordered_jet1_eta, pt_ordered_jet1_phi, pt_ordered_jet1_m"
LvecJ2 = LvecJ1.replace("jet1", "jet2")
LvecJ3 = LvecJ1.replace("jet1", "jet3")
LvecJ4 = LvecJ1.replace("jet1", "jet4")

SaveList = ["Mass", "weight", "evt_trig",
        "fourjetmasstev", "Mjj_avg_dRpairing_GeV",

        "Mjj_msortedP1_high_div4jm", "Mjj_msortedP1_low_div4jm",
        "Mjj_msortedP2_high_div4jm", "Mjj_msortedP2_low_div4jm",
        "Mjj_msortedP3_high_div4jm", "Mjj_msortedP3_low_div4jm",

        "P1high_MTeV", "P1low_MTeV",
        "P2high_MTeV", "P2low_MTeV",
        "P3high_MTeV", "P3low_MTeV",

        "P1high_j1", "P1high_j2", "P1low_j1", "P1low_j2",
        "P2high_j1", "P2high_j2", "P2low_j1", "P2low_j2",
        "P3high_j1", "P3high_j2", "P3low_j1", "P3low_j2",

        "P1_omega", "P2_omega", "P3_omega",
        "P1_x", "P2_x", "P3_x",

        "P1high_rho_high", "P1high_rho_low", "P1low_rho_high", "P1low_rho_low",
        "P2high_rho_high", "P2high_rho_low", "P2low_rho_high", "P2low_rho_low",
        "P3high_rho_high", "P3high_rho_low", "P3low_rho_high", "P3low_rho_low",

        "P1high_rho", "P1low_rho",
        "P2high_rho", "P2low_rho",
        "P3high_rho", "P3low_rho",
]

for Input in InputList:
    FileName = "tree_ML_MCRun2_"
    if isinstance(Input, str):
        FileName = FileName + Input  + ".root"
    else:
        FileName = FileName + str(Input) + "GeV.root"

    print "processing ", FileName
    RDF = ROOT.RDataFrame("tree_ML", InputDir + FileName)

    if isinstance(Input, str):
        RDF = RDF.Define("Mass", str(0))
    else:
        RDF = RDF.Define("Mass", str(Input))
        RDF = RDF.Define("weight", str(1))

    RDF = RDF.Define("P1high_MTeV", "Mjj_msortedP1_high / 1000")
    RDF = RDF.Define("P1low_MTeV", "Mjj_msortedP1_low / 1000")
    RDF = RDF.Define("P2high_MTeV", "Mjj_msortedP2_high / 1000")
    RDF = RDF.Define("P2low_MTeV", "Mjj_msortedP2_low / 1000")
    RDF = RDF.Define("P3high_MTeV", "Mjj_msortedP3_high / 1000")
    RDF = RDF.Define("P3low_MTeV", "Mjj_msortedP3_low / 1000")

    RDF = RDF.Define("Mjj_msortedP1_low_div4jm", "P1low_MTeV / fourjetmasstev")
    RDF = RDF.Define("Mjj_msortedP2_low_div4jm", "P2low_MTeV / fourjetmasstev")
    RDF = RDF.Define("Mjj_msortedP3_low_div4jm", "P3low_MTeV / fourjetmasstev")

    RDF = RDF.Define("j1lvec", "ROOT::Math::PtEtaPhiMVector(" + LvecJ1 + ")")
    RDF = RDF.Define("j2lvec", "ROOT::Math::PtEtaPhiMVector(" + LvecJ2 + ")")
    RDF = RDF.Define("j3lvec", "ROOT::Math::PtEtaPhiMVector(" + LvecJ3 + ")")
    RDF = RDF.Define("j4lvec", "ROOT::Math::PtEtaPhiMVector(" + LvecJ4 + ")")

    RDF = RDF.Define("SortedJets", "sort_dijet_mass(j1lvec, j2lvec, j3lvec, j4lvec)")

    RDF = RDF.Define("P1high_j1", "SortedJets[0]")
    RDF = RDF.Define("P1high_j2", "SortedJets[1]")
    RDF = RDF.Define("P1low_j1", "SortedJets[2]")
    RDF = RDF.Define("P1low_j2", "SortedJets[3]")
    RDF = RDF.Define("P2high_j1", "SortedJets[4]")
    RDF = RDF.Define("P2high_j2", "SortedJets[5]")
    RDF = RDF.Define("P2low_j1", "SortedJets[6]")
    RDF = RDF.Define("P2low_j2", "SortedJets[7]")
    RDF = RDF.Define("P3high_j1", "SortedJets[8]")
    RDF = RDF.Define("P3high_j2", "SortedJets[9]")
    RDF = RDF.Define("P3low_j1", "SortedJets[10]")
    RDF = RDF.Define("P3low_j2", "SortedJets[11]")

    RDF = RDF.Define("P1high", "P1high_j1 + P1high_j2")
    RDF = RDF.Define("P1low", "P1low_j1 + P1low_j2")
    RDF = RDF.Define("P2high", "P2high_j1 + P2high_j2")
    RDF = RDF.Define("P2low", "P2low_j1 + P2low_j2")
    RDF = RDF.Define("P3high", "P3high_j1 + P3high_j2")
    RDF = RDF.Define("P3low", "P3low_j1 + P3low_j2")

    RDF = RDF.Define("P1_omega", "abs( tanh(  (P1high.Rapidity() - P1low.Rapidity())/2  ) )")
    RDF = RDF.Define("P2_omega", "abs( tanh(  (P2high.Rapidity() - P2low.Rapidity())/2  ) )")
    RDF = RDF.Define("P3_omega", "abs( tanh(  (P3high.Rapidity() - P3low.Rapidity())/2  ) )")

    RDF = RDF.Define("P1_x", "-1 + fourjetmasstev / (P1high_MTeV + P1low_MTeV)")
    RDF = RDF.Define("P2_x", "-1 + fourjetmasstev / (P2high_MTeV + P2low_MTeV)")
    RDF = RDF.Define("P3_x", "-1 + fourjetmasstev / (P3high_MTeV + P3low_MTeV)")

    RDF = RDF.Define("P1high_rho_j1", "abs(1 - 2 * TMath::Sq( (P1high + P1low_j1).M()/1000 / fourjetmasstev) )")
    RDF = RDF.Define("P1high_rho_j2", "abs(1 - 2 * TMath::Sq( (P1high + P1low_j2).M()/1000 / fourjetmasstev) )")
    RDF = RDF.Define("P1low_rho_j1", "abs(1 - 2 * TMath::Sq( (P1low + P1high_j1).M()/1000 / fourjetmasstev) )")
    RDF = RDF.Define("P1low_rho_j2", "abs(1 - 2 * TMath::Sq( (P1low + P1high_j2).M()/1000 / fourjetmasstev) )")
    RDF = RDF.Define("P2high_rho_j1", "abs(1 - 2 * TMath::Sq( (P2high + P2low_j1).M()/1000 / fourjetmasstev) )")
    RDF = RDF.Define("P2high_rho_j2", "abs(1 - 2 * TMath::Sq( (P2high + P2low_j2).M()/1000 / fourjetmasstev) )")
    RDF = RDF.Define("P2low_rho_j1", "abs(1 - 2 * TMath::Sq( (P2low + P2high_j1).M()/1000 / fourjetmasstev) )")
    RDF = RDF.Define("P2low_rho_j2", "abs(1 - 2 * TMath::Sq( (P2low + P2high_j2).M()/1000 / fourjetmasstev) )")
    RDF = RDF.Define("P3high_rho_j1", "abs(1 - 2 * TMath::Sq( (P3high + P3low_j1).M()/1000 / fourjetmasstev) )")
    RDF = RDF.Define("P3high_rho_j2", "abs(1 - 2 * TMath::Sq( (P3high + P3low_j2).M()/1000 / fourjetmasstev) )")
    RDF = RDF.Define("P3low_rho_j1", "abs(1 - 2 * TMath::Sq( (P3low + P3high_j1).M()/1000 / fourjetmasstev) )")
    RDF = RDF.Define("P3low_rho_j2", "abs(1 - 2 * TMath::Sq( (P3low + P3high_j2).M()/1000 / fourjetmasstev) )")

    RDF = RDF.Define("P1high_rho_high", "TMath::Max(P1high_rho_j1, P1high_rho_j2)")
    RDF = RDF.Define("P1high_rho_low", "TMath::Min(P1high_rho_j1, P1high_rho_j2)")
    RDF = RDF.Define("P1low_rho_high", "TMath::Max(P1low_rho_j1, P1low_rho_j2)")
    RDF = RDF.Define("P1low_rho_low", "TMath::Min(P1low_rho_j1, P1low_rho_j2)")
    RDF = RDF.Define("P2high_rho_high", "TMath::Max(P2high_rho_j1, P2high_rho_j2)")
    RDF = RDF.Define("P2high_rho_low", "TMath::Min(P2high_rho_j1, P2high_rho_j2)")
    RDF = RDF.Define("P2low_rho_high", "TMath::Max(P2low_rho_j1, P2low_rho_j2)")
    RDF = RDF.Define("P2low_rho_low", "TMath::Min(P2low_rho_j1, P2low_rho_j2)")
    RDF = RDF.Define("P3high_rho_high", "TMath::Max(P3high_rho_j1, P3high_rho_j2)")
    RDF = RDF.Define("P3high_rho_low", "TMath::Min(P3high_rho_j1, P3high_rho_j2)")
    RDF = RDF.Define("P3low_rho_high", "TMath::Max(P3low_rho_j1, P3low_rho_j2)")
    RDF = RDF.Define("P3low_rho_low", "TMath::Min(P3low_rho_j1, P3low_rho_j2)")

    RDF = RDF.Define("P1high_rho", "(P1high_rho_j1 + P1high_rho_j2) / 2")
    RDF = RDF.Define("P1low_rho", "(P1low_rho_j1 + P1low_rho_j2) / 2")
    RDF = RDF.Define("P2high_rho", "(P2high_rho_j1 + P2high_rho_j2) / 2")
    RDF = RDF.Define("P2low_rho", "(P2low_rho_j1 + P2low_rho_j2) / 2")
    RDF = RDF.Define("P3high_rho", "(P3high_rho_j1 + P3high_rho_j2) / 2")
    RDF = RDF.Define("P3low_rho", "(P3low_rho_j1 + P3low_rho_j2) / 2")

    OutCols = ROOT.vector("string")()
    for Col in SaveList: OutCols.push_back(Col)

    RDF.Snapshot("tree_ML", OutputDir + FileName, OutCols)
