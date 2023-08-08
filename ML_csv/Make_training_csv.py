import ROOT
import numpy as np

RootPath = "/eos/uscms/store/user/huiwang/Dijet/ML_TTree/"
MassList = [500, 600, 700, 800, 900, 1000]
for Mass in MassList:
    RootFile = RootPath + "tree_ML_MCRun2_" + str(Mass) + "GeV.root"
    print "processing ", RootFile
    MyFile = ROOT.TFile(RootFile)
    MyTree = MyFile.Get("tree_ML")
    
    OutFile = open("tree_ML_MCRun2_" + str(Mass) + "GeV.csv", "w")
    OutFile.write("M4, R1, R2, R3, P1M, P2M, P3M, dRi, Truth_high, Truth_avg, Mass\n")
    
    for i, Event in enumerate(MyTree):
        #if i > 10:
        #    break
        PassTrig = Event.evt_trig
        if not PassTrig:
            continue

        M4 = Event.fourjetmasstev
        R1 = Event.Mjj_msortedP1_high_div4jm
        R2 = Event.Mjj_msortedP2_high_div4jm
        R3 = Event.Mjj_msortedP3_high_div4jm

        P1M1 = Event.Mjj_msortedP1_high
        P1M2 = Event.Mjj_msortedP1_low
        P2M1 = Event.Mjj_msortedP2_high
        P2M2 = Event.Mjj_msortedP2_low
        P3M1 = Event.Mjj_msortedP3_high
        P3M2 = Event.Mjj_msortedP3_low

        P1M = (P1M1+P1M2)/2
        P2M = (P2M1+P2M2)/2
        P3M = (P3M1+P3M2)/2
        AMarray = np.array([P1M, P2M, P3M])

        dRM = Event.Mjj_avg_dRpairing_GeV
        dRi = np.argmin(np.abs(AMarray - dRM))
        dRiM = AMarray[dRi]
        if abs(dRM - dRiM) / dRM > 0.0001:
            print P1M, P2M, P3M, dRM, dRi

        Truth_high = np.argmin(np.abs(np.array([R1, R2, R3])-(Mass/1000.0)/M4))
        Truth_avg = np.argmin(np.abs(AMarray - Mass))
        OutFile.write(str(M4) + ", " + str(R1) + ", " + str(R2) + ", " + str(R3) + ", " 
                    + str(P1M) + ", " + str(P2M) + ", " + str(P3M) + ", " + str(dRi) + ", " 
                    + str(Truth_high) + ", " + str(Truth_avg) + ", " + str(Mass) + "\n")

    OutFile.close()
    MyFile.Close()
