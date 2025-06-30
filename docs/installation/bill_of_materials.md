# Bill of Materials

This bill of materials (BOM) contains **EVERYTHING** needed to build a setup. From the less memorable screw to the super expensive syringes used for reward delivery. 

> [!NOTE]
> This BOM is destined to the people from the Champalimaud Foundation (CF). Nonetheless, the goal is that people outside CF are also able to order everything and build the setup.

> [!WARNING]
> This BOM specifies the part numbers used by the lab for these setups, but not every component needs to be of a specific part number.
>
> The only things that need to be of a specific model are the Harp Devices, the Behavior Poke Port Breakout v1.1, the Poke Small v1.1 and the 12V Power Supplies.
>
> It's possible to use a different camera model, but please confirm that the camera can be used in Bonsai (although for some cameras the Bonsai workflow will probably need to be adapted).

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

| Item | Description | Amount | Part Number | Part of the Harp Device kit | Agendo | Observations |
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
| [Spouts](https://www.fishersci.com/shop/products/14g-2-sterile-blunt-100pk/NC0353208) | Used in reward delivery | 2 | B14200 100 BULK | :x: | :x: | Used in reward delivery. Glued to the physical lateral pokes |
| [Flexible Tubing](https://www.fishersci.pt/shop/products/tygon-e-3603-non-dehp-tubing/14861161) | Masterflex Tygon E-3603 Non-DEHP Tubing - 15 meters per unit | 2 | Masterflex 06407-71 | :x: | :x: | Connects the spouts to one of the luer fittings (either male or female) |
| [Mini USB cable](https://www.tme.com/in/en/details/ak-300130-018-s/usb-cables-and-adapters/digitus/) | - | 5/6* | AK-300130-018-S | :heavy_check_mark: | :x: | Connects the Harp boards to the computer |
| Micro USB cable | - | 1 | - | :heavy_check_mark: | :x: | Used to upload sounds to the Harp SoundCard |
| 3.5 mm-stereo-audio-jack-to-jack cable | - | 4/5* | _TODO_ | :x: | :x: | Connects the Harp ClockSynchronizer to every other Harp device |
| [12V Power Supply](https://www.digikey.pt/en/products/detail/xp-power/VER12US120-JA/5726836)** | AC/DC Wall Mount Adapter 12V 12W | 9/10* | VER12US120-JA | :heavy_check_mark:*** | :x: | 1 is used to power the LED strip that illuminates the behavior box, the remaining are used to power the Harp devices |
| [BNC-to-bare-wires conector](https://pt.rs-online.com/web/p/conectores-de-alimentacion-dc/8104605?gb=a)** | | 1 | 810-4605 | :x: | :x: | Connects the LED strip to the power supply |

\* if the Harp CurrentDriver is being used

** the number of power supplies can be decreased as explained in the subsection [below](#reducing-the-number-of-power-supplies)

*** the power supply used to power the LED strip that illuminates the behavior box must be ordered separately

#### Reducing the number of power supplies
From the table above, it's pretty noticeable that a lot of power supplies are required, which takes up a lot of space and power outlets. It's possible to use the same power supply for different devices according to their characteristics. The devices can be grouped in the following way:
- Harp Behavior, Harp SoundCard and Harp CurrentDriver*
- V+ of the Harp Audio Amplifiers
- V- of the Harp Audio Amplifiers
- Both Harp SyringePumps

From the list above, it's possible to switch the last line from the previous table with the lines from the table below.

| Item | Description | Amount | Part Number | Comes with Harp Device | Agendo | Observations |
|------|-------------|:------:|:-----------:|:----------------------:|:------:|--------------|
| [12V Power Supply](https://www.digikey.pt/en/products/detail/xp-power/VER12US120-JA/5726836) | AC/DC Wall Mount Adapter 12V 12W | 5 | VER12US120-JA | :heavy_check_mark:*** | :x: | 1 is used to power the LED strip that illuminates the behavior box, the remaining are used to power the Harp devices |
| 2-to-1 cables for the 12V power supplies | - | 4/3* | | :x: | :heavy_check_mark:*** | - |
| 4-to-1 cables for the 12V power supplies | - | 0/1* | | :x: | :heavy_check_mark:*** | - |

\* if the Harp CurrentDriver is being used

## Mechanical Components
This section contains the mechanical components of the setup that were developed and assembled in-house.

> [!WARNING]
> The files for the mechanical components are not currently available online and can't also be ordered, so people outside of the Champalimaud Foundation will have to develop and assemble their own.

| Item | Description | Amount | Part Number | Observations |
|------|-------------|:------:|:-----------:|--------------|
| Behavior box | - | 1 | - | Made of acrylic |
| Physical pokes | - | 3 | - | Preferably made of metal, but can also be 3D printed |
| Speaker holder | - | 2 | - | Preferably made of metal, but can also be 3D printed |
| Speaker holder pole | Hollow alluminium tube | 2 | - | - |
| Box LED holder | - | 1 | - | 3D printed |

## Camera
This section contains the hardware needed to setup the camera and fix it to the lid of the behavior box. Click [here](camera.md) to go to the camera configuration instructions.

| Item | Description | Amount | Part Number | Observations |
|------|-------------|:------:|:-----------:|--------------|
| [FLIR Camera](https://www.digikey.pt/en/products/detail/flir-integrated-imaging-solutions-inc/BFS-U3-16S2M-CS/16528335) | | 1 | BFS-U3-16S2M-CS | - |
| [Camera Lens](https://www.computar.com/products/a4z2812cs-mpir) | | 1 | A4Z2812CS-MPIR | - |
| [Camera USB cable](https://machinevisiondirect.com/products/cei-usb3-1-1-2-3m) | USB-A to Micro-B Straight with Thumbscrews, 3 Meters | 1 | CEI USB3-1-1-2-3M | This cable MUST be connected to a USB 3.0 port for performance |
| [Camera GPIO cable](https://machinevisiondirect.com/es/products/cei-mva-50-3-x-3m) | 6 Pin Female Straight Plug (Hirose HR10A-7P-6S) to Flying Leads, 3 Meters | 1 | CEI MVA-50-3-X-3 | Connects to the Harp Behavior to trigger/monitor the camera frames |
| [Tripod Adapter](https://www.digikey.pt/en/products/detail/flir-integrated-imaging-solutions-inc/ACC-01-0003/16528253) | BFS 30 mm BFLY CM3 Tripod Adapter | 1 | ACC-01-0003 | Used to fix the camera to the Thorlabs poles in the behavior box |
| [Thorlabs 75mm post](https://www.thorlabs.com/thorproduct.cfm?partnumber=TR75/M) | Ø12.7 mm Optical Post, SS, M4 Setscrew, M6 Tap, L = 75 mm | 1 | TR75/M | Connects to the camera |
| [Thorlabs 150mm post](https://www.thorlabs.com/thorproduct.cfm?partnumber=TR150/M) | Ø12.7 mm Optical Post, SS, M4 Setscrew, M6 Tap, L = 150 mm  | 1 | TR150/M | Fixes the camera structure to the box lid |
| [Thorlabs post clamp](https://www.thorlabs.com/thorproduct.cfm?partnumber=SWC/M) | Rotating Clamp for Ø1/2" Posts, 360° Continuously Adjustable, 5 mm Hex | 1 | SWC/M | Fixes both Thorlabs posts to each other |
| M6 Screw | 15/16 mm | 1 | | Fixes the longer post to the behavior box lid |
| [M6 Setscrew](https://www.thorlabs.com/thorproduct.cfm?partnumber=SS6MS16) | M6 x 1.0 Stainless Steel Setscrew, 16 mm Long, 25 Pack | 1 | SS6MS16 | Connects the Thorlabs post to the Camera |

## Others
This section contains the remaining components needed for the setup. None of these components needs to be the exact model present on the list. It just corresponds to the models that have been used by the lab, but feel free to use different ones, as long as they work.

| Item | Description | Amount | Part Number | Observations |
|------|-------------|:------:|:-----------:|--------------|
| [Computer](https://www.pccomponentes.pt/mini-pc-blackview-mp100-mini-pc-amd-ryzen-7-5825u-16gb-512gb-ssd) | Mini PC Blackview MP100 Mini PC AMD Ryzen 7 5825U/16GB/512GB SSD  | 1 | MP100(16+512)-BLACK | - |
| Screen | - | 1 | - | - |
| HDMI cable | - | 1 | - | - |
| Keyboard | - | 1 | - | - |
| Mouse | - | 1 | - | - |
| [USB Hub](https://www.pcdiga.com/adaptadores-e-cabos/conectividade-usb/hubs-usb/hub-usb-3-0-tp-link-uh700-7-portas-c-alimentacao-uh700-6935364010065) | HUB USB 3.0 TP-Link UH700 7 Ports | 1 | P004616 | - |
| Power extension with 6 electrical outlets | Must be appropriate to $90 \degree$ plugs | 1 | | To plug all of the power supplies in a setup | 
| [KVM switch](https://www.amazon.es/dp/B0BVMJTLXY/ref=sr_1_2_sspa?crid=6WU6IOXHAZLP&dib=eyJ2IjoiMSJ9.EfBrD9wlGIv0-riV-FMpt72L3A255YeiOZo3vyguBieY8O4F4_1nHK8ls5V9Noa3SfkdZUYzDhWZvhBNNYrla23g3719gx3X6daMLbsfY8nzr8v-qUZnhDC5gLXdy30fHhhCmsD_8lFtFqonJLgOeAIRZw36uTKce0csgpqU3J_SxBvd04xFMewvK1_sl7WVxBGf7pXsR1WmOrAaU1RozUyXWnf7nMbaG92ykg4K2vGxcjPXQgMVDC9ZcE0ZYMbyc0LCv47sImo0EQQlvo4t2EPCG5uHu1-nlVOVF0iMXUA.JC5pA9cScHzf9T-gpyP8p5D4rFot2U_HaLnB1hG5G_8&dib_tag=se&keywords=usb%2Bkvm%2Bswitch&qid=1738754599&sprefix=usb%2Bkvm%2Bswitch%2Caps%2C138&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1) | | - | | Optional: useful in case one wants to use the same screen + mouse + keyboard kit in different computers
| 12V LED Strip | | 1 | | - |
| Optogenetics Light Source | - | - | - | Optional |
