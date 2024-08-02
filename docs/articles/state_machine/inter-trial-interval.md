# Inter-Trial Interval
The Inter-Trial Interval (ITI) state is, as the name suggests, the time interval that separates two consecutive trials.

Since there is a need to setup each trial (for example, to (re)set some parameters) and the duration of the ITI is, typically, a few seconds, this state is also a preparation of the new trial. Currently, the actions that take place in the ITI state are:
- Updating the trial number.
- Checking if a block of trials ended in the previous trial and, if so, reset the block variables and update the block number and training level.
- Randomizing the ABL (average binaural level) and ILD (inter-aural level difference) values and selecting the sound that is going to be played in the current trial (**Note:** this only happens if the Level0 setting is 0).

## Progression conditions
If the ITIReset setting is 1, this state resets everytime the animal is poking the CNP before the ITI is over.