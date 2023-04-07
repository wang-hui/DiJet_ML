import ROOT
import numpy as np

RootPath = "/eos/uscms/store/user/huiwang/Dijet/ML_TTree/"
MassList = [500, 600, 700, 800, 900, 1000]
for Mass in MassList:
    RootFile = RootPath + "tree_ML_MCRun2_" + str(Mass) + "GeV.root"
    MyFile = ROOT.TFile(RootFile)
    MyTree = MyFile.Get("tree_ML")
    
    OutFile = open("tree_ML_MCRun2_" + str(Mass) + "GeV.csv", "w")
    OutFile.write("M4, R1, R2, R3, Truth, Mass\n")
    
    for i, Event in enumerate(MyTree):
        #if i > 10:
        #    break
        M4 = Event.fourjetmasstev
        R1 = Event.Mjj_msortedP1_high_div4jm
        R2 = Event.Mjj_msortedP2_high_div4jm
        R3 = Event.Mjj_msortedP3_high_div4jm
        Truth = np.argmin(np.abs(np.array([R1, R2, R3])-(Mass/1000.0)/M4))
        OutFile.write(str(M4) + ", " + str(R1) + ", " + str(R2) + ", " + str(R3) + ", " + str(Truth) + ", " + str(Mass) + "\n")

    OutFile.close()
    MyFile.Close()
