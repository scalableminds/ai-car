from abc import ABC, abstractmethod


class Writer(ABC):
    @abstractmethod
    def write(self, data):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exit_type, value, traceback):
        pass
