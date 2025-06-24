import abc
from utility.product import Product
from utility.rack import Rack

class Optimizer(abc.ABC):
    
    @abc.abstractmethod
    def solve(self, batch: list[Product], racks: list[Rack]) -> list[Product]:
        # TODO: - Here should be implementet given algorithm
        pass
    
    @property
    @abc.abstractmethod
    def cost(self) -> float:
        # TODO: - This property should inform about iteration cost
        pass