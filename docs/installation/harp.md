# Harp

This task uses the following Harp boards:
- 1 Harp Behavior
- 1 Harp SoundCard
- 2 Harp Audio Amplifiers
<!-- - 1 Harp Clock Synchronizer -->

In order to use the Harp Behavior and the Harp SoundCard, the USB drivers and the each board's firmware must be installed. The installer for the USB drivers can be downloaded [here](https://bitbucket.org/fchampalimaud/downloads/downloads/UsbDriver-2.12.26.zip). The [Firmware](#firmware) section contains the instructions for installing each board's firmware.

## Firmware
For most boards, it's possible to install the corresponding firmware in two different ways. Unfortunately, only one method is available for the Harp SoundCard. Nevertheless, both methods are described below.

### Firmware Download
1. Go to the [Harp Tech GitHub organization](https://github.com/harp-tech).
2. Search for the board's repository. The name of the repository follows the format device.[_board_name_] (for example, [device.behavior](https://github.com/harp-tech/device.behavior)).
3. Click on `Releases` and search for the latest firmware release, whose name follows the format fw[_firmware_version_]-harp[_harp_core_version_] (for example, fw2.2-harp1.13).
4. Download the latest version of the firmware binary corresponding to the hardware version of the board being used. The firmware binary name follows the format [_board_name_]-fw[_firmware_version_]-harp[_harp_core_version_]-hw[_hardware_version_]-ass[_assembly_version_].hex (for example, Behavior-fw3.2-harp1.13-hw2.0-ass0.hex).
    - **Note:** For the Harp SoundCard, an additional firmware binary must be downloaded (the PIC32 firmware).

### Via Harp Convert to CSV GUI
If the Harp Convert to CSV GUI is already installed, skip to step 3. If it's not already installed, but other Labview-based Harp board GUI is, skip to step 2 instead.

1. Install the [LabView Runtime](https://bitbucket.org/fchampalimaud/downloads/downloads/Runtime-1.0.zip) and reboot the computer.
2. Install the latest version of the [Harp Convert to CSV GUI](https://github.com/harp-tech/csv_converter/releases/tag/1.9.0-preview).
3. Open the Harp Convert to CSV GUI.
4. Click on `Options` and write "bootloader" in the `List` textbox. The _Update Firmware_ window should appear.
5. Choose the communication port (_COMx_) of the board whose firmware is going to be installed.
6. Select the firmware binary to be installed and click on `Update`.
    - **Note:** For the Harp SoundCard, during the installation of the firmware, select the PIC32 firmware when the application asks for the 32 bits device firmware.

### Via Bonsai
As explained at the beginning of the [section](#firmware), it is not possible to install the Harp SoundCard firmware through this method. Skip to step 4 if the Bonsai environment is already installed.

1. Install [Bonsai](https://bonsai-rx.org/docs/articles/installation.html).
2. Open Bonsai and click on `Manage Packages`.
3. Install the following packages:
    - Bonsai - Harp Library
    - Bonsai - Harp Design Library
4. Start a new workflow and add a Device node from the Harp package to it.
5. Change the `PortName` property of the node to the communication port (_COMx_) of the board whose firmware is going to be installed.
6. Double-click on the Device node. The _Device Setup_ window should appear.
7. Click on `Bootloader>>`. The _Device Setup_ should expand.
8. Click on `Open...` to select the firmware binary to be installed and then click on `Update`.