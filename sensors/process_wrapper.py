import time
from multiprocessing import Process, Queue, Event

from sensors.sensor import Sensor


def _inner_read(inner, read_queue, stop_event):
    inner.__enter__()
    while not stop_event.is_set():
        buffer = inner.read()
        read_queue.put_nowait(buffer)
        time.sleep(0.1)
    inner.__exit__(None, None, None)

class ProcessWrapper(Sensor):
    def __init__(self, inner):
        self.inner = inner
        self.last_read = None
        self.queue = Queue()
        self.stop_event = Event()

    def __enter__(self):
        proc = Process(target=_inner_read, args=(self.inner, self.queue, self.stop_event))
        proc.start()
        return self

    def __exit__(self, exit_type, value, traceback):
        self.stop_event.set()

    def read(self):
        while not self.queue.empty():
            self.last_read = self.queue.get_nowait()
        return self.last_read
