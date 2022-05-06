#!/usr/env/bin python

from pathlib import Path

import numpy as np
from sklearn.decomposition import FastICA

from helpers import *

# get list of subjects
subjs_dir = Path("/data/NIMH_scratch/MEG_Hackathon/hv_bids")
fpath = subjs_dir / "subjects.txt"
subjs_arr = np.loadtxt(fpath)
subjs = list(subjs_arr)

data_dir = Path("/data/NIMH_scratch/MEG_Hackathon/DTI_MEG")
fa, lfp = concatenate_subjs(subjs, data_dir)

norm_fa = normalize_modality(fa, axis=None)
norm_lfp = normalize_modality(lfp, axis=None)

final_mat = concatenate_modalities(norm_fa, norm_lfp)

ica_model = FastICA(n_components=11)
fit_components = ica_model.fit_transform(final_mat.T)

opath = data_dir / "ica_11components.npy"
np.save(opath, arr=fit_components)