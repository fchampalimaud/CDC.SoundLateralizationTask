# User Guide

In this page, it is assumed that the Bonsai environment, the USB drivers and each Harp board's firmware are already installed. If any of these requirements isn't met, please read the [Install](../installation/bonsai.md) section.

## Configuring the task
In spite of existing a common task structure, there are small variations of this sound lateralization task that can be achieved by tweaking inumerous configurations. These configurations are divided in 3 different files that can be found inside the `./src/config` directory:
- `training.csv` - Generally, the configurations that can be set in this file are task parameters that can change a lot during the training phase of an animal. Each line of the file is a different training level the animal has to progress to/through. It can be assumed that when the animal reaches the last level, it's ready for the "actual" experiment. A description of each training-specific setting can be found [here](../api/SLTUtils.TrainingConfiguration.yml).
- `animal.json` - This file contains task configurations that are not level-dependent and/or don't change throughout a session. A description of each animal-specific setting can be found [here](../api/SLTUtils.AnimalSpecificConfiguration.yml).
- `setup.json` - The settings that can be found in this file don't usually change the logic of the state machine, but are necessary for the setup to be correctly working (for example: equipment calibration parameters). A description of each animal-specific setting can be found [here](../api/SLTUtils.SetupConfiguration.yml).

## Running the task

1. In the task's directory, open `./bonsai/Bonsai.exe`.
2. Click in `Open File` and select `./src/sound_lateralization_task.bonsai`, which is the file containing the workflow of the task.
3. After opening the workflow, click on the `Start` button which is located in the left side of the top tab of the application. Alternatively, press `F5` on your keyboard.
4. Double-click on the `TaskInfo` SubscribeSubject node - it's a green node - to open a window which will be giving feedback about what's happening in the task (_optional_).

The data collected during a session can be found in the `./src/output` directory.