import mne
import numpy as np
import pandas as pd
from mne.preprocessing import ICA, create_eog_epochs, create_ecg_epochs
# import picard

data = pd.read_csv("data/no_wink.csv", skiprows=0, usecols=[*range(3, 8)])
# print(data)
ch_names = ["EOG.AF3", "EEG.T7", "EEG.Pz", "EEG.T8", "EOG.AF4"]
num_channels = len(ch_names)
sfreq = 2048
ch_types = ["eeg" for i in range(num_channels)]
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
raw = mne.io.RawArray(data.transpose(), info)
picks_all = [*range(num_channels)]

channels = mne.pick_types(raw.info, eeg=True, eog=True)
raw.plot(block=True, n_channels=num_channels, scalings=150)
# raw.plot_psd(fmax=1024, picks=picks_all)

# high pass filter
filt_raw = raw.copy()
filt_raw = filt_raw.load_data().filter(picks=picks_all, l_freq=100, h_freq=None)
# filt_raw.plot(block=True, n_channels=num_channels, scalings=150)

events = mne.find_events(raw, stim_channel='EOG.AF4', shortest_event=1)
print(events[:5])  # show the first 5

# can't get method="picard" to work??
ica = mne.preprocessing.ICA(n_components=5, random_state=97, max_iter='auto')
ica.fit(filt_raw, picks=picks_all)

# doesn't work
# eog_indices, eog_scores = ica.find_bads_eog(filt_raw)
