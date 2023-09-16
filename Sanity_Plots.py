import ROOT
ROOT.ROOT.EnableImplicitMT()
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)

#MassList = [500]
MassList = [500, 600, 700, 800, 900, 1000, 1250, 1500, 1750, 2000, 2500, 3000]
InputDir = "ML_TTree/"
ResultsDir = "results_temp/"

MyChain = ROOT.TChain("tree_ML")
for Mass in MassList:
    RootFile = "tree_ML_MCRun2_" + str(Mass) + "GeV.root"
    print "processing ", RootFile
    MyChain.Add(InputDir + RootFile)

RDF = ROOT.RDataFrame(MyChain)

MassPlotList = MassList + [-1]
for Idx, MassPlot in enumerate(MassPlotList):
    RDFTemp = RDF
    Title = "Gen mass all"
    Xlow = 0
    Xhigh = 10
    if MassPlot != -1:
        RDFTemp = RDFTemp.Filter("Mass == " + str(MassPlot))
        Title = Title.replace("all", str(MassPlot) + " GeV")
        Xlow = MassPlot/1000.0
        Xhigh = MassPlot/1000.0 + 2.6 + 0.4 * Idx

    for P in range(3):
        ######### mjj vs m4j #########
        Mjj = "Mjj_msortedP" + str(P+1) + "_high_div4jm"
        H2dModel = ROOT.RDF.TH2DModel(Title, Title, 200, Xlow, Xhigh, 200, 0.45 - 0.2 * P, 0.8 - 0.1 * P)
        H2d = RDFTemp.Histo2D(H2dModel, "fourjetmasstev", Mjj)
        H2d.GetXaxis().SetTitle("M_{4j} [TeV]")
        H2d.GetYaxis().SetTitle(Mjj)
    
        H2dPfX = H2d.ProfileX()
        H2dPfX.Rebin(4)
        H2dPfX.SetLineColor(ROOT.kRed)
    
        H2dPfY = H2d.ProfileY()
        H2dPfY.Rebin(4)
        H2dPfY.SetLineColor(ROOT.kRed)
    
        MyCanvas = ROOT.TCanvas("MyCanvas", "MyCanvas", 600, 600)
        MyCanvas.SetLeftMargin(0.15)
        MyCanvas.SetRightMargin(0.15)
    
        H2dPfY.Draw()
        MyCanvas.SaveAs(ResultsDir + Mjj + "_vs_M4j_PfY_" + str(MassPlot) + "GeV.png")
    
        MyCanvas.SetLogz()
        H2d.Draw("colz")
        H2dPfX.Draw("same")
    
        MyCanvas.SaveAs(ResultsDir + Mjj + "_vs_M4j" + str(MassPlot) + "GeV.png")

        ######### x vs omega #########
        Omega = "omega" + str(P+1)
        X = "x" + str(P+1)
        H2dModel = ROOT.RDF.TH2DModel(Title, Title, 100, 0, 1, 100, 0, 1.5)
        H2d = RDFTemp.Histo2D(H2dModel, Omega, X)
        H2d.GetXaxis().SetTitle(Omega)
        H2d.GetYaxis().SetTitle(X)

        H2dPfX = H2d.ProfileX()
        H2dPfX.SetLineColor(ROOT.kRed)

        H2d.Draw("colz")
        H2dPfX.Draw("same")

        MyCanvas.SaveAs(ResultsDir + X + "_vs_" + Omega + "_"+ str(MassPlot) + "GeV.png") 
