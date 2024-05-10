# Sound Lateralization Task - Harp Bonsai Setup

This is a repository containing the Bonsai workflow developed for the Sound Lateralization Task that is going to be performed by the Renart Lab at the Champalimaud Foundation.

## Instalation
1. Download this repository (or clone it).
2. Run `./bonsai/Setup.cmd` to download and generate the Bonsai environment.
3. Install the firmwares of the Harp devices (see the [Firmware](#firmware) section).

## Firmware
To install the firmwares from all Harp devices except the Harp Soundcard, follow the procedure:
1. Open the `./src/firmware_installation.bonsai` workflow (run `./bonsai/Bonsai.exe` to open Bonsai through the environment).
2. Click the Device node and select the PortName that corresponds to the device whose firmware is going to be installed.
3. Double-click the Device node. Then, click on `Bootloader>>` and then on `Open...`.
4. Open the correct firmware file from the `./firmware` folder and then click on `Update`.
    - Harp Behavior v2.0 -> Behavior-fw3.2-harp1.13-hw2.0-ass0.hex

To install the Harp Soundcard firmware, read the [Install Drivers](https://github.com/harp-tech/device.soundcard?tab=readme-ov-file#install-drivers) and the [Firmware](https://github.com/harp-tech/device.soundcard?tab=readme-ov-file#firmware) sections of the device's repository.

## Documentation
A small PDF file can be found inside the `./docs` folder.