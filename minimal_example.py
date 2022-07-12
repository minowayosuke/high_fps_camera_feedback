# minimal example code for high fps capturing

import sensor, time, image, math
import pyb
import ulab as np
import utime
from pyb import UART

sensor.reset()                          # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE)  # Set pixel format to GRAYSCALE.
sensor.set_framesize(sensor.VGA)        # Set frame size to QQVGA (160x120).
                                        # -make smaller to go faster.
                                        # VGA(640x480) QVGA(320x240) QQQVGA(80x60) QQQQVGA(40x30)


X=338
Y=330
W=32
H=20

sensor.__write_reg(0x01,X)              # Column Start Context A (0x01) 1-752
sensor.__write_reg(0x02,Y)              # Row Start Context A (0x02) 4-482
sensor.__write_reg(0x03,H)              # Window Height Context A (0x03) 1-480
sensor.__write_reg(0x04,W)              # Window Width Context A (0x04) 1-752
sensor.__write_reg(0x05,640)            # Horizontal Blanking Context A (0x05) 43-1023
sensor.__write_reg(0x06,4)              # Vertical Blanking Contact A (0x06) 4-3000

x = 0
y = 0
w = 640
h = 8

sensor.set_windowing((x,y,w,h))         # sensor.set_windowing(roi)
                                        # roi is a rect tuple (x, y, w, h).
                                        # However, you may just pass (w, h) and the roi will be
                                        # -centered on the frame.



sensor.skip_frames(time = 2000)         # Wait for settings take effect. Time[ms]
clock = time.clock()                    # Create a clock object to track the FPS.

T=5
sensor.set_auto_exposure(False, exposure_us=T)     # make smaller to go faster.

pixelclock=43                                # pixel clock HAS TO BE AN INT in MHz.


kk=0
while(True):
    clock.tick()                       # Update the FPS clock.

    video = sensor.snapshot()          # Take a picture and return the image.


    print(clock.fps())
