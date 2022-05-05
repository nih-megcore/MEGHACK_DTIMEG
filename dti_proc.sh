#!/bin/bash

subjid=sub-ON02747 #$1

#Setup Input and Output Directories
output_dir=/gpfs/gsfs12/users/NIMH_scratch/MEG_Hackathon/DTI_MEG
bids_dir=/gpfs/gsfs12/users/NIMH_scratch/MEG_Hackathon/hv_bids

#Define MRI Paths
T1path=${bids_dir}/${subjid}/ses-01/anat/${subjid}_ses-01_*run-01_T1w.nii.gz
T2path=${bids_dir}/${subjid}/ses-01/anat/${subjid}_ses-01_*run-01_T2w.nii.gz

DWI_r1=${bids_dir}/${subjid}/ses-01/dwi/${subjid}_ses-01_run-01_dwi.nii.gz
DWI_r2=${bids_dir}/${subjid}/ses-01/dwi/${subjid}_ses-01_run-02_dwi.nii.gz

#Copy T1 and T2 into reg folder
regpath=/tmp/regT1T2
mkdir ${regpath}
3dcopy ${T1path} ${regpath}
3dcopy ${T2path} ${regpath}

