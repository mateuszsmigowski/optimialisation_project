from utility.product import Product
from utility.rack import Rack
from optimization_algorithms.optimizer import Optimizer

class Warehouse_Manager:
    
    def __init__(self,
                 batches: list[list[Product]],
                 rack: list[Rack],
                 algorithm: Optimizer
                 ):
        
        self.batches: list[list[Product]] = batches
        self.racks: list[Rack] = rack
        self.algorithm: Optimizer = algorithm
        self.epochs_count: int = len(batches)
        self.storage: list[Product] = []
        
    def start(self):
        
        for batch in self.batches:
            self.algorithm.solve(batch=batch, racks=self.racks)
            
    def remove_products(self):
        
        pass
        
    def place_products(shelf: Shelf, products: list[Product]) -> list[tuple[Product, bool]]:

        placement_results: list[tuple[Product, bool]] = []

        shelf.reset()

        for i, product in enumerate(products):
            can_fit = (product.dimensions[0] <= shelf.dimensions[0] and
                    product.dimensions[1] <= shelf.dimensions[1] and
                    product.dimensions[2] <= shelf.dimensions[2])
            
            if not can_fit:
                placement_results.append((product, False))

            was_placed = shelf.place_product(product)
            placement_results.append((product, was_placed))

        return placement_results