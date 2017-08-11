import time

from sensors import *
from writers import *


def main():
    with PiCameraSensor() as cam, \
         ControllerServer(port=8000) as controller, \
         VideoServer(port=8050) as video_server, \
         ImageDiskWriter(folder="collected_data") as img_disk_writer, \
         MotorWriter() as writer:
            while True:
                try:
                    frame = cam.read()
                    keys = controller.read()
                    video_server.write(frame)
<<<<<<< HEAD
                    #img_disk_writer.write(frame)
                    #csv_disk_writer.write(keys)
=======
                    # img_disk_writer.write(frame)
                    writer.write(keys)
>>>>>>> 9000c5834cf39d4a49cbee514957dd47ec10c2ff
                    print(keys)
                    time.sleep(0.1)
                except KeyboardInterrupt:
                    break

if __name__ == '__main__':
    main()
