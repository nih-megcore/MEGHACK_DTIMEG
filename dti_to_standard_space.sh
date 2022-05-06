#!/bin/bash

subjid="ON95742"

# setup directories and paths
bids_dir=/gpfs/gsfs12/users/NIMH_scratch/MEG_Hackathon/hv_bids
anat_dir=${bids_dir}/${subjid}/ses-01/anat
dwi_dir=${bids_dir}/${subjid}/ses-01/dwi

T1path=${anat_dir}/${subjid}_ses-01_*run-01_T1w.nii.gz
FApath=${dwi_dir}/dti_FA.nii.gz

# align T1 to TT_N27
@auto_tlrc \
    -base TT_N27+tlrc               \
    -input $T1path                  \
    -prefix ${anat_dir}/t1+tlrc.nii \
    -no_avoid_eyes

# align FA map to t1+tlrc

@auto_tlrc \
    -apar ${anat_dir}/t1+tlrc.nii   \
    -input ${FApath}                \
    -prefix ${dwi_dir}/FA+tlrc.nii