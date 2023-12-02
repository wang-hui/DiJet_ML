import ROOT

Dir = "/eos/uscms/store/user/huiwang/Dijet/ML_TTree/"
InputName = "tree_ML_MCRun2_QCD.root"
Stride = 10

RDF = ROOT.RDataFrame("tree_ML", Dir + InputName)

TotEvents = RDF.Count().GetValue()
print "TotEvents", TotEvents

RDF = RDF.Range(0, TotEvents - 1, Stride)
RDF = RDF.Filter("evt_trig == 1")

OutputName = InputName.replace(".root", "_7M_stride10.root")
RDF.Snapshot("tree_ML", Dir + OutputName)
