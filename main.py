import time
import cv2

from sensors import *
from writers import *

def main(write_to_disk, enable_video, use_nn, init_phase_duration, main_framerate, sleep_time):
    init_phase = init_phase_duration

    with PiCameraSensor(internal_framerate=main_framerate) as cam, \
         (NNSensor() if use_nn else ControllerServer(port=8000)) as controller, \
         vid_w as video_server, \
         MotorWriter() as motor_writer, \
         (ImageDiskWriter(folder="collected_data/upper") if write_to_disk \
         else EmptyWriter()) as img_disk_writer, \
         (ImageDiskWriter(folder ="collected_data/lower") if write_to_disk \
         else EmptyWriter()) as img_disk_writer_lower, \
         (CSVDiskWriter(filename="./classes.csv") \
         if write_to_disk else EmptyWriter()) as csv_disk_writer:

        while True:
            try:
                frame = cam.read()
                frame = cv2.resize(frame, (100,100))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                upper = frame[:50,:]
                lower = frame[50:,:]
                
                if use_nn:
                    keys = controller.read(lower)
                else:
                    keys = controller.read()
                
                video_server.write(frame)
                img_disk_writer.write(upper)
                img_disk_writer_lower.write(lower)      
                csv_disk_writer.write(keys)

                if use_nn and init_phase>0:
                    motor_writer.write(set(["UP"]))
                    init_phase -= sleep_time
                else:
                    motor_writer.write(keys)

                time.sleep(sleep_time)
            except KeyboardInterrupt:
                break

if __name__ == '__main__':
    print("Do you want to write collected data to disk? (y/n)")
    write_to_disk = input() == 'y'
    print("Do you want to enable the video server? (y/n)")
    enable_video = input() == 'y'
    print("NN or manual control (n/m)?")
    use_nn = input() =='n'

    vid_w = VideoServer(port=8050) if enable_video else EmptyWriter()

    init_phase_duration = 3 # in sek
    main_framerate = 5
    sleep_time = 0.08
    main(write_to_disk, enable_video, use_nn, init_phase_duration, main_framerate, sleep_time)
