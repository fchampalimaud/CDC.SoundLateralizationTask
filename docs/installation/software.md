# Software Installation

The task's software is composed by the Bonsai workflow, which contains the task logic, and by small Python scripts that perform some operations at the beginning and at the end of the a session (namely, parsing both input and output files from/to more human readable formats). In order to facilitate the deployment of the project and with reproducibility in mind, the Bonsai workflow was developed inside a Bonsai environment and the Python scripts uses [uv](https://github.com/astral-sh/uv) to create and maintain the Python virtual environment.

To install the task's software, follow the steps:
1. Download the source code from the latest project [release](https://github.com/fchampalimaud/CDC.SoundLateralizationTask/releases/latest) and unzip it. Alternatively, clone the [repository](https://github.com/fchampalimaud/CDC.SoundLateralizationTask).
2. Run `./Setup.cmd` to install the Bonsai environment and the Python environment. An application window will appear which is used to specify the COM port each Harp device corresponds to and the paths to the configuration files and the output directory.
3. Download the configuration files templates (`animal.yml`, `setup.csv`, `training.csv`) from the release mentioned in step 1 and place them wherever it's more convenient.
4. After configuring every parameter present in the application, click on the `Update Configuration` button. The button will generate the `./src/config/config.yml` file, which is a hard-coded file used by both the Python scripts and the Bonsai workflow. Close the application window.

> [!CAUTION]
> Please don't move or delete the `./src/config/config.yml` file! If, for some reason, any of the paths or COM ports need to be changed, re-run the `Setup.cmd` script.

## Additional Software

### Spinnaker Drivers

In order to use the FLIR camera to record the sessions, the [Spinnaker drivers](https://flir.netx.net/file/asset/54630/original/attachment) MUST be installed as well. It's mandatory that the computer has the version 1.29.0.5 of the drivers installed, since the version supported by Spinnaker Bonsai Package. After opening the installer, follow the steps below:
1. Click on `Next`. Then, accept the terms and click on `Next` again.
2. Select `Application Development` and click on `Next`.
3. Deselect `GigE Driver` and click on `Next`.
4. Deselect the `I will use GigE Cameras.` checkbox and click on `Next`.
5. Finally, click on `Install`.


### FFmpeg

The task's code makes use of the FFmpeg software to save the video recordings in the disk, because it allows the video to be recorded with higher framerates, without loss of image quality and by making a better use of the computer's resources than the native `VideoWriter` Bonsai node.

FFmpeg can be installed with WinGet by running the following command in the Terminal:

```
winget install Gyan.FFmpeg
```
