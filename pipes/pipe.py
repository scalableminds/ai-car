from abc import ABC, abstractmethod


class Pipe(ABC):
    @abstractmethod
    def pipe(self, data):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exit_type, value, traceback):
        pass
