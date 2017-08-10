import time

from sensors import *
from writers import *


def main():
    with PiCameraSensor() as cam, \
         ControllerServer(port=8000) as controller, \
         VideoServer(port=8050) as video_server, \
         ImageDiskWriter(folder="collected_data") as img_disk_writer, \
         CSVDiskWriter(filename="collected_data/classes.csv") as csv_disk_writer:
            while True:
                try:
                    frame = cam.read()
                    keys = controller.read()
                    video_server.write(frame)
                    # img_disk_writer.write(frame)
                    # csv_disk_writer.write(keys)
                    print(keys)
                    time.sleep(0.1)
                except KeyboardInterrupt:
                    break

if __name__ == '__main__':
    main()
