BreathingTasks_PsychoPy
==============
PsychoPy code to display visual instructions for a 'Breath Hold' and a 'Cued Deep Breathing' task. 

Written with PsychoPy3.0.5

Tips for using this code:
--------------

- It is designed to be used alongside recordings of end-tidal CO2 and O2 via a nasal cannula, during MRI, but can be used with other set-ups. 
- Press '5' when it says 'waiting for scanner ...' to manually start the breathing task instructions. Or set this input to be whatever the MRI sends to indicate the first volume of data is being acquired so that your breathing task will be synchronized to the start of your scan. 
- Always practice with the participant beforehand to make sure they understand the task instructions and can achieve the desired end-tidal changes. 
- Tell them to breathe through their nose (if you are sampling end-tidal CO2 with a nasal cannula). 
- The fixation cross at the start and end of the BH and CDB tasks can help establish a steady-state response before the start of the breathig task and compensate for any signal delays between end-tidal recordings and other recordings e.g. blood flow with fMRI. It is always good to record the end-tidals for about a minute before and after your actual task, to allow for correcting these types of things. 

**For BH**: There is a period of paced breathing to try to get the participant to breathe consistently. Also, this paced breathing finishes with an exhale. This is important because this allows an end-tidal estimate just before the hold period. During the hold period, the participant should not breathe in or out. Right at the end of the hold period it says 'Exhale' - this is important because it allows an end-tidal estimate just after the hold period. Instruct your participant by saying something like "You will want to breathe in just after the hold but we need you to do one more exhale - breathe out all the air you have left!". If a participant cannot manage the full length of the hold, that is okay - just tell them to always end the hold with this exhale, even if the hold is shorter. The 'Recover' period of time is for the participant to take a few recovery breaths, how they like, before the paced breathing starts up again. If your participants are struggling to do this task, even after further practice, consider decreasing the hold time and increasing the recovery time. 

The CO2 and O2 recordings, measured here in mmHg, should look something like this (showing 3 trials, note the increased CO2 end-tidal after the hold):

![image1](https://github.com/RayStick/BreathingTasks_PsychoPy/blob/main/BH_BreathingTrace.png)

**For CBD**: There is a 'Get Ready' to warn the participant that the breathing instructions are about to appear. Then 'IN' and 'OUT' will cue the deep breaths - participants should be told that these breaths need to be deeper than their normal breaths. 

The CO2 and O2 recordings, measured here in mmHg, should look something like this (showing 2 trials, note the decreased CO2 end-tidals after the deep breaths):

![image2](https://github.com/RayStick/BreathingTasks_PsychoPy/blob/main/CDB_BreathingTrace.png)


Use a peak detection algorithm to create the end-tidal trace from breathing traces like this. A linear interpolation is often using between each sampled end-tidal value. 

