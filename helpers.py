#!/usr/env python

from pathlib import PosixPath

import numpy as np
import nibabel as nb
import mne
mne.set_log_level('warning')
from scipy.stats import zscore


def read_fif(fpath):
    """Return mne.evoked.Evoked structure given a fpath.

    Args:
        fpath (str): path to .fif file

    Returns:
        mne.evoked.Evoked: meg evoked potentials
    """

    ave=mne.read_evokeds(fpath, verbose=False)
    ave=ave[0]
    ave.pick_types(meg=True, ref_meg=False)
    return ave

def get_regions(ave):
    """Retrieve list of regions for specifying vector order.

    Args:
        ave (mne.evoked.Evoked): meg evoked potentials

    Returns:
        list: list of regions
    """

    return list(set([i[1:3] for i in ave.info["ch_names"]]))

def compute_lfp_vector(order, ave):
    """Return ordered 1D vector of LFPs.

    Args:
        order (list): order of channel regions
        ave (mne.evoked.Evoked): meg evoked potentials

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
        tuple: np.array of all FA values (n_subjs, n_voxels) ,
               np.array of all LFP values (n_subjs, n_timepoints*n_regions)
    """

    assert type(data_dir) == PosixPath
    assert type(subjs) == list

    master_fa_arr = np.array(())
    master_lfp_arr = np.array(())
    n_subjs = 0; first_subj = True

    for subj in subjs:

        meg_path = data_dir / "meg_ave" / (subj + "_ses-01_task-haririhammer_ave.fif")
        fa_path = data_dir / "dti_blur10mm" / (subj + "_FA_tlrc_blur10mm.nii")

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

def normalize_modality(modality_arr,
                       axis=None):
    """Normalize modality across subjects

    Args:
        modality_arr (np.array): modality array of shape (n_subjs, n_feats)
        axis (int or None): axis to normalize array

    Returns:
        np.array: normalized array
    """

    norm_arr = zscore(modality_arr, axis=axis)
    norm_arr[np.isnan(norm_arr)] = 0

    return norm_arr

def concatenate_modalities(fa, lfp):
    """Concatenate FA values and LFP values.

    Args:
        fa (np.array): fa values (n_subjs, n_voxels)
        lfp (np.array): lfp values (n_subjs, n_timepoints*n_regions)

    Returns:
        np.array: input array for jICA (n_subjs, n_features)
    """

    return np.hstack((fa, lfp))