import ROOT

Dir = "/eos/uscms/store/user/huiwang/Dijet/ML_TTree/"
InputName = "tree_ML_MCRun2_QCD.root"
RDF = ROOT.RDataFrame("tree_ML", Dir + InputName)

RDF = RDF.Range(0, 70000000, 70)
RDF = RDF.Filter("evt_trig == 1")

OutputName = InputName.replace(".root", "_1M_stride70.root")
RDF.Snapshot("tree_ML", Dir + OutputName)
