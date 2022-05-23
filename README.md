# Mind-Controlled EEG Car

## Abstract
We created a mind-controlled EEG car and user interface. Using this technology, a user can perform facial expressions (like raising one’s eyebrows or frowning) and mental commands (thinking about pushing, pulling, dropping, etc.) to maneuver a remote-controlled car. With intense focus, the user can frown and think “push” to move the car forward, raise their eyebrows and think “pull” to stop the car, and clench their teeth and think “drop” to move the car backward. The user can also visualize the signal strengths of each of their mental commands and facial expressions on our dashboard, allowing them to directly view the values associated with each command that they might be wishing to view. We used the method of writing to data files and continuously polling them to fully connect this system, from EEG headset to dashboard and remote-controlled car. Additionally, we used a thresholding algorithm, accounting for the effects of signal variability, to translate the user’s brain signals into directional movement.

## Video Presentation
[Watch our tjSTAR video presentation here.](https://youtu.be/Bl1QghYms_U)

## Tools Used
- Python: [python-osc](https://pypi.org/project/python-osc/), [pandas](https://pandas.pydata.org/docs/), [serial](https://pyserial.readthedocs.io/en/latest/), [dash](https://dash.plotly.com/)
- Arduino: [Instructables Tutorial](https://www.instructables.com/Control-an-RC-Car-Using-the-Computer/)
- Emotiv: [OSC script](https://github.com/Emotiv/opensoundcontrol/tree/master/examples/python), [Headset Tutorial](https://www.youtube.com/watch?v=Z81Lb3EIEz4&ab_channel=emotivstation), [EPOC X User Manual](https://emotiv.gitbook.io/epoc-x-user-manual/), [EmotivBCI User Manual](https://emotiv.gitbook.io/emotivbci/)

