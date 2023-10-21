import ROOT
ROOT.ROOT.EnableImplicitMT()
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)

#InputList = [500]
#InputList = [500, 600, 700, 800, 900, 1000, 1250, 1500, 1750, 2000, 2500, 3000]
InputList = ["QCD_1M_stride70"]

InputDir = "ML_TTree/"
ResultsDir = "results_temp/"

class PlotCfg:
    def __init__(self, Xval, Xtitle, Xbins, Xlow, Xhigh, Yval, Ytitle, Ybins, Ylow, Yhigh, CfgList):
        self.Xval = Xval
        self.Xtitle = Xtitle
        self.Xbins = Xbins
        self.Xlow = Xlow
        self.Xhigh = Xhigh
        self.Yval = Yval
        self.Ytitle = Ytitle
        self.Ybins = Ybins
        self.Ylow = Ylow
        self.Yhigh = Yhigh
        CfgList.append(self)

CfgList = []
#Mjj_vs_M4j = PlotCfg()
x_vs_omega = PlotCfg("_omega", "", 100, 0, 1, "_x", "", 100, 0, 1.6, CfgList)
Phigh_rho = PlotCfg("high_rho_high", "", 100, 0, 1, "high_rho_low", "", 100, 0, 1, CfgList)
Plow_rho = PlotCfg("low_rho_high", "", 100, 0, 1, "low_rho_low", "", 100, 0, 1, CfgList)
x_vs_Phigh_rho  = PlotCfg("high_rho", "", 100, 0, 1, "_x", "", 100, 0, 1.6, CfgList)
x_vs_Plow_rho  = PlotCfg("low_rho", "", 100, 0, 1, "_x", "", 100, 0, 1.6, CfgList)

Cuts = ""
#Cuts = "Trig"
#Cuts = "Masym"

MyChain = ROOT.TChain("tree_ML")
for Input in InputList:
    FileName = "tree_ML_MCRun2_"
    if isinstance(Input, str):
        FileName = FileName + Input  + ".root"
    else:
        FileName = FileName + str(Input) + "GeV.root"
    MyChain.Add(InputDir + FileName)

RDF = ROOT.RDataFrame(MyChain)
if "Trig" in Cuts: RDF = RDF.Filter("evt_trig == 1")

if len(InputList) > 1 : InputList += [-1]
for Input in InputList:
    print "processing", Input
    RDFTemp = RDF
    Mass = Input
    Title = "Gen mass all"
    if isinstance(Input, str):
        Mass = 0
        Title = "QCD"
    elif Mass != -1:
        RDFTemp = RDFTemp.Filter("Mass == " + str(Mass))
        Title = Title.replace("all", str(Mass) + " GeV")

    for Pair in ["P1", "P2", "P3"]:
        RDFPassCuts = RDFTemp
        if "Masym" in Cuts:
            RDFPassCuts = RDFPassCuts.Filter("abs(" + Pair + "high_MTeV - " + Pair + "low_MTeV) / (" +
                            Pair + "high_MTeV + " + Pair + "low_MTeV) < 0.1", "cut_Masym")
        #CutReport = RDFPassCuts.Report()
        #CutReport.Print()

        MyCanvas = ROOT.TCanvas("MyCanvas", "MyCanvas", 600, 600)
        MyCanvas.SetLeftMargin(0.15)
        MyCanvas.SetRightMargin(0.15)
        MyCanvas.SetLogz()

        for Cfg in CfgList:
            Xval = Pair + Cfg.Xval
            Yval = Pair + Cfg.Yval
            H2dModel = ROOT.RDF.TH2DModel(Title, Title, Cfg.Xbins, Cfg.Xlow, Cfg.Xhigh,
                                                        Cfg.Ybins, Cfg.Ylow, Cfg.Yhigh)
            H2d = RDFPassCuts.Histo2D(H2dModel, Xval, Yval, "weight")
            H2d.GetXaxis().SetTitle(Xval)
            H2d.GetYaxis().SetTitle(Yval)
    
            H2dPfX = H2d.ProfileX()
            H2dPfX.SetLineColor(ROOT.kRed)
    
            H2d.Draw("colz")
            H2dPfX.Draw("same")
    
            MyCanvas.SaveAs(ResultsDir + Yval + "_vs_" + Xval + "_" + Cuts + "_" + str(Mass) + "GeV.png")
