#lowercase with underline for function/class names
#canmel case for variables

import ROOT as rt

BaseName = "trigger"
BaseFileList = ["Hists_all_cuts.root"]
#BaseHistList = ["ML_Eff_Trig_Hist"]
BaseHistList = ["ML_Trig_Acceptence_Hist"]

Comp1Name = "trigger + dR + dEta + massAsymm"
Comp1FileList = ["Hists_all_cuts.root"]
#Comp1HistList = ["ML_Eff_Final_Hist"]
Comp1HistList = ["ML_Final_Acceptence_Hist"]

Comp2Name = "trigger + ML tight"
Comp2FileList = ["Hists_ML_cut.root"]
#Comp2HistList = ["ML_Eff_Final_Hist"]
Comp2HistList = ["ML_Final_Acceptence_Hist"]

ShapeComp = False
SetLogY = False

#YTitle = "Pairing Efficiency"
YTitle = "Cut Acceptence"
XTitle = "Gen Mass [GeV]"
#XTitle = "nConstituents"

InputList = [500, 600, 700, 800, 900, 1000, 1250, 1500, 1750, 2000, 2500, 3000]

XMin = 0
XMax = 0
YScale = 1.5

FileDir = "results_temp/"
HistDir = ""

if ShapeComp: YTitle = "A.U."

class MyStruct:
    def __init__(self, Name, FileList, HistList, Color, StructList):
        self.Name = Name
        self.FileList = FileList
        self.HistList = HistList
        self.Color = Color
        StructList.append(self)

StructList = []
Base = MyStruct(BaseName, BaseFileList, BaseHistList, rt.kBlue, StructList)
Comp1 = MyStruct(Comp1Name, Comp1FileList, Comp1HistList, rt.kGreen+1, StructList)
Comp2 = MyStruct(Comp2Name, Comp2FileList, Comp2HistList, rt.kRed, StructList)
#Comp3 = MyStruct(Comp3Name, Comp3FileList, Comp3HistList, rt.kYellow+1, StructList)

rt.TH1.AddDirectory(rt.kFALSE)
#rt.TH1.__init__._creates = False

for i in range(len(BaseFileList)):
    for j in range(len(BaseHistList)):
        MyCanvas = rt.TCanvas("MyCanvas", "MyCanvas", 600, 600)
        rt.gStyle.SetOptStat(rt.kFALSE)

        MyLeg = rt.TLegend(0.3,0.65,0.9,0.9)

        PadUp = rt.TPad("PadUp", "PadUp", 0, 0.3, 1, 1.0)
        PadUp.SetBottomMargin(0.01)
        PadUp.Draw()

        PadDown = rt.TPad("PadDown", "PadDown", 0, 0, 1, 0.3)
        PadDown.SetTopMargin(0.03)
        PadDown.SetBottomMargin(0.3)
        PadDown.SetGrid()
        PadDown.Draw()

        OutName = BaseFileList[i].replace(".root", "_")
        BaseHist = None

        for k in range(len(StructList)):
            iFileName = StructList[k].FileList[i]
            iHistName = StructList[k].HistList[j]
            OutName = OutName + iHistName.replace("_h", "_")
            iFile = rt.TFile.Open(FileDir + iFileName)
            iHist = iFile.Get(HistDir + iHistName)
            print k, iHist
            iHist.SetLineColor(StructList[k].Color)
            iHist.Sumw2()
            if ShapeComp: iHist.Scale(1/iHist.GetEntries())
            MyLeg.AddEntry(iHist, StructList[k].Name, "l")

            MyCanvas.cd()
            PadUp.cd()

            YMaxTemp = iHist.GetMaximum() * YScale
            if k == 0:
                BaseHist = iHist.Clone()

                BaseHist.GetYaxis().SetTitle(YTitle)
                BaseHist.SetMaximum(YMaxTemp)
                BaseHist.SetMinimum(0)
                BaseHist.SetTitle("")
                if XMax > 0:
                    BaseHist.GetXaxis().SetRangeUser(XMin, XMax)
                BaseHist.Draw("hist")

                MyCanvas.cd()
                PadDown.cd()
                BaseFrame = BaseHist.Clone()
                BaseFrame.Reset()

                BaseFrame.GetYaxis().SetTitle("Ratio")
                BaseFrame.GetYaxis().SetTitleOffset(0.4)
                BaseFrame.GetYaxis().SetTitleSize(0.1)
                BaseFrame.GetYaxis().SetLabelSize(0.08)
                BaseFrame.GetYaxis().SetRangeUser(0, 2)

                BaseFrame.GetXaxis().SetTitle(XTitle)
                BaseFrame.GetXaxis().SetTitleOffset(0.8)
                BaseFrame.GetXaxis().SetTitleSize(0.1)
                BaseFrame.GetXaxis().SetLabelSize(0.08)
                if len(InputList) > 0:
                    for Bin, Lable in enumerate(InputList):
                        BaseFrame.GetXaxis().SetBinLabel(Bin+1, str(Lable))
                BaseFrame.Draw()

                MyLine = rt.TLine(BaseFrame.GetXaxis().GetXmin(), 1.0, BaseFrame.GetXaxis().GetXmax(), 1.0)
                MyLine.Draw()
            else:
                if YMaxTemp > BaseHist.GetMaximum(): 
                    BaseHist.SetMaximum(YMaxTemp)
                iHist.Draw("histsame")

                MyCanvas.cd()
                PadDown.cd()
                RatioHist = iHist.Clone()
                rt.SetOwnership(RatioHist, False)
                RatioHist.Divide(BaseHist)
                RatioHist.Draw("histsame")

        MyCanvas.cd()
        PadUp.cd()
        if SetLogY: PadUp.SetLogy()
        MyLeg.Draw()
        MyCanvas.SaveAs("results_temp/" + OutName + ".png")

