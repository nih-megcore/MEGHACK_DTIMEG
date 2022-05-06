
import mne
def read_chnames(fpath):
    ave=mne.read_evokeds(fpath)
    ave=ave[0]
    ave.pick_types(meg=True, ref_meg=False)
    ch_regions=set([i[1:3] for i in ave.info["ch_names"]])
    return ch_regions

#def group_channels():

#subjid='sub-ON97504'
fpath='sub-ON97504_ses-01_task-haririhammer_ave.fif'
ch_regions=read_chnames(fpath)
print(ch_regions)