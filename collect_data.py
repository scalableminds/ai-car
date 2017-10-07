import time

from handlers import *
from server import Server
from sensors import *
from writers import *
from pipes.resize_pipe import ResizePipe

def main():
    vid_handler = VideoHandler()
    key_handler = KeyHandler()
    file_handler = FileHandler("index.html")
    with PiCameraSensor(resolution=(64, 48)) as cam, \
        Server(handlers={
            "/": file_handler,
            "/video": vid_handler,
            "/socket": key_handler 
        }, port=8080) as server, \
        ImageDiskWriter(folder="collected_data") as img_disk_writer, \
        MotorWriter() as motor_writer, \
        ResizePipe(size=(64, 48), grayscale=Trte) as resize_pipe, \
        CSVDiskWriter(filename="collected_data/classes.csv") as csv_disk_writer:
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
