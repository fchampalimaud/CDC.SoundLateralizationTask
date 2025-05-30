# Camera Configuration

The setups need a camera to record the sessions. At the moment, the cameras being used are BFS-U3-16S2M-CS from FLIR. These cameras need to be configured so that they meet the following requirements:
- the frame rate is 100 fps.
- the camera sends a digital signal to the Harp Behavior that signals when each frame is acquired.

After installing the [Spinnaker Drivers](software.md#spinnaker-drivers), connect the camera to the computer in an USB-3.0 port (connecting it to an USB-2.0 port limits the camera's capabilities, namely the frame rate) and follow the instructions:

1. Open the SpinView software.
2. Select the camera to be configured.
3. Click on `Features`.
4. Click on the camera model name and then on `Acquisition Control`.
5. Change the `Acquisition Frame Rate` parameter to the desired value.
6. Close the `Acquisition Control` section and open the one named `Digital IO Control`.
7. Select the `Line 2` in the `Line Selector` parameter.
8. Change the `Line Mode` to `Output`.
9. Close the `Digital IO Control` section and open the one named `User Set Control`.
10. Select an `User Set Selector` other than `Default`.
11. Select the same User Set in the `User Set Default` parameter.
12. Finally, click on the `User Set Save` button to save the current User Set.
13. _Optional_: Click on `Image Format` to change the camera resolution and save the User Set again.

_TODO: add figures of configuration and strobe cable_
