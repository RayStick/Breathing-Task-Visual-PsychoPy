#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cued Deep Breathing (CDB)

Instructions are displayed to the participant in this order: Get Ready, Deep Breaths, Breathe Normally
The script can be started by an MRI pulse trigger.

"""

# import necessary libraries & functions
from __future__ import absolute_import, division
from psychopy import gui, visual, core, data, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, FINISHED)
import os
from psychopy.hardware.emulator import launchScan  # this is to read in TTL pulse from MRI scanner as a trigger

######################
#  CHANGE PARAMETERS #
######################

scan_trigger = 5  # value the MRI pulse trigger is read in as
doRest = 2  # 0 = no rest; 1 = rest before CDB task; 2 = rest after CDB task; 3= rest before AND after CDB task
tResting = 30  # duration of resting fixation in seconds

# Task components : Rest, Get Ready, IN-OUT, Breathe Normally
trialnum = 2  # number of CDB repeats
tStartRest = 28  # duration of rest before first CDB section
tGetReady = 2  # duration of get ready warning before CDB section
tCDB = 8  # duration of CDB
tCDBPace = 4  # duration of each breath in/out in seconds e.g. 6.0 s would be 3s IN and 3s OUT (tCDB / tCDBPace needs to be integer )
tFree = 43  # duration of free breathing in between each CDB section
CDB_instructions = 'DEEP BREATHING task \n \nTake deep breaths IN and OUT when cued \n \nBreathe through your nose'
end_exp_key = 'escape'  # key to press to end the experiment as it is running

#######
# RUN #
#######

# Define Timings
tLength = tGetReady + tCDB + tFree  # total length of one trial
rCDBPace = tCDB/tCDBPace  # number of repeats (breath in and out) in the CDB part- has to be an integer else script will terminate:

if rCDBPace != int(rCDBPace):
    print('** WARNING:' + str(rCDBPace) + ' is not an integer, please change tCDBPace')
    core.quit()

rCDBPace = int(rCDBPace)

# Define Paths & Data Saving

_thisDir = os.path.dirname(os.path.abspath(__file__))  # Get the full path this python script is saved to
os.chdir(_thisDir)  # Change the current wd to the path above - to ensure relative paths start from the same directory

expName = os.path.basename(__file__)  # name of this file
expInfo = {'Participant': '', 'Session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK is False:
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
expInfo['tFree'] = tFree
expInfo['tCDB'] = tCDB
expInfo['tCDBPace'] = tCDBPace

# save a log file for detailed info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# Set-up the Window

win = visual.Window(size=(1440, 900), fullscr=True, screen=0,
                    allowGUI=False, allowStencil=False,
                    monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb',
                    blendMode='avg', useFBO=True)

win.recordFrameIntervals = True

# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] is not None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
    print('**WARNING: could not retrieve frame rate, had to assume 60fps. Experiment timings may be wrong**')

# Define information for each routine in the experiment

# instructions
Instruct = visual.TextStim(win=win, name='Instruct',
                           text=CDB_instructions,
                           font=u'Arial',
                           pos=(0, 0), height=0.15, wrapWidth=1, ori=0,
                           color=u'white', colorSpace='rgb', opacity=1,
                           alignHoriz='center', depth=0.0)

# trial
trialClock = core.Clock()
free = visual.TextStim(win=win, name='free',
                       text=u'Breathe \nNormally',
                       font=u'Arial',
                       pos=(0, 0), height=0.3, wrapWidth=3, ori=0,
                       color=u'white', colorSpace='rgb', opacity=1,
                       alignHoriz='center', depth=0.0)
CDB = visual.TextStim(win=win, name='CDB',
                      text=u'CDB text - IN or OUT',
                      font=u'Arial',
                      pos=(0, 0), height=0.5, wrapWidth=None, ori=0,
                      color=u'white', colorSpace='rgb', opacity=1,
                      alignHoriz='center', depth=0.0)
getready = visual.TextStim(win=win, name='getready',
                           text='Get Ready',
                           font=u'Arial',
                           pos=(0, 0), height=0.3, wrapWidth=3, ori=0,
                           color=u'yellow', colorSpace='rgb', opacity=1,
                           alignHoriz='center', depth=0.0)
timedisplay = visual.TextStim(win=win, name='timedisplay',
                              text='',
                              font=u'Arial',
                              pos=(0, -0.3), height=0.2, wrapWidth=None, ori=0,
                              color=u'yellow', colorSpace='rgb', opacity=1,
                              alignHoriz='center', depth=0.0)
fixation = visual.TextStim(win=win, name='fixation',
                           text=u'+',
                           font=u'Arial',
                           pos=(0, 0), height=0.5, wrapWidth=None, ori=0,
                           color=u'white', colorSpace='rgb', opacity=1,
                           alignHoriz='center', depth=0.0)

# DISPLAY INSTRUCTIONS TO PARTICIPANT
Instruct.draw()
win.flip()
event.waitKeys(maxWait=300, keyList=['space'], timeStamped=False)  # space key to start or after a long wait

# TRIGGER THE START OF THE TASK WITH MRI
MRinfo = {'sync': scan_trigger, 'TR': 3, 'volumes': 300}  # TR and vols can be changed here if needed
globalClock = core.Clock()  # to track the time since experiment started
launchScan(win, MRinfo, mode='scan', globalClock=globalClock)

globalClock = core.Clock()  # to track the time since experiment started

# REST BLOCK TO START?
if doRest == 1 or doRest == 3:
    fixation.draw()
    win.flip()
    event.waitKeys(maxWait=tResting, keyList=[end_exp_key], timeStamped=False)

# FIRST SECTION OF REST
fixation.draw()
win.flip()
event.waitKeys(maxWait=tStartRest, keyList=[end_exp_key], timeStamped=False)

# START CDB TASK
routineTimer = core.CountdownTimer()  # to track time remaining of each routine
thisExp.nextEntry()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=trialnum, method='sequential',
                           originPath=-1,
                           trialList=[None],
                           seed=None, name='trials')
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values

if thisTrial is not None:
    for paramName in thisTrial.keys():
        exec(paramName + '= thisTrial.' + paramName)

for thisTrial in trials:
    currentLoop = trials
    if thisTrial is not None:
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
    trialComponents = [getready, CDB, free]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "trial"-------
    while continueRoutine and routineTimer.getTime() > 0:

        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *getready* updates
        if t >= 0.0 and t <= tGetReady and getready.status == NOT_STARTED:
            # keep track of start time/frame for later
            getready.tStart = t
            getready.frameNStart = frameN  # exact frame index
            getready.setAutoDraw(True)
            getreadytimer = core.CountdownTimer(tGetReady)

            while getreadytimer.getTime() > 0:

                if event.getKeys(keyList=[end_exp_key]):
                    core.quit()

                getready.draw()
                win.flip()

        frameRemains = 0.0 + tGetReady - win.monitorFramePeriod * 0.75  # most of one frame period left
        if getready.status == STARTED and t >= frameRemains:
            getready.setAutoDraw(False)

         # *CDB* updates
        if t >= tGetReady and CDB.status == NOT_STARTED:
            # keep track of start time/frame for later
            CDB.tStart = t
            CDB.frameNStart = frameN  # exact frame index
            CDB.setAutoDraw(True)
            CDBtimer = core.CountdownTimer(tCDB)

            for x in range(0, rCDBPace):
                timer = core.CountdownTimer(tCDBPace)
                half_timer = core.CountdownTimer(tCDBPace/2)

                while timer.getTime() > tCDBPace/2:
                        if event.getKeys(keyList=[end_exp_key]):
                           core.quit()

                        # do stuff
                        CDB.text ='IN'
                        CDB.draw()
                        win.flip()

                while (timer.getTime() > 0) and (timer.getTime() < tCDBPace/2):

                        if event.getKeys(keyList=[end_exp_key]):
                           core.quit()

                        # do stuff
                        CDB.text ='OUT'
                        CDB.draw()
                        win.flip()

        frameRemains = tGetReady + tCDB - win.monitorFramePeriod * 0.75  # most of one frame period left
        if CDB.status == STARTED and t >= frameRemains:
            CDB.setAutoDraw(False)


        # *free* updates
        if t >= tGetReady + tCDB and free.status == NOT_STARTED:
            # keep track of start time/frame for later
            free.tStart = t
            free.frameNStart = frameN  # exact frame index
            free.setAutoDraw(True)
            freetimer = core.CountdownTimer(tFree)

            while freetimer.getTime() > 0:

                 if event.getKeys(keyList=[end_exp_key]):
                    core.quit()

                 free.draw()
                 win.flip()

        frameRemains = 0.0 + tLength- win.monitorFramePeriod * 0.75  # most of one frame period left
        if free.status == STARTED and t >= frameRemains:
            free.setAutoDraw(False)
            getready.setAutoDraw(False)

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

# REST BLOCK TO FINISH?
if doRest == 2 or doRest == 3:
   free.setAutoDraw(False)
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
