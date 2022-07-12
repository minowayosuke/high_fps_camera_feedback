# Cold damping & Phase shift & UARTconect & DAC

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

uart = UART(3, 115200, timeout_char = 0)
uart.init(115200, bits=8, parity=None, stop=1, timeout_char=0,timeout=0)

from pyb import DAC
dac = DAC("P6", bits=12, buffering=True)     # create DAC on pin P6

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

BIT = 4096                              # 8bits=255, 12bits=4095

Delay = 4                               # number of loops for delaying


sensor.skip_frames(time = 2000)         # Wait for settings take effect. Time[ms]
clock = time.clock()                    # Create a clock object to track the FPS.

T=5000
sensor.set_auto_exposure(False, exposure_us=T)     # make smaller to go faster.

pixelclock=43                                # pixel clock HAS TO BE AN INT in MHz.
video = np.zeros((h,w), dtype=np.uint8)
centroid = np.zeros((Delay+1,1), dtype=np.float)
OutputVoltage = np.zeros((Delay+1,1), dtype=np.float)

kk=0
while(True):
    clock.tick()                       # Update the FPS clock.

    video = sensor.snapshot()          # Take a picture and return the image.

    video_list = list(video[0:w])

    video_list2 = [n**3 for n in video_list]

    m_sum = sum(video_list2)

    n=0
    M_sum=0
    while n < H:
        i = 0+W*n
        j = W+W*n
        video_list_col = video_list2[i:j]
        col_sum = sum(video_list_col)
        M_sum_col = col_sum * n
        M_sum = M_sum + M_sum_col
        n = n+1

    numMax=np.argmax(video_list)

    row = int(numMax/W)                 #

    if m_sum == 0 :
        z_centroid = row                # avoid zero-division. replacing the centroid with brightest pixel position
    else:
        z_centroid = M_sum / m_sum      #　calculate centroid

    if 0 < z_centroid < H :
        z_centroid = z_centroid

    elif z_centroid >= H :
        z_centroid = H

    else :
        z_centroid = 0

    if Delay == 0 :
        V_1 = int(BIT*(H-z_centroid)/H)


        strdata=str(V_1)                            #for uart communication
        strdata ='{:0>{w}}'.format(strdata, w=4)    #
        uart.write(strdata)                         #
        dac.write(V_1)

    else :
        if kk < Delay :
            amari = int(kk%(Delay+1))
            amari2 = int((kk+Delay)%(Delay+1))
            OutputVoltage[amari2,0:1]=np.array([z_centroid])

        else :
            amari = int(kk%(Delay+1))
            amari2 = int((kk+Delay)%(Delay+1))
            OutputVoltage[amari2,0:1]=np.array([z_centroid])

            Centroid = OutputVoltage[amari]
            Centroid2 = Centroid[0]




            V_1 = int(BIT*Centroid2/H)  #
                                        #

            strdata=str(V_1)                            #for uart communication
            strdata ='{:0>{w}}'.format(strdata, w=4)    #
            uart.write(strdata)                         #
            dac.write(V_1)



    print(clock.fps())
