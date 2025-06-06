# Task Configuration

After setting up both the hardware and the software needed for the task, there's just one more step to follow before start running the task: configuring it.

Despite the task having a [common structure](../articles/introduction.md), there are small variations to the task that can be achieved by tweaking inumerous configurations. Additionally, there's a need to input the calibration parameters for different pieces of hardware (speakers, SyringePumps, etc), which vary from setup to setup. Because of this, 3 different configuration files were created:
- `animal.yml` - This file contains task configurations that are not level-dependent and/or don't change throughout a session. Some of the parameters present in this file can be updated based on the previous session. A description of each animal-specific setting can be found [here](../api/Animal.Animal.yml).
- `training.csv` - Generally, the configurations that can be set in this file are task parameters that can change a lot during the training phase of an animal. Each line of the file is a different training level the animal has to progress to/through. It can be assumed that when the animal reaches the last level, it's ready for the "actual" experiment. A description of each training-specific setting can be found [here](../api/Training.Level.yml).
- `setup.csv` - The settings that can be found in this file don't usually change the logic of the state machine, but are necessary for the setup to be working correctly (for example: equipment calibration parameters). Each line of this file is a different setup, so it's possible to have a single file stored in a drive containing the configurations for every setup and "point" to that file from the pre-configuration script (the application mentioned in the [Software Installation](software.md) page). A description of each setup-specific setting can be found [here](../api/SetupList.Setup.yml).

## Output Directory

It is intended that all data from every animal is saved in a single directory (the output directory). Look at the following example of an output directory.

```
output/
├── Rat001/
│   ├── 241001/
│   │   ├── out_0.json
│   │   ├── out_0.csv
│   │   ├── video_0.avi
│   │   ├── cam_metadata_0.csv
│   │   ├── events/
│   │   │   ├── behavior_0_32.bin
│   │   │   ├── behavior_0_33.bin
│   │   │   ├── soundcard_0_32.bin
│   │   │   ├── soundcard_0_33.bin
│   │   │   ├── left_pump_0_32.bin
│   │   │   ├── left_pump_0_33.bin
│   │   │   ├── right_pump_0_32.bin
│   │   │   ├── right_pump_0_33.bin
│   │   │   ├── current_driver_0_32.bin
│   │   │   └── current_driver_0_33.bin
│   │   └── config/
│   │       ├── animal_0.yml
│   │       ├── setup_0.csv
│   │       └── training_0.csv
│   └── 241002/
│       ├── out_0.json
│       ├── out_1.json
│       ├── out_0.csv
│       ├── out_1.csv
│       ├── video_0.avi
│       ├── video_1.avi
│       ├── cam_metadata_0.csv
│       ├── cam_metadata_1.csv
│       ├── events/
│       │   ├── behavior_0_32.bin
│       │   ├── behavior_0_33.bin
│       │   ├── behavior_1_32.bin
│       │   ├── behavior_1_33.bin
│       │   ├── soundcard_0_32.bin
│       │   ├── soundcard_0_33.bin
│       │   ├── soundcard_1_32.bin
│       │   ├── soundcard_1_33.bin
│       │   ├── left_pump_0_32.bin
│       │   ├── left_pump_0_33.bin
│       │   ├── left_pump_1_32.bin
│       │   ├── left_pump_1_33.bin
│       │   ├── right_pump_0_32.bin
│       │   ├── right_pump_0_33.bin
│       │   ├── right_pump_1_32.bin
│       │   ├── right_pump_1_33.bin
│       │   ├── current_driver_0_32.bin
│       │   ├── current_driver_0_33.bin
│       │   ├── current_driver_1_32.bin
│       │   └── current_driver_1_33.bin
│       └── config/
│           ├── animal_0.yml
│           ├── animal_1.yml
│           ├── setup_0.csv
│           ├── setup_1.csv
│           ├── training_0.csv
│           └── training_1.csv
└── Rat002/
    └── 241003/
        ├── out_0.json
        ├── out_0.csv
        ├── video_0.avi
        ├── cam_metadata_0.csv
        ├── events/
        │   ├── behavior_0_32.bin
        │   ├── behavior_0_33.bin
        │   ├── soundcard_0_32.bin
        │   ├── soundcard_0_33.bin
        │   ├── left_pump_0_32.bin
        │   ├── left_pump_0_33.bin
        │   ├── right_pump_0_32.bin
        │   ├── right_pump_0_33.bin
        │   ├── current_driver_0_32.bin
        │   └── current_driver_0_33.bin
        └── config/
            ├── animal_0.yml
            ├── setup_0.csv
            └── training_0.csv
```

Inside the output directory there is a folder for every animal. Inside each animal's folder there is a folder for every session day, whose name is in the `YYMMDD` format, and inside every session day folder there are different files and folders types:
- `out_X.json` - this is the main output file and has the output data from every trial from every session an animal did so far as Bonsai saves it.
- `out_X.csv` - this is the CSV version of the `out_X.json` file, since it is a more human readable format. This file is generated by a Python script that runs after Bonsai closes.
- `video_X.avi` - this is the CSV version of the `out_X.json` file, since it is a more human readable format. This file is generated by a Python script that runs after Bonsai closes.
- `cam_metadata_X.csv` - this is the CSV version of the `out_X.json` file, since it is a more human readable format. This file is generated by a Python script that runs after Bonsai closes.
- `events/` - this directory has every event from every Harp device connected during a session. The files inside this directory have a name formatted as follows: [_device_name_]\_X\_[_register_].bin. Basically, there's a different file with Harp messages per device register.
- `config/`- this directory contains a copy of the configuration files used in the current session.

> [!CAUTION]
> Don't store any other files in the output directory that are not generated automatically during a session and don't change the names of the files. Some operations - auto-update of configuration files, the numbers in the file names - depend on the files saved by the task's software and on the way they are saved.
>
> If there's a need to manually save other files related to the experiment, please do it somewhere else.