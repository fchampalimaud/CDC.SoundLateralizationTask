# Introduction

The sound lateralization task implemented in the current project, which is based on [1], was designed as a state machine, where the progression through the different states is driven by certain events. The figure below is a representation of the state machine that describes this task.

![State Machine](../../images/state_machine.svg)

From the figure, notice that from most states there are two possible states that these states can progress to. This happens because there are certain conditions that have to be met in order for the state machine to progress to the next "desired" state.

 The remaining pages of this subsection are dedicated to the description each individual state (which include an explanation of what happens and what are the progression conditions).

<!-- ## References
[1]  -->