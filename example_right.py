import mne
import pandas as pd
import picard as picard
from mne.preprocessing import ICA

# load data
data = pd.read_csv("data/right_wink.csv", skiprows=0, usecols=[*range(3, 8)])
# print(data)
ch_names = ["EEG.AF3", "EEG.T7", "EEG.Pz", "EEG.T8", "EEG.AF4"]
num_channels = len(ch_names)
sfreq = 2048
ch_types = ["eeg" for i in range(num_channels)]

# turn into mne raw object
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
raw = mne.io.RawArray(data.transpose(), info)
# raw.save('data/example_right.fif')
picks_all = [*range(num_channels)]

# plot signals
channels = mne.pick_types(raw.info, eeg=True, eog=True)
raw.plot(block=True, n_channels=num_channels, scalings=150)
# raw.plot_psd(fmax=1024, picks=picks_all)

# fit ica component
ica = ICA(n_components=5, method='picard', random_state=97, max_iter='auto')
ica.fit(raw, picks=picks_all)
raw.load_data()
ica.plot_sources(raw, block=True, picks=picks_all, show_scrollbars=False)

# high pass filter
filt_raw = raw.copy()
filt_raw = filt_raw.load_data().filter(picks=picks_all, l_freq=100, h_freq=None)
filt_raw.plot(block=True, n_channels=num_channels, scalings=150)
