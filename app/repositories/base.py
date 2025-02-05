from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    async def get(self, id: int):
        pass

    @abstractmethod
    async def create(self, schema):
        pass
