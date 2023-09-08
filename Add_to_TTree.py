import ROOT
ROOT.ROOT.EnableImplicitMT()
ROOT.gInterpreter.Declare('#include "Add_to_TTree.h"')

#MassList = [500, 600, 700, 800, 900, 1000]
MassList = [1250, 1500, 1750, 2000, 2500, 3000]

InputDir = "/eos/uscms/store/user/huiwang/Dijet/ML_TTree/"
OutputDir = "ML_TTree/"

LvecJ1 = "pt_ordered_jet1_pt, pt_ordered_jet1_eta, pt_ordered_jet1_phi, pt_ordered_jet1_m"
LvecJ2 = LvecJ1.replace("jet1", "jet2")
LvecJ3 = LvecJ1.replace("jet1", "jet3")
LvecJ4 = LvecJ1.replace("jet1", "jet4")

for Mass in MassList:
    RootFile = "tree_ML_MCRun2_" + str(Mass) + "GeV.root"
    print "processing ", RootFile
    RDF = ROOT.RDataFrame("tree_ML", InputDir + RootFile)

    RDF = RDF.Define("y12", "get_y(" + LvecJ1 + ", " + LvecJ2 + ")")
    RDF = RDF.Define("y34", "get_y(" + LvecJ3 + ", " + LvecJ4 + ")")
    RDF = RDF.Define("y13", "get_y(" + LvecJ1 + ", " + LvecJ3 + ")")
    RDF = RDF.Define("y24", "get_y(" + LvecJ2 + ", " + LvecJ4 + ")")
    RDF = RDF.Define("y14", "get_y(" + LvecJ1 + ", " + LvecJ4 + ")")
    RDF = RDF.Define("y23", "get_y(" + LvecJ2 + ", " + LvecJ3 + ")")

    RDF.Snapshot("tree_ML", OutputDir + RootFile)
