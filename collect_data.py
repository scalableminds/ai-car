import time

from handlers import *
from server import Server
from sensors import *
from writers import *

def main():
    vid_handler = VideoHandler()
    key_handler = KeyHandler()
    file_handler = FileHandler("index.html")
    with Webcam() as cam, \
        Server(handlers={
            "/": file_handler,
            "/video": vid_handler,
            "/socket": key_handler 
        }, port=8080) as server, \
        ImageDiskWriter(folder="collected_data") as img_disk_writer, \
        CSVDiskWriter(filename="collected_data/classes.csv") as csv_disk_writer:
            while True:
                try:
                    frame = cam.read()
                    keys = key_handler.read()                    
                    # img_disk_writer.write(frame)
                    # csv_disk_writer.write(keys)
                    #print(keys)
                    vid_handler.write(frame)
                    time.sleep(0.1)
                except KeyboardInterrupt:
                    break

if __name__ == '__main__':
    main()
