#!/usr/bin/env python
# -*- coding: utf-8 -*-

### Breath_Hold (BH) ###
# The script can be started by an MRI pulse trigger
# Instructions are displayed to the participant: Paced Breathing, BH, Exhale, Recover
# This script loops over the instructions a set amount of times, and then ends with an extra Paced Breathing section.
# Optional: a period of rest (fixation cross) can be run before or after the BH task.

#import necessary libraries & functions
from __future__ import absolute_import, division
from psychopy import locale_setup, gui, visual, core, data, event, logging, sound
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy
import os
import sys
from psychopy.hardware.emulator import launchScan #this is to read in TTL pulse from MRI scanner as a trigger

###################################################################################################
######################################## CHANGE PARAMETERS ########################################
###################################################################################################

scan_trigger = 5 #value the MRI pulse trigger is read in as
doRest = 2 # 0 = no rest; 1 = rest before BH; 2 = rest after BH
tResting = 480 #duration of resting fixation in seconds

## BH : (Paced Breathing, BH, Exhale, Recover) ##
trialnum = 6 # number of BH trial repeats
tPace = 24# duration of paced breathing in seconds
tBreathPace = 6 # duration of each breath in/out in seconds e.g. 6.0 s would be 3s IN and 3s OUT (tPace / tBreathPace pace needs to be integer )
tHold =20 # duration of BH in seconds
tExhale = 2 # duration for expelling air after BH in seconds
tRecover = 6 # duration of recovery breaths in seconds
BH_instructions ='BREATH-HOLD task \n \nFollow the breathing instructions \n \nBreathe through your nose';
end_exp_key = 'escape' #key to press to end the experiment as it is running

###################################################################################################
############################################  RUN #################################################
###################################################################################################

## Define Timings ##
tLength = tPace + tHold + tExhale + tRecover # total length of one trial
sExhale = tPace + tHold # start of breathout within trial
sRecover = sExhale + tExhale  # start of recover within trial
rBreathPace = tPace/tBreathPace # number of repeats (breath in and out) in the breath paced phase - has to be an integer else script will terminate:

if rBreathPace != int(rBreathPace):
    print('** WARNING:' + str(rBreathPace) + ' is not an integer, please change tBreathPace')
    core.quit()

rBreathPace=int(rBreathPace)

## Define Paths & Data Saving ##

_thisDir = os.path.dirname(os.path.abspath(__file__)); # Get the full path this python script is saved to
os.chdir(_thisDir); # Change the current wd to the path above - to ensure relative paths start from the same directory

expName = os.path.basename(__file__);  #name of this file
expInfo = {'Participant':'', 'Session':'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['Participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)

expInfo['doRest'] = doRest
expInfo['tResting'] = tResting
expInfo['trialnum'] = trialnum
expInfo['tPace'] = tPace
expInfo['tBreathPace'] = tBreathPace
expInfo['tHold'] = tHold
expInfo['tExhale']= tExhale
expInfo['tRecover'] = tRecover

# save a log file for detailed info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

## Set-up the Window ##

win = visual.Window(
    size=(1440, 900), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)

win.recordFrameIntervals = True

# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
    print('**WARNING: could not retrieve frame rate, had to assume 60fps. Experiment timings may be wrong**')

## Define information for each routine in the experiment ##

#instructions
Instruct = visual.TextStim(win=win, name='Instruct',
    text=BH_instructions,
    font=u'Arial',
    pos=(0, 0), height=0.15, wrapWidth=1, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    alignHoriz='center', depth=0.0);

# trial
trialClock = core.Clock()
pace = visual.TextStim(win=win, name='pace',
    text=u'IN',
    font=u'Arial',
    pos=(0, 0.2), height=0.5, wrapWidth=None, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    alignHoriz='center', depth=0.0);
hold = visual.TextStim(win=win, name='hold',
    text =u'Hold',
    font=u'Arial',
    pos=(0, 0.2), height=0.5, wrapWidth=None, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    alignHoriz='center', depth=0.0);
exhale = visual.TextStim(win=win, name='exhale',
    text=u'Exhale!',
    font=u'Arial',
    pos=(0, 0.2), height=0.5, wrapWidth=None, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    alignHoriz='center', depth=0.0);
recover = visual.TextStim(win=win, name='recover',
    text=u'Recover',
    font=u'Arial',
    pos=(0, 0.2), height=0.5, wrapWidth=None, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    alignHoriz='center', depth=0.0);
timedisplay = visual.TextStim(win=win, name='timedisplay',
    text='',
    font=u'Arial',
    pos=(0, -0.3), height=0.2, wrapWidth=None, ori=0,
    color=u'yellow', colorSpace='rgb', opacity=1,
    alignHoriz='center', depth=0.0);
fixation = visual.TextStim(win=win, name='fixation',
    text=u'+',
    font=u'Arial',
    pos=(0, 0), height=0.5, wrapWidth=None, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    alignHoriz='center', depth=0.0);

## DISPLAY INSTRUCTIONS TO PARTICIPANT ##
Instruct.draw()
win.flip()
event.waitKeys(maxWait=300, keyList=['space'], timeStamped=False) # space key to start or after a long wait

## TRIGGER THE START OF THE TASK WITH MRI ##
MRinfo = {'sync': scan_trigger, 'TR': 3, 'volumes': 300} #TR and vols can be changed here if needed
globalClock = core.Clock()  # to track the time since experiment started
launchScan(win, MRinfo, mode='scan', globalClock=globalClock)

globalClock = core.Clock()  # to track the time since experiment started

########## REST BLOCK TO START?##########
if doRest == 1:
   fixation.draw()
   win.flip()
   event.waitKeys(maxWait=tResting, keyList=[end_exp_key], timeStamped=False)

########## START BH TASK ##########
routineTimer = core.CountdownTimer()  # to track time remaining of each routine
thisExp.nextEntry()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=trialnum, method='sequential',
    originPath=-1,
    trialList=[None],
    seed=None, name='trials')
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values

if thisTrial != None:
    for paramName in thisTrial.keys():
        exec(paramName + '= thisTrial.' + paramName)

for thisTrial in trials:
    currentLoop = trials
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)

    # ------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(tLength)
    # update component parameters for each repeat
    # keep track of which components have finished
    trialComponents = [pace, hold, exhale, recover]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "trial"-------

    while continueRoutine and routineTimer.getTime() > 0:

        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *pace* updates
        if t >= 0.0 and t<= (tPace) and pace.status == NOT_STARTED:
            # keep track of start time/frame for later
            pace.tStart = t
            pace.frameNStart = frameN  # exact frame index
            pace.setAutoDraw(True)
            pacetimer = core.CountdownTimer(tPace)
            # Add countdown
            for x in range(0, rBreathPace):
                timer = core.CountdownTimer(tBreathPace)

                while timer.getTime() > tBreathPace/2:

                    if event.getKeys(keyList=[end_exp_key]):
                       core.quit()

                    # do stuff
                    pace.text ='IN'
                    time = pacetimer.getTime()+1#add 1 so it counts down to 1 on the screen instead of 0
                    timedisplay.text = str(int(time))
                    if pacetimer.getTime() > 0:
                        pace.draw and timedisplay.draw()
                    elif pacetimer.getTime() <= 0: #don't let it show zero or minus numbers
                        pace.draw()
                    win.flip()

                while (timer.getTime() > 0) and (timer.getTime() < tBreathPace/2):

                    if event.getKeys(keyList=[end_exp_key]):
                       core.quit()

                    # do stuff
                    pace.text ='OUT'
                    time = pacetimer.getTime()+1#add 1 so it counts down to 1 on the screen instead of 0
                    timedisplay.text = str(int(time))
                    if pacetimer.getTime() > 0:
                        pace.draw and timedisplay.draw()
                    elif pacetimer.getTime() <= 0:#don't let it show zero or minus numbers
                        pace.draw()
                    win.flip()

        frameRemains = 0.0 + (tPace) - win.monitorFramePeriod * 0.75  # most of one frame period left
        if pace.status == STARTED and t >= frameRemains:
            pace.setAutoDraw(False)


        # *hold* updates
        if t >= tPace and t<= sExhale and hold.status == NOT_STARTED:
            # keep track of start time/frame for later
            hold.tStart = t
            hold.frameNStart = frameN  # exact frame index
            hold.setAutoDraw(True)
            #Add count down
            timer = core.CountdownTimer(tHold)
            while timer.getTime() > 0:

                    if event.getKeys(keyList=[end_exp_key]):
                       core.quit()

                    # do stuff
                    time = timer.getTime()+1 #add 1 so it counts down to 1 on the screen instead of 0
                    timedisplay.text = str(int(time))
                    if timer.getTime() > 0:
                        hold.draw and timedisplay.draw()
                    elif timer.getTime() <= 0: #don't let it show zero or minus numbers
                        hold.draw
                    win.flip()

        frameRemains = tPace + tHold- win.monitorFramePeriod * 0.75  # most of one frame period left
        if hold.status == STARTED and t >= frameRemains:
            hold.setAutoDraw(False)

        # *exhale* updates
        if t >= sExhale and t<= sRecover and exhale.status == NOT_STARTED:
            # keep track of start time/frame for later
            exhale.tStart = t
            exhale.frameNStart = frameN  # exact frame index
            exhale.setAutoDraw(True)
            #Add count down
            timer = core.CountdownTimer(tExhale)
            while timer.getTime() > 0:
                  if event.getKeys(keyList=[end_exp_key]):
                       core.quit()
                  exhale.draw
                  win.flip()

        frameRemains = sExhale + tExhale- win.monitorFramePeriod * 0.75  # most of one frame period left
        if exhale.status == STARTED and t >= frameRemains:
            exhale.setAutoDraw(False)

        # *recover* updates
        if t >= sRecover and t<= tLength and recover.status == NOT_STARTED:
            # keep track of start time/frame for later
            recover.tStart = t
            recover.frameNStart = frameN  # exact frame index
            recover.setAutoDraw(True)
            #Add count down
            timer = core.CountdownTimer(tRecover)
            while timer.getTime() > 0:
            #while timer.getTime() > 2:
                if event.getKeys(keyList=[end_exp_key]):
                    core.quit()
                recover.draw
                win.flip()

#            while timer.getTime() > 0 and timer.getTime() < 2: # prepare the participabt for start of paced breathing
#                recover_getready.setAutoDraw(True)
#                if event.getKeys(keyList=[end_exp_key]):
#                    core.quit()
#                recover.draw and recover_getready.draw()
#                win.flip()


        frameRemains = sRecover + tRecover- win.monitorFramePeriod * 0.75  # most of one frame period left
        if recover.status == STARTED and t >= frameRemains:
            recover.setAutoDraw(False)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

################################

#ADD EXTRA BASELINE because last trial ends on "ON" - to allow slow response to be recorded
t = 0
trialClock.reset()  # clock
frameN = -1
pace.setAutoDraw(True)
# get current time
t = trialClock.getTime()
frameN = frameN + 1  # number of completed frames (so 0 is the first frame)

# *pace* updates
if t >= 0.0 and t<= tPace:
       # keep track of start time/frame for later
       pace.tStart = t
       pace.frameNStart = frameN  # exact frame index
       pace.setAutoDraw(True)
       pacetimer = core.CountdownTimer(tPace)
       for x in range(0, rBreathPace):
             timer = core.CountdownTimer(tBreathPace)

             while timer.getTime() > tBreathPace/2:

                    if event.getKeys(keyList=[end_exp_key]):
                       core.quit()

                    # do stuff
                    pace.text ='IN'
                    time = pacetimer.getTime()+1 #add 1 so it counts down to 1 on the screen instead of 0
                    timedisplay.text = str(int(time))
                    if pacetimer.getTime() > 0:
                        pace.draw and timedisplay.draw()
                    elif pacetimer.getTime() <= 0: #don't let it show zero or minus numbers
                        pace.draw
                    win.flip()

             while (timer.getTime() > 0) and (timer.getTime() < tBreathPace/2):

                    if event.getKeys(keyList=[end_exp_key]):
                       core.quit()

                    # do stuff
                    pace.text = 'OUT'
                    time = pacetimer.getTime()+1 #add 1 so it counts down to 1 on the screen instead of 0
                    timedisplay.text = str(int(time))
                    if pacetimer.getTime() > 0:
                       pace.draw and timedisplay.draw()
                    elif pacetimer.getTime() <= 0: #don't let it show zero or minus numbers
                        pace.draw

                    win.flip()

frameRemains = 0.0 + tPace- win.monitorFramePeriod * 0.75  # most of one frame period left
if t >= frameRemains:
    pace.setAutoDraw(False)

########## REST BLOCK TO FINISH? ##########
if doRest == 2:
   pace.setAutoDraw(False)
   fixation.draw()
   win.flip()
   event.waitKeys(maxWait=tResting, keyList=[end_exp_key], timeStamped=False)

# These should auto-save but just in case:
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# Close everything
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
