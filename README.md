# MEGHACK_DTIMEG

DTI processing perfomed using the DTI-scripts fork and modification for bids.  DTI processing done with FSL.

FA maps warped to TT_N27+tlrc.BRIK using AFNI
```dti_to_standard_space```

MEG data from hv_bids folder processed using mne-bids-pipeline.
Average data loaded in MNE python and signals were averaged across regional channel locations to create local regional power.  This part is implemented in the ```helpers.py``` function but is called in the run_ica.py script.

Calculated ICA on FA/MEG vectors ```run_ica.py```
