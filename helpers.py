#!/usr/env python

import numpy as np
import nibabel as nb

def read_fa_map(fpath):
    """Return vectorized FA map.

    Args:
        fpath (str): path to standard space FA map

    Returns:
        np.array: 1D vector of FA map values
    """

    img = nb.load(fpath)
    data = img.get_fdata()
    return np.reshape(data, data.size)


