# Start Trial
A trial starts when the rodent pokes his nose in the central nose port (CNP). So this state consists of waiting that the rodent starts poking the CNP.

## Progression conditions
If there is a poke within a certain time limit (determined by the MaxWait parameter), the task continues as it is supposed to, otherwise this trial is aborted.