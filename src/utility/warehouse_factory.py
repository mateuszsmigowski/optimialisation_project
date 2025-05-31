from utility.shelf import Shelf
from utility.rack import Rack

class Warehouse_Factory():
    
    def __init__(self):
        pass
    
    def make_racks(self):

        racks: list[Rack] = []
        
        for i in range(0,2):
            rack = self.__make_rack(rack_index=i)
            racks.append(rack)
        
        return racks
    
    def __make_rack(self, rack_index: int) -> Rack:
        
        rack = Rack(f"R{rack_index}")
        
        for i in range(0,6):
            shelf = self.__make_shelf(
                rack_index=rack_index,
                shelf_index=i,
                access_cost=rack_index,
                additional_cost=i
                )
            rack.add_shelf(shelf)
            
        return rack
            
    def __make_shelf(self, rack_index: int, shelf_index: int, access_cost: float, additional_cost: float) -> Shelf:

        return Shelf(
            shelf_id=f"R{rack_index}-S{shelf_index}",
            access_cost=access_cost,
            operational_cost=additional_cost
        )