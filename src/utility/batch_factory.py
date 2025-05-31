from utility.product import Product

class Batch_Factory:
    
    def make_products(voxel_size: float) -> list[Product]:

        return [
            Product("PR01", 0.5, (1.3, 1.2, 0.2), 100, voxel_size=voxel_size),
            Product("PR02", 1.0, (0.5, 0.4, 0.3), 80, voxel_size=voxel_size),
            Product("PR03", 0.8, (0.8, 0.1, 0.1), 50, voxel_size=voxel_size),
            Product("PR04", 1.2, (1.4, 1.6, 0.5), 70, voxel_size=voxel_size),
            Product("PR05", 1.0, (0.5, 0.4, 0.3), 80, voxel_size=voxel_size),
            Product("PR06", 0.8, (0.8, 0.1, 0.1), 50, voxel_size=voxel_size),
            Product("PR07", 0.8, (0.8, 0.1, 0.1), 50, voxel_size=voxel_size),
            Product("PR08", 0.8, (0.8, 0.1, 0.1), 50, voxel_size=voxel_size),
            Product("PR09", 0.8, (0.8, 0.1, 0.1), 50, voxel_size=voxel_size),
            Product("PR10", 0.8, (0.8, 0.1, 0.1), 50, voxel_size=voxel_size)
        ]