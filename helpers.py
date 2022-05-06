#!/usr/env python

import numpy as np
import nibabel as nb
import mne

def read_fif(fpath):
    """Return mne.evoked.Evoked structure given a fpath.

    Args:
        fpath (str): path to .fif file

    Returns:
        mne.evoked.Evoked: _description_
    """

    ave=mne.read_evokeds(fpath)
    ave=ave[0]
    ave.pick_types(meg=True, ref_meg=False)
    return ave

def get_regions(ave):
    """Retrieve list of regions for specifying vector order.

    Args:
        ave (mne.evoked.Evoked): _description_

    Returns:
        list: list of regions
    """

    return list(set([i[1:3] for i in ave.info["ch_names"]]))

def compute_lfp_vector(order, ave):
    """Return ordered 1D vector of LFPs.

    Args:
        order (list): order of channel regions
        ave (mne.evoked.Evoked): _description_

    Returns:
        np.array: 1D vector of LFPs in order
    """

    ave_data = ave._data
    region_dict = {}

    # divide ave_data into regions
    for i, ch_name in enumerate(ave.info.ch_names):
        region = ch_name[1:3]
        try:
            assert region_dict[region].size > 0
            region_dict[region] = np.vstack((region_dict[region],ave_data[i,:]))
        except KeyError:
            region_dict.setdefault(region, ave_data[i,:])

    # average regions
    lfp_dict = {region: np.average(arr, axis=0) for region, arr in region_dict.items()}

    # concatenate into 1D array in given "order"

    lfp_vector = np.array(())
    for region in order:
        lfp_vector = np.hstack((lfp_vector, lfp_dict[region]))

    return lfp_vector


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