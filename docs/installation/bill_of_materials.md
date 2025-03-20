# Bill of Materials

## Harp

### Boards
| Item | Description | Amount | Observations |
|------|-------------|:------:|--------------|
| Harp Behavior | General-purpose Harp board | 1 | - |
| Harp SoundCard | Delivers the auditory stimulus | 1 | - |
| Harp Audio Amplifiers | Amplifies the auditory stimulus | 2 | 1 Harp Audio Amplifier per speaker |
| Harp ClockSynchronizer | Synchronizes the timestamps from every Harp device | 1 | - |
| Harp SyringePump | Device used for reward delivery | 2 | - |
| Harp CurrentDriver | Drives/controls the LED/laser used in optogenetics | 1 | Optional |

### Peripherals

| Item | Description | Amount | Part Number | Observations |
|------|-------------|:------:|:-----------:|--------------|
| Behavior Poke Port Breakout v1.1 | Makes the ethernet ports pins from the Harp Behavior available | 3 | - | Connects to the Harp Behavior |
| RJ-to-RJ cables | - | 3 | _TODO_ | Connects the Harp Behavior to the Behavior Poke Port Breakout v1.1 |
| Poke Small v1.1 | Board with infrared beam to detect animal pokes | 3 | - | Connects to the Behavior Poke Port Breakout v1.1 |
| 3.5 mm-stereo-audio-jack-to-bare-wires | - | 3 | _TODO_ | Connects the Poke Small v1.1 to the Behavior Poke Port Breakout v1.1 |
| 5 mm white/blue LED | Placed on the box lid to give cues to the animal | 1 | - | Connects to the LED0 pins of the Harp Behavior |
| 3 mm green LED | Placed in the central poke to give cues to the animal | 1 | - | Connects to the LED1 pins of the Harp Behavior |
| RCA-to-RCA cables | - | 2 | _TODO_ | Connects each Harp Audio Amplifier to the Harp SoundCard |
| Speakers | Deliver the auditory stimulus | 2 | _TODO_ | 1 speaker per Harp Audio Amplifier |
| Banana Plug | 4 mm Triple Contact Plug | 2 | _TODO_ | Connects the speakers to the Harp Audio Amplifiers |
| 10 ml Glass Syringe | | 2 | _TODO_ | Used for the Harp SyringePump |
| 4-way Stopcock | Attaches to the end of the syringe | 2 | _TODO_ | 1 per Harp SyringePump |
| Nylon Male Luer Fitting | Attaches to one end of the stopcock | 2 | _TODO_ | 1 per Harp SyringePump |
| Nylon Female Luer Fitting | Attaches to one end of the stopcock | 2 | _TODO_ | 1 per Harp SyringePump |
| Spouts | Used in reward delivery | 2 | _TODO_ | Glued to the physical lateral pokes
| Flexible Tubing | Used in reward delivery | 2 | _TODO_ | Connects the spouts to one of the luer fittings (either male or female) |
| Mini USB cable | - | 5/6* | _TODO_ | Connects the Harp boards to the computer |
| Micro USB cable | - | 1 | _TODO_ | Used to upload sounds to the Harp SoundCard |
| 3.5 mm-stereo-audio-jack-to-jack cable | - | 4/5* | _TODO_ | Connects the Harp ClockSynchronizer to every other Harp device |
| 12V Power Supply** | - | 9/10* | _TODO_ | 1 is used to power the LED strip that illuminates the behavior box, the remaining are used to power the Harp devices

\* if the Harp CurrentDriver is being used

** the number of power supplies can be decreased as explained [here](TODO)

## Camera

## Others