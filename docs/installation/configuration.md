# Task Configuration

After setting up both the hardware and the software needed for the task, there's just one more step to follow before start running the task: configuring it.

Despite the task having a [common structure](../articles/state_machine/introduction.md), there are small variations to the task that can be achieved by tweaking inumerous configurations. Additionally, there's a need to input the calibration parameters for different pieces of hardware (speakers, SyringePumps, etc), which vary from setup to setup. Because of this, 4 different configuration files were created:
- `startup.json` - This file is the only hardcoded file both in the Bonsai workflow and in the Python application. It is located in the `./src/config` directory (where `.` is the root folder of the project) and its name can't be changed. This file contains the paths to the remaining input files and the path to the "main" output directory (read the section on the [output directory](#output-directory)). A description of each parameter can be found [here](../api/Parameters.StartupFile.yml).
- `animal.json` - This file contains task configurations that are not level-dependent and/or don't change throughout a session. Some of the parameters present in this file are filled/changed according to the answers given to the initial prompts of the task. A description of each animal-specific setting can be found [here](../api/Parameters.AnimalConfig.yml).
- `training.csv` - Generally, the configurations that can be set in this file are task parameters that can change a lot during the training phase of an animal. Each line of the file is a different training level the animal has to progress to/through. It can be assumed that when the animal reaches the last level, it's ready for the "actual" experiment. A description of each training-specific setting can be found [here](../api/Parameters.TrainingConfig.yml).
- `setup.csv` - The settings that can be found in this file don't usually change the logic of the state machine, but are necessary for the setup to be working correctly (for example: equipment calibration parameters). Each line of this file is a different setup, so it's possible to have a single file stored in a drive containing the configurations for every setup and "point" to that file through the `startup.json` file. A description of each setup-specific setting can be found [here](../api/Parameters.SetupConfig.yml).

## Output Directory

It is intended that all data from every animals is saved in a single directory (the "main" output directory). Look at the following example of a "main" output directory.

```
main/
├── Rat001/
│   ├── 241001/
│   │   ├── out.csv
│   │   ├── events0.bin
│   │   ├── 0.png
│   │   └── 1.png
│   └── 241002/
│       ├── out.csv
│       ├── events0.bin
│       └── 0.png
└── Rat002/
    ├── 241003/
    │   ├── out.csv
    │   ├── events0.bin
    │   ├── 0.png
    │   └── 1.png
    └── 241004/
        ├── out.csv
        ├── events0.bin
        ├── events1.bin
        └── 0.png
```

Inside the "main" directory there is a folder for every animal. Inside each animal's folder there is a folder for every session day, whose name is in the `YYMMDD` format, and inside every session day folder there are 3 file types:
- `out.csv` - this is the main output file and has the output data from every trial from every session an animal did so far.
- `eventsX.bin` - this file has every event from every Harp board connected during a session. Here, the `X` represents the session number of the day (in theory, an animal participates in only one session a day, but in case the session is stopped ahead of time - for example, because of a crash - it's good that the events from the new session don't overwrite the existing ones).
- `X.png` - this file is a print of the Python application window captured at the end of each block. Here, the `X` represents the block number of the day.

**WARNING:** it is recommended that the "main" output directory only contains files saved by the task's software. If there's a need to manually save other files related to the experiment, please do it somewhere else.

# Others (COM ports and some file paths)

Although there was a good effort to put the maximum amount of configuration parameters outside of Bonsai, there are still some things that have to be configured in it, namely:
- the COM ports for the Harp boards.
- the paths for the video-related files.

To configure these, follow the steps:
1. Open bonsai from `./bonsai/Bonsai.exe` and open the project's file.
2. Double-click on the `Hardware` node. Inside this node, there are 7 different nodes: the first 5 are Harp-related, the sixth is the camera-related and the last one is used to save every Harp message.
3. Double-click on the Harp-related nodes for the boards being used. Find the respective device node (for example, `Behavior` or `SoundCard`), click on it and change the `PortName` property accordingly on the right panel in Bonsai. To find out which COM port corresponds to the board, install one of the Harp LabVIEW-based GUIs and look for a `List devices` button (or a button with a similar name).
4. For the video-related files, double-click on the `Camera` Group Workflow node. Then click on the Sink nodes (the purple ones) and change the `FileName` property so that those files are created and saved in the desired paths.
