<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

To cite this repository, please see: 
[![DOI](https://zenodo.org/badge/223283087.svg)](https://zenodo.org/badge/latestdoi/223283087)

PsychoPy code to display visual instructions for a _Breath Hold_ and a _Cued Deep Breathing_ task, alongside MRI scanning.
==============

How to run:
--------------
Download [PsychoPy](https://www.psychopy.org/). The code in this repo is written in PsychoPy3.0.5 - compatibility with other versions has not been tested.
Open PsychoPy on your computer. To run from 'Coder' view, simply do File-Open, select your breathing task file and then press the green running man symbol to start.

Input arguments that can be changed:
--------------
(See each code for default arguments used)

Breath_Hold.py

- _scan_trigger:_ value the MRI pulse trigger is read in as
- _doRest:_ 0 = no rest; 1 = rest before BH task; 2 = rest after BH trials; 3= rest before AND after BH trials (rest refers to showing a fixation cross)
- _tResting_start_ = duration of resting fixation at the start in seconds, if doRest=1 or doRest=3
- _tResting_end_ = duration of resting fixation at the end in seconds, if doRest=2 or doRest=3
- _trialnum_ = number of BH trial repeats (one trail is paced breathing + hold + exhale + recover)
- _tPace_ = duration of paced breathing in seconds
- _tBreathPace_ = duration of each breath in/out in seconds e.g. 6.0 s would be 3s IN and 3s OUT (tPace / tBreathPace pace needs to be integer )
- _tHold_ = duration of the hold period in seconds
- _tExhale_ = duration for expelling air after the hold in seconds
- _tRecover_ = duration of recovery breaths in seconds
- _BH_instructions_ = 'instructions to display to participant at start of experiment'
- _end_exp_key_ = key to press to end the experiment prematurely

Cued_Deep_Breathing.py

- _scan_trigger:_ value the MRI pulse trigger is read in as
- _doRest:_ 0 = no rest; 1 = rest before CDB trials; 2 = rest after CDB trials; 3= rest before AND after CDB trials (rest refers to showing a fixation cross)
- _tResting_start_ = duration of resting fixation at the start in seconds, if doRest=1 or doRest=3
- _tResting_end_ = duration of resting fixation at the end in seconds, if doRest=2 or doRest=3
- _trialnum_ = number of CDB trial repeats (Get Ready, IN-OUT, Breathe Normally)
- _tGetReady_ = duration of get ready warning before CDB section
- _tCDB_ = duration of CDB section
- _tCDBPace_ = duration of each breath in/out in seconds e.g. 6.0 s would be 3s IN and 3s OUT (tCDB / tCDBPace needs to be integer )
- _tFree_ = duration of free breathing in between each CDB section
- _CDB_instructions_ = 'instructions to display to participant at start of experiment'
- _end_exp_key_ = key to press to end the experiment prematurely

Fixation.py

- _RestDuration_ = duration of the resting block in seconds (fixation cross is shown in center of screen)
- _end_exp_key_ = key to press to end the experiment prematurely


Tips for using this code:
--------------

- It is designed to be used alongside recordings of end-tidal CO2 and O2 via a nasal cannula, during MRI, but can be used with other set-ups.
- If you are sampling exhaled CO2 and O2, it is good practice to measure the partial pressure of these recordings before the scanning session (to appropriately calibrate your gas analyzer within your recording environment, in order to convert signal recordings from Volts to mmHg).
- Press '5' when it says 'waiting for scanner ...' to manually start the breathing task instructions. Or set this input to be whatever the MRI sends to indicate the first volume of data is being acquired so that your breathing task will be synchronized to the start of your scan. 
- Always practice with the participant before the main experimental session to make sure they understand the task instructions and can achieve the desired end-tidal changes. If possible, practice while monitoring the physiological signals closely. Pay particular attention to the **exhalations preceding and following** the hold: if they are not performed well, you won't be able to use the recorded data in the most appropriate way. See the pictures below, which show an example of good task compliance. 
- Tell them to breathe through their nose (if you are sampling end-tidal CO2 with a nasal cannula). 
- The fixation cross at the start and end of the BH and CDB tasks can help establish a steady-state response before the start of the breathing task and compensate for any signal delays between end-tidal recordings and other recordings e.g. blood flow with fMRI. It is always good to record the end-tidals for about a minute before and after your actual task, to allow for correcting these types of things.
- If carrying out these tasks during MRI scanning, remind the particpant on a few occasions to try to keep their head as still as possible. Unfortunately, task-correlated motion is common.

**For BH**: There is a period of paced breathing to try to get the participant to breathe consistently. Also, this paced breathing finishes with an exhale. This is important because this allows an end-tidal estimate just before the hold period. During the hold period, the participant should not breathe in or out. Right at the end of the hold period it says 'Exhale' - this is important because it allows an end-tidal estimate just after the hold period. Instruct your participant by saying something like "You will want to breathe in just after the hold but we need you to do one more exhale - breathe out all the air you have left!". If a participant cannot manage the full length of the hold, that is okay - just tell them to always end the hold with this exhale, even if the hold is shorter. The 'Recover' period of time is for the participant to take a few recovery breaths, how they like, before the paced breathing starts up again. If your participants are struggling to do this task, even after further practice, consider decreasing the hold time and increasing the recovery time. 

The CO2 and O2 recordings, measured here in mmHg, should look something like this (showing 3 trials, note the increased CO2 end-tidal after the hold):

![image1](https://github.com/RayStick/BreathingTasks_PsychoPy/blob/main/BH_BreathingTrace.png)

**For CBD**: There is a 'Get Ready' to warn the participant that the breathing instructions are about to appear. Then 'IN' and 'OUT' will cue the deep breaths - participants should be told that these breaths need to be deeper than their normal breaths. 

The CO2 and O2 recordings, measured here in mmHg, should look something like this (showing 2 trials, note the decreased CO2 end-tidals after the deep breaths):

![image2](https://github.com/RayStick/BreathingTasks_PsychoPy/blob/main/CDB_BreathingTrace.png)

Use a peak detection algorithm to create the end-tidal trace from breathing traces like this. A linear interpolation is often used between each sampled end-tidal value. Some peak detection algorithms on GitHub: [peakdet](https://github.com/physiopy/peakdet) and [NeuroKit](https://github.com/neuropsychology/NeuroKit)


## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/kristinazvolanek"><img src="https://avatars.githubusercontent.com/u/54590158?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Kristina Zvolanek</b></sub></a><br /><a href="https://github.com/RayStick/BreathingTasks_PsychoPy/pulls?q=is%3Apr+reviewed-by%3Akristinazvolanek" title="Reviewed Pull Requests">👀</a> <a href="#ideas-kristinazvolanek" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/smoia"><img src="https://avatars.githubusercontent.com/u/35300580?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Stefano Moia</b></sub></a><br /><a href="https://github.com/RayStick/BreathingTasks_PsychoPy/pulls?q=is%3Apr+reviewed-by%3Asmoia" title="Reviewed Pull Requests">👀</a> <a href="#ideas-smoia" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="http://linkedin.com/in/rstickland-phd"><img src="https://avatars.githubusercontent.com/u/50215726?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Rachael Stickland</b></sub></a><br /><a href="https://github.com/RayStick/BreathingTasks_PsychoPy/commits?author=RayStick" title="Code">💻</a> <a href="#ideas-RayStick" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/RayStick/BreathingTasks_PsychoPy/commits?author=RayStick" title="Documentation">📖</a></td>
    <td align="center"><a href="http://brightlab.northwestern.edu"><img src="https://avatars.githubusercontent.com/u/32640425?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Molly Bright</b></sub></a><br /><a href="#ideas-BrightMG" title="Ideas, Planning, & Feedback">🤔</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
