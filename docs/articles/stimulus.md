# Stimulus
This is the state where the stimulus is presented. The stimulus stops when either the rodent leaves the CNP (if UseRT is 1) or when the animal enters one of the LNP's (if UseRT is 0) or when the defined presentation time elapses (the presentation time is defined by MaxRT).

## Progression conditions
If the animal leaves the CNP after the minimum reaction time (defined by MinRT) and before the maximum reaction time (defined by MaxRT), the task proceeds as expected. Otherwise, it is aborted.