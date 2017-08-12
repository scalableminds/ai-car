import time
import cv2

from sensors import *
from writers import *

print("Do you want to write collected data to disk? (y/n)")
write_to_disk = input() == 'y'
print("Do you want to enable the video server? (y/n)")
enable_video = input() == 'y'

vid_w = VideoServer(port=8050) if enable_video else EmptyWriter()

def main():
    with PiCameraSensor(internal_framerate=5) as cam, \
         ControllerServer(port=8000) as controller, \
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
                
                keys = controller.read()
                video_server.write(frame)
                img_disk_writer.write(upper)
                img_disk_writer_lower.write(lower)      
                csv_disk_writer.write(keys)
                motor_writer.write(keys)
                time.sleep(0.1)
            except KeyboardInterrupt:
                break

if __name__ == '__main__':
    main()
