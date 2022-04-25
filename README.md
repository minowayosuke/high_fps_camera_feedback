# high_fps_camera_feedback
Code for our paper: "textexttextext" doi???????????????

The code is targeted for [OpenMV camera unit](https://openmv.io/) and written in MicroPython (MicroPython implements a subset of Python functionality). You can get images at a high fps (possibly > 500 fps) with real-time processing. The resulting signal can be output from the unit through DAC or DIO pins and can be used for various purposes e.g. feedback cooling of a levitated nano-oscillator for our case.

The actual fps strongly depends on the size of the region-of-interst and the content of the image-processing.

## Hardware
We used OpenMV Cam H7 R1 and Global Shutter Camera Module for the experiment in the paper. We recommend to use the updated version of the OpenMV cam since the version we used is not available anymore. The basic idea of the code should be working also in the newer OpenMV cam moudle although we did not test the code in the newer one.

## Firmware
Firmware version used in the paper was v3.5.2. IDE version was v2.4.0.

## Software
### Main idea to get higher fps
To get higher fps, you need to restrict the region of interst. For example, we can reach well above 1000 fps for 32x20 pixels without any image processing. However, it's not recommended because the DAC is working only at 1khz and above-1-khz speed is useless for most of the purpose. Additionally, we experienced a hung-up of IDE often for > 1000fps. We didn't check whether it's just a problem of IDE or a some kind of thermal runaway of chip. We never expereienced a such behavior well below 1000 fps. Possibly, this issue may have been or will be fixed for newer version.

### Setting region of interst
You should choose an appropriate region of interest from the default pixel format 640x480(VGA) by using `sensor.__write_reg()`function,
~~~
sensor.__write_reg(0x01,X)              # Column position, 1-752
sensor.__write_reg(0x02,Y)              # Row position, 4-482
sensor.__write_reg(0x03,H)              # region of interest Height, 1-480
sensor.__write_reg(0x04,W)              # region of interest Width, 1-752
~~~
where the coordinate origin is at the lower right corner.

After setting the region of interest, you can get the image by
```
image = sensor.snapshot()          # Take a picture and return the image.
```
However, the derived image size is still 640x480. The actual image in the region of interest is reshpaed to 640x480 (just like as numpy's reshape function with zero-padding). So, it may be convinient to set windowing before getting the image. As far as we know the smallest window we can set without error is 640x8. So,
```
sensor.set_windowing((0,0,640,8)) 
```
before `sensor.snapshot()`.

### Image processing
You can use MicroPython and its libraries for image processing. Note that MicroPython has a limited functionality compared to normal Python. We used a micropython library called ulab, the MicroPython's equivalent of numpy. 
