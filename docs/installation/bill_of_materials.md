# Bill of Materials

This bill of materials (BOM) contains **EVERYTHING** needed to build a setup. From the less memorable screw to the super expensive syringes used for reward delivery. 

> [!NOTE]
> This BOM is destined to the people from the Champalimaud Foundation (CF). Nonetheless, the goal is that people outside CF are also able to order everything and build the setup.

## Harp
This section contains the setup components that relate to the Harp devices somehow (except for the Camera that has a section of its own).

### Devices
The Harp devices are assembled by the Hardware and Software Platform, so place an Agendo request to order them.

> [!WARNING]
> For people outside of the Champalimaud Foundation, it's possible to order the Harp devices in the [Open Ephys Production Site](https://open-ephys.org/harp).
> 
> It's also possible to assemble the devices in-house with the right equipment since all of them are under an open source license. Some devices (like the Harp SyringePump) must be built in-house since they are not sold externally.

| Item | Description | Amount | Observations |
|------|-------------|:------:|--------------|
| [Harp Behavior](https://github.com/harp-tech/device.behavior) | General-purpose Harp board | 1 | - |
| [Harp SoundCard](https://github.com/harp-tech/device.soundcard) | Delivers the auditory stimulus | 1 | - |
| [Harp Audio Amplifiers](https://github.com/harp-tech/peripheral.audioamp) | Amplifies the auditory stimulus | 2 | 1 Harp Audio Amplifier per speaker |
| [Harp ClockSynchronizer](https://github.com/harp-tech/device.clocksynchronizer) | Synchronizes the timestamps from every Harp device | 1 | - |
| [Harp SyringePump](https://github.com/harp-tech/device.syringepump) | Device used for reward delivery | 2 | - |
| [Harp CurrentDriver](https://github.com/fchampalimaud/device.currentdriver) | Drives/controls the LED/laser used in optogenetics | 1 | Optional |

### Peripherals
For this part of the BOM, a peripheral is considered to be anything that either interacts with the Harp devices or is needed make the different devices work and/or interact with each other.

| Item | Description | Amount | Part Number | Comes with Harp Device | Agendo | Observations |
|------|-------------|:------:|:-----------:|:----------------------:|:------:|--------------|
| [Behavior Poke Port Breakout v1.1](https://github.com/harp-tech/peripheral.portbreakout) | Makes the ethernet ports pins from the Harp Behavior available | 3 | - | :x: | :heavy_check_mark: | Connects to the Harp Behavior |
| [RJ-to-RJ cables](https://www.pcdiga.com/adaptadores-e-cabos/conectividade-de-rede/cabos-de-rede-rj45/cabo-de-rede-ewent-im1037-cat-6-u-utp-slim-100-cobre-1m-branco-im1037-8054392618567) | - | 3 | IM1037 | :x: | :x: | Connects the Harp Behavior to the Behavior Poke Port Breakout v1.1 |
| Poke Small v1.1 | Board with infrared beam to detect animal pokes | 3 | - | :x: | :heavy_check_mark: | Connects to the Behavior Poke Port Breakout v1.1 |
| 3.5 mm-stereo-audio-jack-to-bare-wires | - | 3 | _TODO_ | :x: | :x: | Connects the Poke Small v1.1 to the Behavior Poke Port Breakout v1.1 |
| 5 mm white/blue LED | Placed on the box lid to give cues to the animal | 1 | - | :x: | :x: | Connects to the LED0 pins of the Harp Behavior |
| 3 mm green LED | Placed in the central poke to give cues to the animal | 1 | - | :x: | :x: | Connects to the LED1 pins of the Harp Behavior |
| RCA-to-RCA cables | - | 2 | - | :heavy_check_mark: | :x: | Connects each Harp Audio Amplifier to the Harp SoundCard |
| Speakers | Deliver the auditory stimulus | 2 | _TODO_ | :x: | :x: | 1 speaker per Harp Audio Amplifier |
| [Banana Plug](https://pt.mouser.com/ProductDetail/Deltron/557-0100?qs=lj71xN7SzAKK0gloei9mgg%3D%3D) | 4 mm Triple Contact Plug (Black or Red) - Pack of 10 units | 4 | 557-0100 | :x: | :x: | Connects the speakers to the Harp Audio Amplifiers |
| [10 ml Glass Syringe](https://www.fishersci.pt/shop/products/hamilton-1000-series-gastight-syringes-luer-lock-syringes-tll-termination-14/10683921) | Hamilton 1000 Series Gastight Syringes: Luer Lock Syringes, TLL Termination | 2 | Hamilton 81620 | :x: | :x: | Used for the Harp SyringePump |
| [4-way Stopcock](https://www.fishersci.pt/shop/products/4-way-stopcock/11742683) | Pack of 10 units | 2 | Masterflex 30600-04 | :x: | :x: | Attaches to the end of the syringe (1 per Harp SyringePump) |
| [Nylon Male Luer Fitting](https://www.fishersci.pt/shop/products/cole-parmer-nylon-male-luer-fitting/11755818?crossRef=mflx45505-31&searchHijack=true&searchTerm=mflx45505-31&searchType=RAPID&matchedCatNo=mflx45505-31) | Pack of 25 units | 2 | Masterflex MFLX45505-31 | :x: | :x: | Attaches to one end of the stopcock (1 per Harp SyringePump) |
| [Nylon Female Luer Fitting](https://www.fishersci.pt/shop/products/nylon-luer-fitting/11745818) | Pack of 25 units | 2 | Masterflex 45502-00 | :x: | :x: | Attaches to one end of the stopcock (1 per Harp SyringePump) |
| Spouts | Used in reward delivery | 2 | _TODO_ | :x: | :x: | Glued to the physical lateral pokes
| [Flexible Tubing](https://www.fishersci.pt/shop/products/tygon-e-3603-non-dehp-tubing/14861161) | Masterflex Tygon E-3603 Non-DEHP Tubing - 15 meters per unit | 2 | Masterflex 06407-71 | :x: | :x: | Connects the spouts to one of the luer fittings (either male or female) |
| [Mini USB cable](https://www.tme.com/in/en/details/ak-300130-018-s/usb-cables-and-adapters/digitus/) | - | 5/6* | AK-300130-018-S | :heavy_check_mark: | :x: | Connects the Harp boards to the computer |
| Micro USB cable | - | 1 | - | :heavy_check_mark: | :x: | Used to upload sounds to the Harp SoundCard |
| 3.5 mm-stereo-audio-jack-to-jack cable | - | 4/5* | _TODO_ | :x: | :x: | Connects the Harp ClockSynchronizer to every other Harp device |
| [12V Power Supply](https://www.digikey.pt/en/products/detail/xp-power/VER12US120-JA/5726836)** | AC/DC Wall Mount Adapter 12V 12W | 9/10* | VER12US120-JA | :heavy_check_mark:*** | :x: | 1 is used to power the LED strip that illuminates the behavior box, the remaining are used to power the Harp devices |

\* if the Harp CurrentDriver is being used

** the number of power supplies can be decreased as explained [here](TODO)

*** the power supply used to power the LED strip that illuminates the behavior box must be ordered separately

## Camera

| Item | Description | Amount | Part Number | Observations |
|------|-------------|:------:|:-----------:|--------------|
| FLIR Camera | | 1 | BFS-U3-16S2M-CS | - |
| Camera Lens | | 1 | A4Z2812CS-MPIR | - |
| Camera USB cable | USB-A to Micro-B Straight with Thumbscrews, 3 Meters | 1 | CEI USB3-1-1-2-3M | This cable MUST be connected to a USB 3.0 port for performance |
| Camera GPIO cable | 6 Pin Female Straight Plug (Hirose HR10A-7P-6S) to Flying Leads, 3 Meters | 1 | CEI MVA-50-3-X-3 | Connects to the Harp Behavior to trigger/monitor the camera frames |
| Tripod Adapter | BFS 30 mm BFLY CM3 Tripod Adapter | 1 | ACC-01-0003 | Used to fix the camera to the Thorlabs poles in the behavior box |
| Thorlabs 75mm post | Ø12.7 mm Optical Post, SS, M4 Setscrew, M6 Tap, L = 75 mm | 1 | TR75/M | Connects to the camera |
| Thorlabs 150mm post | Ø12.7 mm Optical Post, SS, M4 Setscrew, M6 Tap, L = 150 mm  | 1 | TR150/M | Fixes the camera structure to the box lid |
| Thorlabs post clamp | Rotating Clamp for Ø1/2" Posts, 360° Continuously Adjustable, 5 mm Hex | 1 | SWC/M | Fixes both Thorlabs posts to each other |
| M6 Screw | 15/16 mm | 1 | | Fixes the longer post to the behavior box lid |
| M6 Setscrew | M6 x 1.0 Stainless Steel Setscrew, 16 mm Long, 25 Pack | 1 | SS6MS16 | Connects the Thorlabs post to the Camera |

## Others

| Item | Description | Amount | Part Number | Observations |
|------|-------------|:------:|:-----------:|--------------|
| Behavior box | - | 1 | - | Made of acrylic |
| Physical pokes | - | 3 | - | Preferably made of metal, but can also be 3D printed |
| Speaker holder | - | 2 | - | Preferably made of metal, but can also be 3D printed |
| Speaker holder pole | Hollow alluminium tube | 2 | - | - |
| Box LED holder | - | 1 | - | 3D printed |

| Item | Description | Amount | Part Number | Observations |
|------|-------------|:------:|:-----------:|--------------|
| Computer | | 1 | | |
| Screen | | 1 | | |
| HDMI cable | | 1 | | |
| Keyboard | | 1 | | |
| Mouse | | 1 | | |
| USB Hub | | 1 | | |
| Power extension with 6 electrical outlets | Must be appropriate to $90 \degree$ plugs | 1 | | To plug all of the power supplies in a setup | 
| KVM switch | | - | | Optional: useful in case one wants to use the same screen + mouse + keyboard kit in different computers
| 12V LED Strip | | 1 | | |
| 2-to-1 cables for the 12V power supplies | | | | |
| 4-to-1 cables for the 12V power supplies | | | | |
| Electrical wire | | | | |
| Optogenetics Light Source | | | | |