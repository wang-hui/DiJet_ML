import uproot
print("uproot version: ", uproot.__version__)

import tensorflow as tf
print("tensorflow version: ", tf.__version__)
print("running on GPU: ", tf.test.is_built_with_cuda())

#InputList = [500]
InputList = [500, 600, 700, 800, 900, 1000, 1250, 1500, 1750, 2000, 2500, 3000]
#InputList = ["QCD_1M_stride70"]

InputNames = ["fourjetmasstev", "P1high_MTeV", "P1low_MTeV", "P2high_MTeV", "P2low_MTeV",
              "P3high_MTeV", "P3low_MTeV"]

ModelDir = "results/results_quad_sum_mass_diff_DNN_Dropout_0p2/"

Model = tf.keras.models.load_model(ModelDir + "Model.h5")
#Model.summary()

for Input in InputList:
    FileName = "ML_TTree/tree_ML_MCRun2_"
    if isinstance(Input, str):
        FileName = FileName + Input  + ".root"
    else:
        FileName = FileName + str(Input) + "GeV.root"

    Events = uproot.open(FileName)["tree_ML"]
    
    InputArrays = Events.arrays(InputNames, library="pd").to_numpy()
    #print(InputArrays.dtype)
    print(InputArrays.shape)
    print(InputArrays[0])
    
    OutputArrays = Model.predict(InputArrays, batch_size = 5000)
    #print(OutputArrays.dtype)
    print(OutputArrays.shape)
    print(OutputArrays[0])
    
    with uproot.recreate(FileName.replace(".root","_ML.root")) as OutputFile:
        OutputFile["tree_ML"] = {"P1_ML": OutputArrays[:,0], "P2_ML": OutputArrays[:,1], "P3_ML": OutputArrays[:,2]}
