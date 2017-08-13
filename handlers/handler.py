from abc import ABC, abstractmethod
import asyncio

class Handler(ABC):
    @abstractmethod
    @asyncio.coroutine
    def handle(self, request):
        pass
     
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exit_type, value, traceback):
        pass
