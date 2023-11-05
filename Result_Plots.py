import ROOT
ROOT.ROOT.EnableImplicitMT()
ROOT.gInterpreter.Declare('#include "Add_to_TTree.h"')

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)

def fit_gaus (TH1):
    Mean = TH1.GetMean()
    MPV = TH1.GetXaxis().GetBinCenter(TH1.GetMaximumBin())
    RMS = TH1.GetStdDev()
    #TH1.Fit("gaus", "0Q", "", Mean - 1.5*RMS, Mean + 1.5*RMS)
    TH1.Fit("gaus", "0Q", "", MPV - 1.5*RMS, MPV + 1.5*RMS)

    F1 = TH1.GetFunction("gaus")
    C = F1.GetParameter(0)
    Mu = F1.GetParameter(1)
    Sigma = F1.GetParameter(2)

    TH1.Fit("gaus", "Q", "", Mu - 1.5*Sigma, Mu + 1.5*Sigma)

    return Mu, Sigma

def evaluate_rdf (RDF, Name, Mass):
    ML_Accuracy = Truth_Efficiency = ML_Efficiency = 0
    Xlow = 0
    Xhigh = 2000
    if Mass > 0:
        Xlow = Mass/4
        Xhigh = Mass*2

    Truth_QSMD_M = RDF.Histo1D(ROOT.RDF.TH1DModel("Truth_QSMD_M", "Truth_QSMD_M", 100, Xlow, Xhigh),
                    "Truth_QSMD_M", "weight")
    ML_pred_M = RDF.Histo1D(ROOT.RDF.TH1DModel("ML_pred_M", "ML_pred_M", 100, Xlow, Xhigh),
                    "ML_pred_M", "weight")
    ML_pred_val = RDF.Histo1D(ROOT.RDF.TH1DModel("ML_pred_val", "ML_pred_val", 50, 0.3, 1.0),
                    "ML_pred_val", "weight")
    fourjetmasstev = RDF.Histo1D(ROOT.RDF.TH1DModel("fourjetmasstev", "fourjetmasstev", 100, 0.0, 5.0),
                    "fourjetmasstev", "weight")

    MyCanvas = ROOT.TCanvas("MyCanvas", "MyCanvas", 600, 600)
    MyCanvas.SetLeftMargin(0.15)
    MyCanvas.SetRightMargin(0.1)

    ML_pred_M.Draw()
    ML_pred_M.SetTitle("QCD")
    ML_pred_M.GetXaxis().SetTitle("Average dijet mass [GeV]")
    ML_pred_M.GetYaxis().SetTitle("Events")
    ML_pred_M.SetLineColor(ROOT.kGreen+1)

    MyLeg = ROOT.TLegend(0.6,0.7,0.9,0.9)
    MyLeg.AddEntry(ML_pred_M.GetPtr(), "ML pred", "l")

    if Mass > 0:
        Truth_QSMD_M.Draw("same")
        MyLeg.AddEntry(Truth_QSMD_M.GetPtr(), "truth", "l")
        ML_pred_M.SetTitle("Gen mass " + str(Mass) + "GeV")
        ML_pred_M.SetMaximum(Truth_QSMD_M.GetMaximum() * 1.2)

        EventsTot = RDF.Count().GetValue()
        Mu, Sigma = fit_gaus(Truth_QSMD_M)
        Truth_QSMD_M_3Sigma = Truth_QSMD_M.Integral(
            Truth_QSMD_M.FindBin(Mu-3*Sigma), Truth_QSMD_M.FindBin(Mu+3*Sigma))
        Truth_Efficiency = Truth_QSMD_M_3Sigma / EventsTot
        ML_pred_M_3Sigma = ML_pred_M.Integral(ML_pred_M.FindBin(Mu-3*Sigma), ML_pred_M.FindBin(Mu+3*Sigma))
        ML_Efficiency = ML_pred_M_3Sigma /  EventsTot

        RDF_temp = RDF.Filter("ML_pred == Truth_QSMD")
        EventsMatch = RDF_temp.Count().GetValue()
        ML_Accuracy = float(EventsMatch) / EventsTot

        print ("ML accuracy: %.2f" %ML_Accuracy, "Truth efficiency: %.2f" %Truth_Efficiency,
                "ML efficiency: %.2f" %ML_Efficiency)

    MyLeg.Draw()
    MyCanvas.SaveAs("results_temp/M2jAvg_" + Name + "_" + str(Mass) + "GeV.png")

    ML_pred_val.Draw()
    MyCanvas.SaveAs("results_temp/ML_pred_val_" + Name + "_" + str(Mass) + "GeV.png")

    fourjetmasstev.Draw()
    MyCanvas.SaveAs("results_temp/M4jTev_" + Name + "_" + str(Mass) + "GeV.png")

    return ML_Accuracy, Truth_Efficiency, ML_Efficiency

#SaveList = [
#        "P1_Mhigh_TeV", "P1_Mlow_TeV",
#        "P2_Mhigh_TeV", "P2_Mlow_TeV",
#        "P3_Mhigh_TeV", "P3_Mlow_TeV",
#        "P1_ML", "P2_ML", "P3_ML",
#        "ML_pred_Phigh_lvec", "ML_pred_Plow_lvec"
#]

#InputList = [500]
InputList = [500, 600, 700, 800, 900, 1000, 1250, 1500, 1750, 2000, 2500, 3000]
#InputList = ["QCD_1M_stride70"]

Nbins = len(InputList)
InputDir = "ML_TTree/"
SkipGeoCut = True

ML_Accuracy_Trig = ROOT.TH1F("ML_Accuracy_Trig", "ML_Accuracy_Trig", Nbins, 0.5, Nbins + 0.5)
Truth_Efficiency_Trig = ROOT.TH1F("Truth_Efficiency_Trig", "Truth_Efficiency_Trig", Nbins, 0.5, Nbins + 0.5)
ML_Efficiency_Trig = ROOT.TH1F("ML_Efficiency_Trig", "ML_Efficiency_Trig", Nbins, 0.5, Nbins + 0.5)
ML_Accuracy_Masym = ROOT.TH1F("ML_Accuracy_Masym", "ML_Accuracy_Masym", Nbins, 0.5, Nbins + 0.5)
Truth_Efficiency_Masym = ROOT.TH1F("Truth_Efficiency_Masym", "Truth_Efficiency_Masym", Nbins, 0.5, Nbins + 0.5)
ML_Efficiency_Masym = ROOT.TH1F("ML_Efficiency_Masym", "ML_Efficiency_Masym", Nbins, 0.5, Nbins + 0.5)

for Idx, Input in enumerate(InputList):
    Mass = Input
    FileName = "tree_ML_MCRun2_"
    if isinstance(Input, str):
        FileName = FileName + Input  + ".root"
        Mass = 0
    else:
        FileName = FileName + str(Input) + "GeV.root"

    print ("=============================================")
    print ("processing " + FileName)
    MainFile = ROOT.TFile.Open(InputDir + FileName)
    MainTree = MainFile.Get("tree_ML")
    MLFile = ROOT.TFile.Open(InputDir + FileName.replace(".root", "_ML.root"))
    MLTree = MLFile.Get("tree_ML")
    MainTree.AddFriend(MLTree)

    RDF = ROOT.RDataFrame(MainTree)

    RDF = RDF.Filter("evt_trig == 1", "cut_Trig")

    RDF = RDF.Define("P1high_M", "P1high_MTeV * 1000")
    RDF = RDF.Define("P1low_M", "P1low_MTeV * 1000")
    RDF = RDF.Define("P2high_M", "P2high_MTeV * 1000")
    RDF = RDF.Define("P2low_M", "P2low_MTeV * 1000")
    RDF = RDF.Define("P3high_M", "P3high_MTeV * 1000")
    RDF = RDF.Define("P3low_M", "P3low_MTeV * 1000")

    RDF = RDF.Define("P1_M", "(P1high_M + P1low_M)/2")
    RDF = RDF.Define("P2_M", "(P2high_M + P2low_M)/2")
    RDF = RDF.Define("P3_M", "(P3high_M + P3low_M)/2")

    RDF = RDF.Define("P1_QSMD", "TMath::Sq(P1high_M - Mass) + TMath::Sq(P1low_M - Mass)")
    RDF = RDF.Define("P2_QSMD", "TMath::Sq(P2high_M - Mass) + TMath::Sq(P2low_M - Mass)")
    RDF = RDF.Define("P3_QSMD", "TMath::Sq(P3high_M - Mass) + TMath::Sq(P3low_M - Mass)")

    RDF = RDF.Define("Truth_QSMD", "min_index(P1_QSMD, P2_QSMD, P3_QSMD)")
    RDF = RDF.Define("ML_pred", "max_index_val(P1_ML, P2_ML, P3_ML).first")
    RDF = RDF.Define("ML_pred_val", "max_index_val(P1_ML, P2_ML, P3_ML).second")

    RDF = RDF.Define("Truth_QSMD_M", "col_index<float>(P1_M, P2_M, P3_M, Truth_QSMD)")
    RDF = RDF.Define("ML_pred_M", "col_index<float>(P1_M, P2_M, P3_M, ML_pred)")

    print ("Trig cut")
    ML_Accuracy, Truth_Efficiency, ML_Efficiency = evaluate_rdf(RDF, "cut_Trig", Mass)
    ML_Accuracy_Trig.SetBinContent(Idx + 1, ML_Accuracy)
    Truth_Efficiency_Trig.SetBinContent(Idx + 1, Truth_Efficiency)
    ML_Efficiency_Trig.SetBinContent(Idx + 1, ML_Efficiency)

    # dR cut
    RDF = RDF.Define("P1JetsVec", "to_vec(P1high_j1, P1high_j2, P1low_j1, P1low_j2)")
    RDF = RDF.Define("P2JetsVec", "to_vec(P2high_j1, P2high_j2, P2low_j1, P2low_j2)")
    RDF = RDF.Define("P3JetsVec", "to_vec(P3high_j1, P3high_j2, P3low_j1, P3low_j2)")
    RDF = RDF.Define("ML_pred_Jets", "col_index<std::vector<lvec>>(P1JetsVec, P2JetsVec, P3JetsVec, ML_pred)")
    RDF = RDF.Define("ML_pred_dR1", "ROOT::Math::VectorUtil::DeltaR(ML_pred_Jets[0], ML_pred_Jets[1])")
    RDF = RDF.Define("ML_pred_dR2", "ROOT::Math::VectorUtil::DeltaR(ML_pred_Jets[2], ML_pred_Jets[3])")

    if not SkipGeoCut:
        RDF = RDF.Filter("ML_pred_dR1 < 2 && ML_pred_dR2 < 2", "cut_dR")
        print ("dR cut")
        ML_Accuracy, Truth_Efficiency, ML_Efficiency = evaluate_rdf(RDF, "cut_dR", Mass)

    # dEta cut
    RDF = RDF.Define("ML_pred_Phigh_lvec", "ML_pred_Jets[0] + ML_pred_Jets[1]")
    RDF = RDF.Define("ML_pred_Plow_lvec", "ML_pred_Jets[2] + ML_pred_Jets[3]")

    if not SkipGeoCut:
        RDF = RDF.Filter("abs(ML_pred_Phigh_lvec.Eta() - ML_pred_Plow_lvec.Eta()) < 1.1", "cut_dEta")
        print ("dEta cut")
        ML_Accuracy, Truth_Efficiency, ML_Efficiency = evaluate_rdf(RDF, "cut_dEta", Mass)

    # Masym cut
    RDF = RDF.Filter("abs(ML_pred_Phigh_lvec.M() - ML_pred_Plow_lvec.M()) / (ML_pred_Phigh_lvec.M() + ML_pred_Plow_lvec.M()) < 0.1", "cut_Masym")

    print ("Masym cut")
    ML_Accuracy, Truth_Efficiency, ML_Efficiency = evaluate_rdf(RDF, "cut_Masym", Mass)
    ML_Accuracy_Masym.SetBinContent(Idx + 1, ML_Accuracy)
    Truth_Efficiency_Masym.SetBinContent(Idx + 1, Truth_Efficiency)
    ML_Efficiency_Masym.SetBinContent(Idx + 1, ML_Efficiency)

    CutReport = RDF.Report()
    CutReport.Print()

#    OutCols = ROOT.vector("string")()
#    for Col in SaveList: OutCols.push_back(Col)
#    RDF.Snapshot("tree_ML", "test.root", OutCols)

Hists = ROOT.TFile("results_temp/Hists.root", "recreate")
ML_Accuracy_Trig.Write()
Truth_Efficiency_Trig.Write()
ML_Efficiency_Trig.Write()
ML_Accuracy_Masym.Write()
Truth_Efficiency_Masym.Write()
ML_Efficiency_Masym.Write()

