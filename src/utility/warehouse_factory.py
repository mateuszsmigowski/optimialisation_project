from utility.shelf import Shelf
from utility.rack import Rack

class WarehouseFactory():
    
    def __init__(self, rack_count: int = 10, shelf_count: int = 4):
        
        self.rack_count = rack_count
        self.shelf_count = shelf_count
    
    def make_racks(self):

        racks: list[Rack] = []
        
        for i in range(0, self.rack_count):
            rack = self.__make_rack(rack_index=i)
            racks.append(rack)
        
        return racks
    
    def __make_rack(self, rack_index: int) -> Rack:
        
        rack = Rack(f"R{rack_index}")
        
        for i in range(0, self.shelf_count):
            shelf = self.__make_shelf(
                rack_index=rack_index,
                shelf_index=i,
                access_cost=(rack_index+1)*100,
                additional_cost=(i+1)*10
                )
            rack.add_shelf(shelf)
            
        return rack
            
    def __make_shelf(self, rack_index: int, shelf_index: int, access_cost: float, additional_cost: float) -> Shelf:

        return Shelf(
            shelf_id=f"R{rack_index}-S{shelf_index}",
            access_cost=access_cost,
            operational_cost=additional_cost
        )