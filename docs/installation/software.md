# Software Installation

The task's software is composed by the Bonsai workflow, which contains the task logic, and by a small Python application, which allows for real-time monitoring of the task and some interaction with it. In order to facilitate the deployment of the project and with reproducibility in mind, the Bonsai workflow was developed inside a Bonsai environment and the Python application uses [uv](https://github.com/astral-sh/uv) to create and maintain the Python virtual environment.

To install the task's software, follow the steps:
1. Clone the [GitHub repository](https://github.com/fchampalimaud/CDC.SoundLateralizationTask) (or download it for non-git users).
2. Run `./Setup.cmd` to install the Bonsai environment and uv. The Python environment will be installed the first time the project is run.