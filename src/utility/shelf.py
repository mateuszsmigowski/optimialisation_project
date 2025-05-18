import numpy as np
from utility.product import Product

class Shelf:

    ## - Initialization
    def __init__(self, 
                 shelf_id: str,
                 dimensions: tuple[float, float, float],
                 voxel_size: float,
                 access_cost: float, operational_cost: float = 0.0
                 ):

        self.shelf_id: str = shelf_id
        self.dimensions: tuple[float, float, float] = dimensions
        self.voxel_size: float = voxel_size
        self.stored_products: list[Product] = []
        self.grid_dimension: tuple[int, int, int] = (
            int(dimensions[0] // voxel_size),
            int(dimensions[1] // voxel_size),
            int(dimensions[2] // voxel_size)
        )
        self.total_voxels: int = self.grid_dimension[0] * self.grid_dimension[1] * self.grid_dimension[2]
        self.total_volume: float = self.total_voxels * (voxel_size ** 3)
        self.voxel_grid: np.ndarray = np.zeros(self.grid_dimension, dtype=np.int8)
        self.occupied_voxels_count: int = 0

        self.access_cost: float = access_cost
        self.operational_cost: float = operational_cost

    ## - Protocols
    def __eq__(self, value: object) -> bool:
        
        if not isinstance(value, Shelf):
            return NotImplemented
        return self.shelf_id == value.shelf_id
    
    def __hash__(self):
        
        return hash(self.shelf_id)

    ## - Methods
    def find_placement_position(self, product_voxel_dims: tuple[int, int, int]) -> tuple[int, int, int] | None:

        px, py, pz = product_voxel_dims
        gx, gy, gz = self.grid_dimension

        for z in range(gz - pz + 1):
            for y in range(gy - py + 1):
                for x in range(gx - px + 1):

                    is_space_free = True

                    if np.any(self.voxel_grid[x:x+px, y:y+py, z:z+pz] != 0):
                        is_space_free = False

                    if is_space_free:
                        return (x, y, z)
        
        return None
    
    def place_product(self, product: Product) -> bool:

        product_voxel_dims = product.dims_in_voxels()
        current_orientation_dims = product_voxel_dims

        placement_position = self.find_placement_position(current_orientation_dims)

        if placement_position:

            x, y, z = placement_position
            px, py, pz = current_orientation_dims
            self.voxel_grid[x:x+px, y:y+py, z:z+pz] = 1

            self.stored_products.append(product)
            self.occupied_voxels_count = np.sum(self.voxel_grid)

            product.assigned_shelf = self
            product.position = placement_position
            product.orientation = tuple(dim * self.voxel_size for dim in current_orientation_dims)

            return True
        
        return False
    
    def remove_product(self, product: Product) -> bool:

        if product not in self.stored_products or product.position is None or product.orientation is None:

            return False
        
        x, y, z = product.position
        ox, oy, oz = (
            int(round(product.orientation[0] / self.voxel_size)),
            int(round(product.orientation[1] / self.voxel_size)),
            int(round(product.orientation[2] / self.voxel_size))
        )

        self.voxel_grid[x:x+ox, y:y+oy, z:z+oz] = 0

        self.stored_products.remove(product)
        self.occupied_voxels_count = np.sum(self.voxel_grid)

        product.reset()

        return True
    
    def reset(self) -> None:

        for product in self.stored_products:
            product.reset()

        self.stored_products = []
        self.voxel_grid.fill(0)
        self.occupied_voxels_count = 0

    def visualize(self) -> None:
        
        if self.grid_dimension[2] > 0:

            print(f"Shelf: {self.shelf_id}, Voxel Grid ({self.grid_dimension})")
            print("Bottom Layer (z = 0):")

            slice_2d = self.voxel_grid[:, :, 0]
            print(slice_2d)

            print(f"Occupied Voxels: {self.occupied_voxels_count} / {self.total_voxels}")
            
        else:
            print(f"Shelf: {self.shelf_id} has zero height grid.")
