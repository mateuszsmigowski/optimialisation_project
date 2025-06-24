from utility.shelf import Shelf
from utility.product import Product

class Rack:
    
    def __init__(self, rack_id: str, max_shelves: int = 6):
        
        self.rack_id: str = rack_id
        self.max_shelves: int = max_shelves
        self.shelves: list[Shelf] = []
        
    def __getitem__(self, index: int) -> Shelf:
        return self.shelves[index]
    
    def __str__(self):
        return f"Rack id: {self.rack_id}"
        
    @property
    def get_products_count(self) -> int:
        return sum(shelf.get_products_count for shelf in self.shelves)
        
    def add_shelf(self, shelf: Shelf) -> bool:
        
        if len(self.shelves) < self.max_shelves:
            self.shelves.append(shelf)
            return True
        else:
            return False
        
    def get_shelf(self, index) -> Shelf | None:
        
        if 0 <= index < len(self.shelves):
            return self.shelves[index]
        else:
            return None
    
    def add_product(self, product: Product) -> bool:
        
        pass