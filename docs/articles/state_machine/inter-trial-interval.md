# Inter-Trial Interval
The Inter-Trial Interval (ITI) state is, as the name suggests, the time interval that separates two consecutive trials.

Since there is a need to setup each trial (for example, to (re)set some parameters) and the duration of the ITI is, typically, a few seconds, this state is also used to prepare the new trial. Currently, the actions that take place in the ITI state are:

- Checking if a block of trials ended in the previous trial and, if so, reset the block variables and update the block
number and training level;
- Updating the trial number;
- Randomizing the ABL (average binaural level) and ILD (inter-aural level) values and selecting the sound that is
going to be played in the current trial.

## State description

## What happens in this state

## Subjects used and/or updated
