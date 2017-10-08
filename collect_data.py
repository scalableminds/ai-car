import time

from handlers import *
from server import Server
from sensors import *
from writers import *
from pipes.resize_pipe import ResizePipe
from datetime import datetime
import os

def main():
    vid_handler = VideoHandler()
    key_handler = KeyHandler()
    file_handler = FileHandler("index.html")
    timestamp_str = str(datetime.now()).replace(" ", "_")
    log_folder = "collected_data_" + timestamp_str

    os.mkdir(log_folder)

    with PiCameraSensor(resolution=(64, 48)) as cam, \
        Server(handlers={
            "/": file_handler,
            "/video": vid_handler,
            "/socket": key_handler 
        }, port=8080) as server, \
        ImageDiskWriter(folder=log_folder) as img_disk_writer, \
        MotorWriter() as motor_writer, \
        ResizePipe(size=(64, 48), grayscale=True) as resize_pipe, \
        CSVDiskWriter(filename="%s/classes.csv" % log_folder) as csv_disk_writer:
            while True:
                try:
                    frame = cam.read()
                    frame = resize_pipe.pipe(frame)
                    keys = key_handler.read()     
                    motor_writer.write(keys)               
                    img_disk_writer.write(frame)
                    csv_disk_writer.write(keys)
                    # print(keys)
                    vid_handler.write(frame)
                    time.sleep(0.1)
                except KeyboardInterrupt:
                    break

if __name__ == '__main__':
    main()
