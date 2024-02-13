import uproot
print("uproot version: ", uproot.__version__)

import tensorflow as tf
print("tensorflow version: ", tf.__version__)
print("running on GPU: ", tf.test.is_built_with_cuda())

#InputList = [500]
InputList = [500, 600, 700, 800, 900, 1000, 1250, 1500, 1750, 2000, 2500, 3000]
#InputList = ["QCD_2M_stride30"]
#InputList = ["Ms2000_Mc500", "Ms4000_Mc1000", "Ms6000_Mc1600", "Ms8000_Mc2000", "Ms9000_Mc2250", "Ms8000_Mc3000"]

ReadList = ["fourjetmasstev", "P1high_MTeV", "P1low_MTeV", "P1high_dR", "P1low_dR",
                              "P2high_MTeV", "P2low_MTeV", "P2high_dR", "P2low_dR",
                              "P3high_MTeV", "P3low_MTeV", "P3high_dR", "P3low_dR"]

CNNInputs = ["fourjetmasstev", "P1high_MTeV", "P1low_MTeV", "P1high_dR", "P1low_dR",
             "fourjetmasstev", "P2high_MTeV", "P2low_MTeV", "P2high_dR", "P2low_dR",
             "fourjetmasstev", "P3high_MTeV", "P3low_MTeV", "P3high_dR", "P3low_dR"]

#DijetModelDir = "results/results_quad_sum_mass_diff_CNN_more/"
#SigBGModelDir = "results/results_SigBG_CNN_more/"
DijetModelDir = "results/results_ResAndNonres_CNN_more/"
SigBGModelDir = "results/results_ResAndNonres_SigBG_CNN_more/"

DijetModel = tf.keras.models.load_model(DijetModelDir + "Model.h5")
#DijetModel.summary()
SigBGModel = tf.keras.models.load_model(SigBGModelDir + "Model.h5")
#SigBGModel.summary()

for Input in InputList:
    FileName = "ML_TTree/tree_ML_MCRun2_"
    if isinstance(Input, str):
        FileName = FileName + Input  + ".root"
    else:
        FileName = FileName + str(Input) + "GeV.root"

    print("Processing", FileName)
    Events = uproot.open(FileName)["tree_ML"]

    InputPD = Events.arrays(ReadList, library="pd")
    InputArrays = InputPD[CNNInputs].to_numpy()
    #print(InputArrays.dtype)
    print(InputArrays.shape)
    print(InputArrays[0])

    DijetPred = DijetModel.predict(InputArrays, batch_size = 5000)
    #print(DijetPred.dtype)
    print(DijetPred.shape)
    print(DijetPred[0])

    SigBGPred = SigBGModel.predict(InputArrays, batch_size = 5000)
    #print(SigBGPred.dtype)
    print(SigBGPred.shape)
    print(SigBGPred[0])

    with uproot.recreate(FileName.replace(".root","_ML.root")) as OutputFile:
        OutputFile["tree_ML"] = {"P1_ML": DijetPred[:,0], "P2_ML": DijetPred[:,1], "P3_ML": DijetPred[:,2],
                                 "SigBG_ML": SigBGPred[:, 1]}
