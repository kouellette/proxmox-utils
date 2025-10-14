from abc import ABC, abstractmethod


class UtilInterface(ABC):
    @staticmethod
    @abstractmethod
    def add_arguments(sub_parsers):
        pass

    @abstractmethod
    async def exec(self):
        pass
