#!/bin/bash

subjid=$1

# setup directories and paths
odir=/gpfs/gsfs12/users/NIMH_scratch/MEG_Hackathon/DTI_MEG/dti
bids_dir=/gpfs/gsfs12/users/NIMH_scratch/MEG_Hackathon/hv_bids
anat_dir=${bids_dir}/${subjid}/ses-01/anat
dwi_dir=${bids_dir}/${subjid}/ses-01/dwi

T1file=${subjid}_ses-01_*run-01_T1w.nii.gz
FAfile=dti_FA.nii.gz

cd ${anat_dir} || exit

# align T1 to TT_N27
@auto_tlrc \
    -base TT_N27+tlrc               \
    -input $T1file                  \
    -prefix t1+tlrc.nii \
    -no_avoid_eyes

# remove temporary files
rm *+orig*
rm *.1D
rm *WarpDrive.log

# align FA map to t1+tlrc

cd ${dwi_dir} || exit

@auto_tlrc \
    -apar ../anat/t1+tlrc.nii   \
    -input $FAfile                \
    -prefix ${subjid}_FA_tlrc.nii

cp ${subjid}_FA_tlrc.nii ${odir}/${subjid}_FA_tlrc.nii
