# Software Installation

The task's software is composed by the Bonsai workflow, which contains the task logic, and by small Python scripts that perform some operations at the beginning and at the end of the a session (namely, parsing both input and output files from/to more human readable formats). In order to facilitate the deployment of the project and with reproducibility in mind, the Bonsai workflow was developed inside a Bonsai environment and the Python scripts uses [uv](https://github.com/astral-sh/uv) to create and maintain the Python virtual environment.

To install the task's software, follow the steps:
1. Download the source code from the latest project [release](TODO) and unzip it. Alternatively, clone the [repository](https://github.com/fchampalimaud/CDC.SoundLateralizationTask).
2. Run `./Setup.cmd` to install the Bonsai environment and the Python environment. An application window will appear which is used to specify the COM port each Harp device corresponds to and the paths to the configuration files and the output directory. (_FIGURE_)
3. Download the configuration files templates (`animal.yml`, `setup.csv`, `training.csv`) from the release mentioned in step 1 and place them wherever it's more convenient.
4. After configuring every parameter present in the application, click on the `Update Configuration` button. The button will generate the `./src/config/config.yml` file, which is a hard-coded file used by both the Python scripts and the Bonsai workflow. Close the application window.

> [!CAUTION]
> Please don't move or delete the `./src/config/config.yml` file! If, for some reason, any of the paths or COM ports need to be changed, re-run the `Setup.cmd` script.

## Additional Software

In order to use the FLIR camera to record the sessions, the [Spinnaker drivers](TODO) MUST be installed as well. It's mandatory that the computer has the version 1.29.X.X of the drivers installed, since the version supported by Spinnaker Bonsai Package.

_TODO: specify the steps to follow_
