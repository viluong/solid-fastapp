from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    def get(self, id: int):
        pass

    @abstractmethod
    def create(self, schema):
        pass