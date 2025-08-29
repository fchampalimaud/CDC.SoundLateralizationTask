# Running the Task

After having everything else setup, the only thing left is to run the task. To do it, follow the steps:
1. In the task's directory, double-click on the `./Run.cmd` script.
2. Answer the initial prompts. Then, the bonsai workflow will open and the task will start with the GUI that allows the user to monitor the task in real-time and interact with some aspects of it.

## Initial prompts

The goal of the initial prompts is to ease up launching the task without the need for the user to change the configuration files manually every session, specially for parameters that depend on the data saved in the previous session (like the trial number) and for repetitive operations (like choosing the animal the will perform the task). Below, you can find the prompts with a brief description of what it does and what answers are valid.

1. Hello! :) Let me know who you are, please: 
    
    This prompt only accepts letters and spaces and the first character **must** be a capital letter. Examples of valid answers are: `John Doe` or `JD`.

2. Are you training an animal from which batch?

    This prompt accepts alphanumeric answers (with underscores, but the underscore can't be the first or last character). An example of a valid answer is: `batch_name`. 

3. Which furry friend is going to be joining us?

    This prompt accepts an animal ID, which is composed by 2 to 6 capital letters followed by 4 digits: Examples of valid answers are: `ANIMAL0000` or `RAT0055`.

4. Get parameters from last session (fixation time, reaction time, lnp_time and training_level)? [y/n]

    This prompt only accepts `y` and `n` as valid answers and only appears in case the animal input in 3. already started training previously. If the answer is affirmative, the values from fixation time, reaction time, LNP time and training level are read from the last trial done by the animal and written in the animal's `animal.yml` file.

5. What is the training level the animal should stop progressing? (You can leave blank if the animal can progress until the last level)

    This prompt only accepts a number up to 2 digits.

In addition to the prompts mentioned above, the startup script also looks at the data saved from the last session and updates the session number and the block number automatically.
