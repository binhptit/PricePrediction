from abc import ABC, abstractmethod

class BaseProfitLoss(ABC):
    def __init__(self) -> None:
        super().__init__()
        pass

    def run(self):
        pass