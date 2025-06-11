---
_layout: landing
---

# Home

Welcome to the documentation for the Bonsai workflow developed for the Sound Lateralization Task that is going to be performed by the Circuit Dynamics and Computation group at the Champalimaud Foundation.

The experimental setup makes use of the capabilities of the Harp devices (which implement the [Harp](https://harp-tech.org/) protocol) and the [Bonsai](https://bonsai-rx.org/) visual programming framework, which work really well together. 

The documentation for the task is divided in 3 sections:
- **[Installation and Configuration](./installation/software.md)** - This section is a step-by-step guide for setting up everything that is needed to run the task in a new setup. It includes instructions for installing the task's software, the firmware for each Harp device used in the task, calibrating the hardware and configuring the task.
- **[Task](./articles/introduction.md)** - This is the section where the task is described. It contains a high-level explanation of the task, as well as a more low-level one.
- **[Extensions](./api/CF.yml)** - Since there was a need to create custom Bonsai nodes written in C# to implement functionality which was difficult to implement or wasn't available natively in Bonsai (namely the reading of configuration files), a section documenting these nodes had to be created. There is also a description of every parameter from each configuration file.

If you find any bug in the project or any missing/incorrect/out-of-date documentation, feel free to create an issue on [GitHub](https://github.com/fchampalimaud/CDC.SoundLateralizationTask) or contribute with a pull-request.

If you want to build the documentation locally click [here](./documentation.md).