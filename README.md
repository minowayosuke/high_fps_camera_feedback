# high_fps_camera_feedback
Code for our paper: "textexttextext" doi???????????????

The code is for [OpenMV camera unit](https://openmv.io/). You can get images at a high fps (possibly > 500 fps) with real-time processing. The resulting signal can be output from the unit through DAC or DIO pins and can be used for various purposes e.g. feedback cooling of a levitated nano-oscillator for our case.

The actual fps strongly depends on the size of the region-of-interst and the content of the image-processing.

## Hardware
We used OpenMV Cam H7 R1 and Global Shutter Camera Module for the experiment in the paper. We recommend to use the updated version of the OpenMV cam since the version we used is not available anymore. The basic idea of the code should be working also in the newer OpenMV cam moudle although We did not test the code in the newer one.

## Firmware
Firmware version used in the paper was v3.5.2. IDE version was v2.4.0.

## Software
### Main idea to get higher fps
To get higher fps, you need to restrict the region of interst. For example, we can reach well above 1000 fps for 32x20 pixels without any image processing. However, it's not recommended because the DAC is working only at 1khz and above-1-khz speed is useless for most of the purpose. Additionally, we experienced a hung-up of IDE often for > 1000fps. We didn't check whether it's just a problem of IDE or a some kind of thermal runaway of chip. We never expereienced a such behavior well below 1000 fps. Possibly, this issue may have been  or will be fixed for newer version.

You should choose an appropriate region of interest from the default pixel 640x480(VGA).

###
