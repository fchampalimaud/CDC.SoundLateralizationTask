# Camera Setup

The setups need a camera to record the sessions. At the moment, the cameras being used are FL3-U3-13S2M from Point Grey. These cameras need to be configured so that they meet the following requirements:
- the frame rate is 100 fps.
- the camera sends a digital signal to the Harp Behavior that signals when each frame is acquired.

The first step is to install the Point Grey FlyCap2 program which includes the:
- the program used to configure the camera.
- the camera drivers.
- the camera SDK used by the Point Grey Bonsai package so that the camera works in Bonsai.

After installing the program, connect the camera to the computer in an USB-3.0 port (connecting it to an USB-2.0 port limits the camera's capabilities, namely the frame rate).

_TODO: configuration itself and strobe cable_