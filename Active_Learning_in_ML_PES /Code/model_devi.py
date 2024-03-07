from deepmd.infer import calc_model_devi
from deepmd.infer import DeepPot as DP
import numpy as np
import dpdata

dsys = dpdata.LabeledSystem(file_name='/work/akbarshs/MLMD/deepmd/ActiveLearning/VASP40000SCAN/AL40K50_0.15/data/AIMD/data9/',fmt= 'deepmd/npy')
#print (dsys)
coord = dsys['coords']
cell = dsys['cells']
atype = dsys['atom_types']
graphs = [DP("graph1.pb"), DP("graph2.pb"), DP("graph3.pb"), DP("graph4.pb")]
model_devi = calc_model_devi(coord, cell, atype, graphs)
