import mne
import pandas as pd
# import picard as picard
from mne.preprocessing import ICA
from mne.time_frequency import stft
from scipy.fft import fft, ifft

# load data
data = pd.read_csv("data/right_wink.csv", skiprows=0, usecols=[*range(3, 8)])
# print(data)
ch_names = ["AF3", "T7", "Pz", "T8", "AF4"]
num_channels = len(ch_names)
sfreq = 2048
ch_types = ["eeg" for i in range(num_channels)]

# turn into mne raw object
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
raw = mne.io.RawArray(data.transpose(), info)
print(info)
# raw.save('data/example_right.fif')
picks_all = [*range(num_channels)]

# plot signals
channels = mne.pick_types(raw.info, eeg=True, eog=True)
raw.plot(block=True, n_channels=num_channels, scalings=150)
# raw.plot_psd(fmax=1024, picks=picks_all)

# fit ica component
ica = ICA(n_components=5, random_state=97, max_iter='auto')
ica.fit(raw, picks=picks_all)
raw.load_data()
ica.plot_sources(raw, block=True, picks=picks_all, show_scrollbars=False)

# high pass filter
filt_raw = raw.copy().load_data().filter(picks=picks_all, l_freq=25, h_freq=None)
filt_raw.plot(block=True, n_channels=num_channels, scalings=150)

# fit ica component
# ica = ICA(n_components=5, method='picard', random_state=97, max_iter='auto')
ica = ICA(n_components=5, random_state=97, max_iter='auto')
ica.fit(filt_raw, picks=picks_all)
filt_raw.load_data()
ica.plot_sources(filt_raw, block=True, picks=picks_all, show_scrollbars=False)

# visualize 10-20 eeg labeling system
montage = mne.channels.make_standard_montage(kind='standard_1020')
raw_1020 = raw.copy().set_montage(montage)
fig = montage.plot(kind='3d')
fig.gca().view_init(azim=70, elev=15)  # set view angle
montage.plot(kind='topomap')
print(montage)  # 94 channels
print(raw_1020.get_montage())  # 5 channels
ica.plot_sources(filt_raw, block=True, picks=picks_all, show_scrollbars=False)
# ica.plot_properties(raw_1020, picks=[1])
# ica.plot_components(raw, picks=1)
