import numpy as np

class Product:
    
    def __init__(self,
                 product_id: str,
                 weight: float,
                 dimensions: tuple[float, float, float],
                 frequency: int,
                 voxel_size: float):

        from utility.shelf import Shelf

        self.product_id: str = product_id
        self.weight: float = weight
        self.dimensions: tuple[float, float, float] = dimensions
        self.frequency: int = frequency
        self.volume: float = dimensions[0] * dimensions[1] * dimensions[2]
        self.assigned_shelf: Shelf | None = None
        self.voxel_size = voxel_size
        self.voxel_dims: tuple[int, int, int] | None = None

        self.position: tuple[int, int, int] | None = None
        self.orientation: tuple[int, int, int] | None = None
    
    def __eq__(self, other: object) -> bool:

        if not isinstance(other, Product):
            return NotImplemented
        return self.product_id == other.product_id
    
    def __hash__(self) -> int:
        
        return hash(self.product_id)
    
    def __str__(self):
        
        return f"Product id: {self.product_id}"
    
    def dims_in_voxels(self) -> tuple[int, int, int]:

        return (
            int(np.ceil(self.dimensions[0] / self.voxel_size)),
            int(np.ceil(self.dimensions[1] / self.voxel_size)),
            int(np.ceil(self.dimensions[2] / self.voxel_size))
        )
    
    def reset(self) -> None:

        self.assigned_shelf = None
        self.position = None
        self.orientation = None