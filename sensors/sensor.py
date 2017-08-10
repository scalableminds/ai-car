from abc import ABC, abstractmethod


class Sensor(ABC):
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exit_type, value, traceback):
        pass
