# Abort
The Abort state is triggered when some conditions are not met in the previous states. This state consists of a small time penalty. The penalty time is defined by AbortPenalty, unless a fixation abort occurred. If that's the case, then the penalty time is defined by FixationAbortPenalty.

Since this state is one of the two possible final states of a trial, there is a need to set/update some variables that would normally be set/updated in states that the state machine did not get into during the current trial.