import time

from sensors import *
from writers import *
from pipes import *

def main():
    with PiCameraSensor() as cam, \
        MotorWriter(frequency=3, speed=0.6) as motor_writer, \
        KerasPipe(filename="./model.h5", verbose=True) as keras_pipe, \
        ResizePipe(size=(64, 48), grayscale=True) as resize_pipe:
            while True:
                try:
                    frame = cam.read()
                    frame = resize_pipe.pipe(frame)
                    keys = keras_pipe.pipe(frame)
                    print(keys)
                    motor_writer.write(keys)      
                    time.sleep(0.1)
                except KeyboardInterrupt:
                    break

if __name__ == '__main__':
    main()
