import ROOT
ROOT.ROOT.EnableImplicitMT()
ROOT.gInterpreter.Declare('#include "Add_to_TTree.h"')

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)

def fit_gaus (TH1):
    Mean = TH1.GetMean()
    MPV = TH1.GetXaxis().GetBinCenter(TH1.GetMaximumBin())
    RMS = TH1.GetStdDev()
    TH1.Fit("gaus", "0Q", "", Mean - 1.5*RMS, Mean + 1.5*RMS)
    #TH1.Fit("gaus", "0Q", "", MPV - 1.5*RMS, MPV + 1.5*RMS)

    F1 = TH1.GetFunction("gaus")
    C = F1.GetParameter(0)
    Mu = F1.GetParameter(1)
    Sigma = F1.GetParameter(2)

    #TH1.Fit("gaus", "Q", "", Mu - 1.5*Sigma, Mu + 1.5*Sigma)

    return Mu, Sigma

def get_acc_eff (RDF, TarName, TarHist, RefHist):
    EventsTot = RDF.Count().GetValue()
    Mu, Sigma = fit_gaus(RefHist)
    RefHist_3Sigma = RefHist.Integral(RefHist.FindBin(Mu-3*Sigma), RefHist.FindBin(Mu+3*Sigma))
    RefHistEff = RefHist_3Sigma / EventsTot

    TarHist_3Sigma = TarHist.Integral(TarHist.FindBin(Mu-3*Sigma), TarHist.FindBin(Mu+3*Sigma))
    TarHistEff = TarHist_3Sigma /  EventsTot

    RDF_temp = RDF.Filter(TarName + " == Truth_QSMD")
    EventsMatch = RDF_temp.Count().GetValue()
    TarHistAcc = float(EventsMatch) / EventsTot

    print("TruthEff %.2f" %RefHistEff, TarName + " Eff %.2f" % TarHistEff, TarName + " Acc %.2f" % TarHistAcc)
    return RefHistEff, TarHistEff, TarHistAcc

def evaluate_rdf (ML_pair_RDF, dR_pair_RDF, Name):
    NpCol = ML_pair_RDF.AsNumpy(["Mass"])
    Mass = NpCol["Mass"][0]

    Truth_Eff = ML_Eff = ML_Acc = dR_Eff = dR_Acc = 0
    Xlow = 0
    Xhigh = 2000
    if Mass > 0:
        Xlow = Mass/4
        Xhigh = Mass*2

    Truth_QSMD_M = ML_pair_RDF.Histo1D(ROOT.RDF.TH1DModel("Truth_QSMD_M", "Truth_QSMD_M", 100, Xlow, Xhigh),
                    "Truth_QSMD_M", "weight")
    ML_pair_M = ML_pair_RDF.Histo1D(ROOT.RDF.TH1DModel("ML_pair_M", "ML_pair_M", 100, Xlow, Xhigh),
                    "ML_pair_M", "weight")
    ML_pair_val = ML_pair_RDF.Histo1D(ROOT.RDF.TH1DModel("ML_pair_val", "ML_pair_val", 50, 0.3, 1.0),
                    "ML_pair_val", "weight")
    dR_pair_M = dR_pair_RDF.Histo1D(ROOT.RDF.TH1DModel("dR_pair_M", "dR_pair_M", 100, Xlow, Xhigh),
                    "dR_pair_M", "weight")

    MyCanvas = ROOT.TCanvas("MyCanvas", "MyCanvas", 600, 600)
    MyCanvas.SetLeftMargin(0.15)
    MyCanvas.SetRightMargin(0.1)

    ML_pair_M.Draw("e")
    ML_pair_M.SetTitle("QCD " + Name)
    ML_pair_M.GetXaxis().SetTitle("Average dijet mass [GeV]")
    ML_pair_M.GetYaxis().SetTitle("Events")
    ML_pair_M.SetLineColor(ROOT.kRed)

    dR_pair_M.Scale(ML_pair_M.GetEntries() / dR_pair_M.GetEntries())
    dR_pair_M.Draw("esame")
    dR_pair_M.SetLineColor(ROOT.kBlue)

    MyLeg = ROOT.TLegend(0.6,0.7,0.9,0.9)
    MyLeg.AddEntry(ML_pair_M.GetPtr(), "ML pairing", "le")
    MyLeg.AddEntry(dR_pair_M.GetPtr(), "dR pairing", "le")

    if Mass > 0:
        Truth_QSMD_M.Draw("esame")
        Truth_QSMD_M.SetLineColor(ROOT.kGreen+1)
        MyLeg.AddEntry(Truth_QSMD_M.GetPtr(), "Truth", "le")
        ML_pair_M.SetTitle("Gen mass " + str(Mass) + "GeV " + Name)
        ML_pair_M.SetMaximum(Truth_QSMD_M.GetMaximum() * 1.2)

        Truth_Eff, ML_Eff, ML_Acc = get_acc_eff (ML_pair_RDF, "ML_pair", ML_pair_M, Truth_QSMD_M)
        Truth_Eff, dR_Eff, dR_Acc = get_acc_eff (dR_pair_RDF, "dR_pair", dR_pair_M, Truth_QSMD_M)

    MyLeg.Draw()
    MyCanvas.SaveAs("results_temp/M2jAvg_" + Name + "_" + str(Mass) + "GeV.png")

    #ML_pair_val.Draw()
    #MyCanvas.SaveAs("results_temp/ML_pair_val_" + Name + "_" + str(Mass) + "GeV.png")

    return (Truth_Eff, ML_Eff, ML_Acc, dR_Eff, dR_Acc)

def get_first_last_acceptance (RDF):
    CutReport = RDF.Report()
    CutIter = iter(CutReport)
    CutFirst = next(CutIter)
    CutLast = None
    for Cut in CutReport:
        CutLast = Cut

    return float(CutFirst.GetPass()) / CutFirst.GetAll(), float(CutLast.GetPass()) / CutFirst.GetAll()

################### config #######################

#cut values for tight(0.01), medium(0.05), and loose(0.1)
#SigBG_ML_Thresholds = [0.9426, 0.8016, 0.6509]       #trained with QCD and resonant signals
SigBG_ML_Thresholds = [0.9497, 0.8174, 0.6807]       #trained with QCD and resonant and nonresonant signals
SigBG_ML_Threshold = str(SigBG_ML_Thresholds[1])

AlphaBins = [0.15, 0.25, 0.35, 0.5]
AlphaCutLow = "ML_pair_Alpha > " + str(AlphaBins[0]) + " && ML_pair_Alpha < " + str(AlphaBins[1])
AlphaCutMed = "ML_pair_Alpha > " + str(AlphaBins[1]) + " && ML_pair_Alpha < " + str(AlphaBins[2])
AlphaCutHigh = "ML_pair_Alpha > " + str(AlphaBins[2]) + " && ML_pair_Alpha < " + str(AlphaBins[3])

#InputList = [500]
InputList = [500, 600, 700, 800, 900, 1000, 1250, 1500, 1750, 2000, 2500, 3000]
#InputList = ["QCD_2M_stride30"]
#InputList = ["Ms2000_Mc500", "Ms4000_Mc1000", "Ms6000_Mc1600", "Ms8000_Mc2000", "Ms9000_Mc2250", "Ms8000_Mc3000"]

#cut flow
cut_ML = True
cut_Alpha = False

cut_dR = False
cut_dEta = False
cut_Masym = False

Nbins = len(InputList)
InputDir = "ML_TTree/"

Truth_Eff_Trig_Hist = ROOT.TH1F("Truth_Eff_Trig_Hist", "Truth_Eff_Trig_Hist", Nbins, 0.5, Nbins + 0.5)
ML_Eff_Trig_Hist = ROOT.TH1F("ML_Eff_Trig_Hist", "ML_Eff_Trig_Hist", Nbins, 0.5, Nbins + 0.5)
ML_Acc_Trig_Hist = ROOT.TH1F("ML_Acc_Trig_Hist", "ML_Acc_Trig_Hist", Nbins, 0.5, Nbins + 0.5)
dR_Eff_Trig_Hist = ROOT.TH1F("dR_Eff_Trig_Hist", "dR_Eff_Trig_Hist", Nbins, 0.5, Nbins + 0.5)
dR_Acc_Trig_Hist = ROOT.TH1F("dR_Acc_Trig_Hist", "dR_Acc_Trig_Hist", Nbins, 0.5, Nbins + 0.5)
ML_Trig_Acceptance_Hist = ROOT.TH1F("ML_Trig_Acceptance_Hist", "ML_Trig_Acceptance_Hist", Nbins, 0.5, Nbins + 0.5)
dR_Trig_Acceptance_Hist = ROOT.TH1F("dR_Trig_Acceptance_Hist", "dR_Trig_Acceptance_Hist", Nbins, 0.5, Nbins + 0.5)

Truth_Eff_Final_Hist = ROOT.TH1F("Truth_Eff_Final_Hist", "Truth_Eff_Final_Hist", Nbins, 0.5, Nbins + 0.5)
ML_Eff_Final_Hist = ROOT.TH1F("ML_Eff_Final_Hist", "ML_Eff_Final_Hist", Nbins, 0.5, Nbins + 0.5)
ML_Acc_Final_Hist = ROOT.TH1F("ML_Acc_Final_Hist", "ML_Acc_Final_Hist", Nbins, 0.5, Nbins + 0.5)
dR_Eff_Final_Hist = ROOT.TH1F("dR_Eff_Final_Hist", "dR_Eff_Final_Hist", Nbins, 0.5, Nbins + 0.5)
dR_Acc_Final_Hist = ROOT.TH1F("dR_Acc_Final_Hist", "dR_Acc_Final_Hist", Nbins, 0.5, Nbins + 0.5)
ML_Final_Acceptance_Hist = ROOT.TH1F("ML_Final_Acceptance_Hist", "ML_Final_Acceptance_Hist", Nbins, 0.5, Nbins + 0.5)
dR_Final_Acceptance_Hist = ROOT.TH1F("dR_Final_Acceptance_Hist", "dR_Final_Acceptance_Hist", Nbins, 0.5, Nbins + 0.5)

for Idx, Input in enumerate(InputList):
    FileName = "tree_ML_MCRun2_"
    if isinstance(Input, str):
        FileName = FileName + Input  + ".root"
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

    for Pair in ["P1", "P2", "P3"]:
        RDF = RDF.Define(Pair + "high_M", Pair + "high_MTeV * 1000")
        RDF = RDF.Define(Pair + "low_M", Pair + "low_MTeV * 1000")
        RDF = RDF.Define(Pair + "_M", "(" + Pair + "high_M + " + Pair + "low_M)/2")
        RDF = RDF.Define(Pair + "_QSMD", "TMath::Sq(" + Pair +
                        "high_M - Mass) + TMath::Sq(" + Pair + "low_M - Mass)")

    RDF = RDF.Define("Truth_QSMD", "min_index(P1_QSMD, P2_QSMD, P3_QSMD)")
    RDF = RDF.Define("dR_pair", "min_index(abs(P1_M - Mjj_avg_dRpairing_GeV)," +
                     "abs(P2_M - Mjj_avg_dRpairing_GeV), abs(P3_M - Mjj_avg_dRpairing_GeV))")
    RDF = RDF.Define("ML_pair", "max_index_val(P1_ML, P2_ML, P3_ML).first")
    RDF = RDF.Define("ML_pair_val", "max_index_val(P1_ML, P2_ML, P3_ML).second")

    RDF = RDF.Define("Truth_QSMD_M", "col_index<float>(P1_M, P2_M, P3_M, Truth_QSMD)")
    RDF = RDF.Define("dR_pair_M", "col_index<float>(P1_M, P2_M, P3_M, dR_pair)")
    RDF = RDF.Define("ML_pair_M", "col_index<float>(P1_M, P2_M, P3_M, ML_pair)")

    RDF = RDF.Define("ML_pair_Alpha", "ML_pair_M / fourjetmasstev / 1000")

    print ("Trig cut")
    RDF = RDF.Filter("evt_trig == 1", "cut_Trig")
    # order: Truth_Eff, ML_Eff, ML_Acc, dR_Eff, dR_Acc
    EffAccTuple = evaluate_rdf(RDF, RDF, "cut_Trig")
    Truth_Eff_Trig_Hist.SetBinContent(Idx + 1, EffAccTuple[0])
    ML_Eff_Trig_Hist.SetBinContent(Idx + 1, EffAccTuple[1])
    ML_Acc_Trig_Hist.SetBinContent(Idx + 1, EffAccTuple[2])
    dR_Eff_Trig_Hist.SetBinContent(Idx + 1, EffAccTuple[3])
    dR_Acc_Trig_Hist.SetBinContent(Idx + 1, EffAccTuple[4])

    # ML cut
    if cut_ML:
        RDF = RDF.Filter("SigBG_ML > " + SigBG_ML_Threshold, "cut_ML")
        print ("ML cut")
        EffAccTuple = evaluate_rdf(RDF, RDF, "cut_ML")
        if cut_Alpha:
            RDF_AlphaLow = RDF.Filter(AlphaCutLow, "cut_AlphaLow")
            EffAccTemp = evaluate_rdf(RDF_AlphaLow, RDF_AlphaLow, "cut_AlphaLow")

            RDF_AlphaMed = RDF.Filter(AlphaCutMed, "cut_AlphaMed")
            EffAccTemp = evaluate_rdf(RDF_AlphaMed, RDF_AlphaMed, "cut_AlphaMed")

            RDF_AlphaHigh = RDF.Filter(AlphaCutHigh, "cut_AlphaHigh")
            EffAccTemp = evaluate_rdf(RDF_AlphaHigh, RDF_AlphaHigh, "cut_AlphaHigh")

    RDF = RDF.Define("P1JetsVec", "to_vec(P1high_j1, P1high_j2, P1low_j1, P1low_j2)")
    RDF = RDF.Define("P2JetsVec", "to_vec(P2high_j1, P2high_j2, P2low_j1, P2low_j2)")
    RDF = RDF.Define("P3JetsVec", "to_vec(P3high_j1, P3high_j2, P3low_j1, P3low_j2)")

    RDF = RDF.Define("ML_pair_Jets", "col_index<std::vector<lvec>>(P1JetsVec, P2JetsVec, P3JetsVec, ML_pair)")
    RDF = RDF.Define("ML_pair_dR1", "ROOT::Math::VectorUtil::DeltaR(ML_pair_Jets[0], ML_pair_Jets[1])")
    RDF = RDF.Define("ML_pair_dR2", "ROOT::Math::VectorUtil::DeltaR(ML_pair_Jets[2], ML_pair_Jets[3])")

    RDF = RDF.Define("dR_pair_Jets", "col_index<std::vector<lvec>>(P1JetsVec, P2JetsVec, P3JetsVec, dR_pair)")
    RDF = RDF.Define("dR_pair_dR1", "ROOT::Math::VectorUtil::DeltaR(dR_pair_Jets[0], dR_pair_Jets[1])")
    RDF = RDF.Define("dR_pair_dR2", "ROOT::Math::VectorUtil::DeltaR(dR_pair_Jets[2], dR_pair_Jets[3])")

    RDF = RDF.Define("ML_pair_Phigh_lvec", "ML_pair_Jets[0] + ML_pair_Jets[1]")
    RDF = RDF.Define("ML_pair_Plow_lvec", "ML_pair_Jets[2] + ML_pair_Jets[3]")
    RDF = RDF.Define("dR_pair_Phigh_lvec", "dR_pair_Jets[0] + dR_pair_Jets[1]")
    RDF = RDF.Define("dR_pair_Plow_lvec", "dR_pair_Jets[2] + dR_pair_Jets[3]")

    ML_pair_RDF = RDF
    dR_pair_RDF = RDF

    # dR cut
    if cut_dR:
        ML_pair_RDF = ML_pair_RDF.Filter("ML_pair_dR1 < 2 && ML_pair_dR2 < 2", "ML_pair_cut_dR")
        dR_pair_RDF = dR_pair_RDF.Filter("dR_pair_dR1 < 2 && dR_pair_dR2 < 2", "dR_pair_cut_dR")
        print ("dR cut")
        EffAccTuple = evaluate_rdf(ML_pair_RDF, dR_pair_RDF, "cut_dR")

    # dEta cut
    if cut_dEta:
        ML_pair_RDF = ML_pair_RDF.Filter("abs(ML_pair_Phigh_lvec.Eta() - ML_pair_Plow_lvec.Eta()) < 1.1",
                                        "ML_pair_cut_dEta")
        dR_pair_RDF = dR_pair_RDF.Filter("abs(dR_pair_Phigh_lvec.Eta() - dR_pair_Plow_lvec.Eta()) < 1.1",
                                        "dR_pair_cut_dEta")
        print ("dEta cut")
        EffAccTuple = evaluate_rdf(ML_pair_RDF, dR_pair_RDF, "cut_dEta")

    # Masym cut
    if cut_Masym:
        ML_pair_RDF = ML_pair_RDF.Filter("abs(ML_pair_Phigh_lvec.M() - ML_pair_Plow_lvec.M()) /" + 
                        "(ML_pair_Phigh_lvec.M() + ML_pair_Plow_lvec.M()) < 0.1", "ML_pair_cut_Masym")
        dR_pair_RDF = dR_pair_RDF.Filter("abs(dR_pair_Phigh_lvec.M() - dR_pair_Plow_lvec.M()) /" + 
                        "(dR_pair_Phigh_lvec.M() + dR_pair_Plow_lvec.M()) < 0.1", "dR_pair_cut_Masym")
        print ("Masym cut")
        EffAccTuple = evaluate_rdf(ML_pair_RDF, dR_pair_RDF, "cut_Masym")

    # order: Truth_Eff, ML_Eff, ML_Acc, dR_Eff, dR_Acc
    Truth_Eff_Final_Hist.SetBinContent(Idx + 1, EffAccTuple[0])
    ML_Eff_Final_Hist.SetBinContent(Idx + 1, EffAccTuple[1])
    ML_Acc_Final_Hist.SetBinContent(Idx + 1, EffAccTuple[2])
    dR_Eff_Final_Hist.SetBinContent(Idx + 1, EffAccTuple[3])
    dR_Acc_Final_Hist.SetBinContent(Idx + 1, EffAccTuple[4])

    print("ML pair acceptance")
    ML_Trig_Acceptance, ML_Final_Acceptance = get_first_last_acceptance(ML_pair_RDF)
    ML_Trig_Acceptance_Hist.SetBinContent(Idx + 1, ML_Trig_Acceptance)
    ML_Final_Acceptance_Hist.SetBinContent(Idx + 1, ML_Final_Acceptance)
    print(ML_Trig_Acceptance, ML_Final_Acceptance)
    MLReport = ML_pair_RDF.Report()
    MLReport.Print()

    print("dR pair acceptance")
    dR_Trig_Acceptance, dR_Final_Acceptance = get_first_last_acceptance(dR_pair_RDF)
    dR_Trig_Acceptance_Hist.SetBinContent(Idx + 1, dR_Trig_Acceptance)
    dR_Final_Acceptance_Hist.SetBinContent(Idx + 1, dR_Final_Acceptance)
    print(dR_Trig_Acceptance, dR_Final_Acceptance)
    dRReport = dR_pair_RDF.Report()
    dRReport.Print()

if Nbins > 1:
    Hists = ROOT.TFile("results_temp/Hists.root", "recreate")
    Truth_Eff_Trig_Hist.Write()
    ML_Eff_Trig_Hist.Write()
    ML_Acc_Trig_Hist.Write()
    dR_Eff_Trig_Hist.Write()
    dR_Acc_Trig_Hist.Write()
    ML_Trig_Acceptance_Hist.Write()
    dR_Trig_Acceptance_Hist.Write()

    Truth_Eff_Final_Hist.Write()
    ML_Eff_Final_Hist.Write()
    ML_Acc_Final_Hist.Write()
    dR_Eff_Final_Hist.Write()
    dR_Acc_Final_Hist.Write()
    ML_Final_Acceptance_Hist.Write()
    dR_Final_Acceptance_Hist.Write()
