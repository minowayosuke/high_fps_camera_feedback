# high_fps_camera_feedback
Codes for our paper: ["Imaging-based feedback cooling of a levitated nanoparticle" doi:10.1063/5.0095614](https://aip.scitation.org/doi/10.1063/5.0095614)
or [arXiv:2204.05506 [quant-ph]](https://arxiv.org/abs/2204.05506)

if you find the codes useful, please consider citing the paper as:
>Review of Scientific Instruments 93, 075109 (2022). https://doi.org/10.1063/5.0095614

All the explanation here is based on the hardware, firmware and software version used in the paper (see below).

The code is targeted for [OpenMV camera unit](https://openmv.io/) and written in MicroPython (MicroPython implements a subset of Python functionality). This nice system integrates a CMOS camera sensor with a microcontroller. So, we can implement a real-time processing of taken images and output some analogu/digital signals. You can get images at a high fps (~ 1000 fps) with real-time processing in an integrated microcontroller. The resulting signal can be output from the unit through DAC or DIO pins and can be used for various purposes e.g. feedback cooling of a levitated nano-oscillator for our case.

The actual fps strongly depends on the size of the region-of-interest and the implementation of the image-processing.

## Hardware
We used OpenMV Cam H7 R1 and Global Shutter Camera Module for the experiment in the paper. We recommend using the updated version of the OpenMV cam since the version we used is not available anymore. The basic idea of the code should be working also in the newer OpenMV cam module although we did not test the code in the newer one.

## Firmware
The firmware version used in the paper was v3.5.2. IDE version was v2.4.0.

## Software
### Main idea to get higher fps
To get higher fps, you need to restrict the region of interest. For example, we can reach ***above 1000 fps*** (note that the maximum frame rate may depends on the hardware and firmware version) for 32x20 pixels without any image processing. However, it may be not practical to operate at such a high speed because the DAC is working only at 1 kHz and above-1-kHz speed is useless for most purposes. Additionally, we experienced a hung-up of IDE often for > 1000fps. We didn't check whether it's just a problem of IDE or some kind of thermal runaway of the chip. We never experienced such behavior well below 1000 fps. Possibly, this issue may have been or will be fixed for a newer version.

### Setting region of interest
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
However, the derived image size is still 640x480. The actual image in the region of interest is reshaped to 640x480 (just like as numpy's reshape function with zero-padding). So, it may be convenient to set windowing before getting the image. As far as we know the smallest window we can set without error is 640x8. So,
```
sensor.set_windowing((0,0,640,8)) 
```
before `sensor.snapshot()`.

### Image processing
You can use MicroPython and its libraries for image processing. Note that MicroPython has limited functionality compared to normal Python. We used a micropython library called ulab, the MicroPython's equivalent of numpy. ulab's capability strongly depends on the firmware version. Also, some features of ulab seemed to be slower than expected. So, we used only a part of its functionality. We determined the levitated nanoparticle position using the centroid scheme as described in our paper. 

### Code examples
feedback_cooling.py is the code for the feedback cooling used in the paper.

minimal_exapmle.py is a minimal code example for high-speed image capture.

Note that these two codes are tested **only under the environment specified above.**

Finally, we quickly checked the minimal code example with OpenMV Cam H7 Plus, global shutter caera module and firmware v4.3.1 just for reference. The code itself was not used in our paper. We didn't conduct an in-depth-test and don't guarantee its functioning.

