#!/usr/env python

from pathlib import PosixPath

import numpy as np
import nibabel as nb
import mne
mne.set_log_level('warning')


def read_fif(fpath):
    """Return mne.evoked.Evoked structure given a fpath.

    Args:
        fpath (str): path to .fif file

    Returns:
        mne.evoked.Evoked: _description_
    """

    ave=mne.read_evokeds(fpath, verbose=False)
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

def concatenate_subjs(subjs, data_dir):
    """Retrieve and merge subject LFP and FA vectors.

    Args:
        subjs (list): list of subjects
        data_dir (posix.Path): path to data directory

    Returns:
        tuple: np.array of all FA values (n_voxels, n_subjs) ,
               np.array of all LFP values (n_timepoints*n_regions, n_subjs)
    """

    assert type(data_dir) == PosixPath
    assert type(subjs) == list

    master_fa_arr = np.array(())
    master_lfp_arr = np.array(())
    n_subjs = 0; first_subj = True

    for subj in subjs:

        meg_path = data_dir / (subj + "_ses-01_task-haririhammer_ave.fif")
        fa_path = data_dir / (subj + "_FA_tlrc.nii")

        if (not meg_path.exists) or (not fa_path.exists):
            print(f"{subj} does not have both MEG and FA files. Skipping...")
            continue
        else:
            n_subjs += 1

        # retrieve MEG data
        ave = read_fif(meg_path)

        # use first subject's region order as standard across subjects
        if first_subj:
            order = get_regions(ave)
            first_subj = False

        lfp_vector = compute_lfp_vector(order, ave)

        # retrieve FA data
        fa_vector = read_fa_map(fa_path)

        # merge arrays
        master_fa_arr = np.hstack((master_fa_arr, fa_vector))
        master_lfp_arr = np.hstack((master_lfp_arr, lfp_vector))

    out_fa = np.reshape(master_fa_arr, (n_subjs, -1))
    out_lfp = np.reshape(master_lfp_arr, (n_subjs, -1))

    return out_fa, out_lfp