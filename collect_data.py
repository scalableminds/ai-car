import time

from sensors import *
from writers import *
from pipes import *
import cv2


def main():
    with PiCameraSensor() as cam, \
         PiPipe() as pipe, \
         ControllerServer(port=8000) as controller, \
         VideoServer(port=8050) as video_server, \
         ImageDiskWriter(folder="collected_data") as img_disk_writer, \
         CSVDiskWriter(filename="collected_data/classes.csv") as csv_disk_writer:
            while True:
                try:
                    frame = cam.read()
                    frame = pipe.pipe(frame)
                    keys = controller.read()
                    video_server.write(frame)
                    # img_disk_writer.write(frame)
                    # csv_disk_writer.write(keys)
                    print(keys)
                    time.sleep(0.1)
                except KeyboardInterrupt:
                    break

if __name__ == '__main__':
   # main()
    with PiPipe() as pipe, \
         CoPilot() as pilot:

        for i in range(4):
            img = cv2.imread("test/%d.jpg" % i, cv2.IMREAD_COLOR)
            res = pipe.pipe(img)
            print(pilot.pipe(res, 20))

    while True:
        cv2.waitKey(100)
