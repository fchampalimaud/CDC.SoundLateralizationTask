# Reward
The Reward state evaluates whether the rodent got the answer right or not. In case the answer is wrong, a penalty time is applied (10 seconds for instance). If the answer is right, the animal only gets the reward (water) if he stayed in the correct LNP for at least a minimum amount of time (IntendedLNP). This is the final state of a successful trial.

Additionally, the following variables/metrics are updated:
- AbortEvent
- RepeatTrial
- BlockAbortRatio
- BlockPerformance
- BaseFT
- BaseRT
- IntendedLNP