import ROOT
ROOT.ROOT.EnableImplicitMT()
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)

#MassList = [500]
MassList = [500, 600, 700, 800, 900, 1000, 1250, 1500, 1750, 2000, 2500, 3000]
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

Trig = ""
Trig = "PassTrig"

MyChain = ROOT.TChain("tree_ML")
for Mass in MassList:
    FileName = "tree_ML_MCRun2_" + str(Mass) + "GeV.root"
    MyChain.Add(InputDir + FileName)

RDF = ROOT.RDataFrame(MyChain)
if Trig != "": RDF = RDF.Filter("evt_trig == 1")

if len(MassList) > 1 : MassList += [-1]
for Mass in MassList:
    print "processing", str(Mass), "GeV"
    RDFTemp = RDF
    Title = "Gen mass all"
    if Mass != -1:
        RDFTemp = RDFTemp.Filter("Mass == " + str(Mass))
        Title = Title.replace("all", str(Mass) + " GeV")

    for P in range(3):
        Pair = "P" + str(P+1)

        MyCanvas = ROOT.TCanvas("MyCanvas", "MyCanvas", 600, 600)
        MyCanvas.SetLeftMargin(0.15)
        MyCanvas.SetRightMargin(0.15)
        MyCanvas.SetLogz()

        for Cfg in CfgList:
            Xval = Pair + Cfg.Xval
            Yval = Pair + Cfg.Yval
            H2dModel = ROOT.RDF.TH2DModel(Title, Title, Cfg.Xbins, Cfg.Xlow, Cfg.Xhigh,
                                                        Cfg.Ybins, Cfg.Ylow, Cfg.Yhigh)
            H2d = RDFTemp.Histo2D(H2dModel, Xval, Yval)
            H2d.GetXaxis().SetTitle(Xval)
            H2d.GetYaxis().SetTitle(Yval)
    
            H2dPfX = H2d.ProfileX()
            H2dPfX.SetLineColor(ROOT.kRed)
    
            H2d.Draw("colz")
            H2dPfX.Draw("same")
    
            MyCanvas.SaveAs(ResultsDir + Yval + "_vs_" + Xval + "_" + Trig + str(Mass) + "GeV.png")
