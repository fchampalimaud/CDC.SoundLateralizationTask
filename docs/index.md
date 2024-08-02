---
_layout: landing
---

# Home

Welcome to the documentation for the Bonsai workflow developed for the Sound Lateralization Task that is going to be performed by the Circuit Dynamics and Computation group at the Champalimaud Foundation.

The experimental setup makes use of the capabilities of the Harp devices (which implement the [Harp](https://harp-tech.org/) protocol) and the [Bonsai](https://bonsai-rx.org/) visual programming framework, which work really well together. 

The documentation for the task is divided in 3 sections:
- **[Install](./installation/bonsai.md)** - This section is a step-by-step guide for installing everything that is needed to run the task in a new setup. It includes instructions for installing the Bonsai environment and the firmware for each Harp board used during the task.
- **[Task](./articles/introduction.md)** - This is the section where the task is described. It contains a high-level explanation of the task, as well as a user guide of how the task should be run (it includes a description of every input and output parameter). It also has explanations regarding some of the Bonsai implementation details.
- **[Package](./api/SLTUtils.yml)** - Since a custom Bonsai package that adds new nodes with functionality which was difficulty to implement or wasn't available natively in Bonsai (namely the reading of configuration files) was created, there was a need to create a section documenting it.