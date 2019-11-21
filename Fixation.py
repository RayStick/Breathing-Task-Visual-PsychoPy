#!/usr/bin/env python
# -*- coding: utf-8 -*-

###  Fixation ###
# Simply shows a fixation cross for a set amount of time

#import necessary libraries & functions
from psychopy import locale_setup, gui, visual, core, data, event, logging, sound

########## CHANGE ##########
RestDuration = 600 #duration of the resting block in seconds
end_exp_key = 'escape' #key to press to end the experiment prematurely

########## START ##########
globalClock = core.Clock()  # to track the time since experiment started

## Set-up the Window ##
win = visual.Window(
    size=(1440, 900), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)

## Display Fixation ##
rest = visual.TextStim(win=win, name='rest',
    text=u'+',
    font=u'Arial',
    pos=(0, 0), height=0.5, wrapWidth=None, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    alignHoriz='center', depth=0.0);

rest.draw()
win.flip()
event.waitKeys(maxWait=RestDuration, keyList=['escape'], timeStamped=False)

# make sure everything is closed down
win.close()
core.quit()
