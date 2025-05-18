from utility.product import Product
from utility.shelf import Shelf
from views.visualizer import Visualizer

VOXEL_SIZE = 0.1

def create_shelf() -> Shelf:

    shelf_dimensions = (5.0, 0.5, 0.5)
    access_cost = 10.0
    additional_cost = 2.0

    if not all((dim / VOXEL_SIZE).is_integer() for dim in shelf_dimensions):
        print("Warning: - Shelf dimensions not perfectly divisable by voxel size")

    return Shelf(
        shelf_id="A1-L1",
        dimensions=shelf_dimensions,
        access_cost=access_cost,
        voxel_size=VOXEL_SIZE,
        operational_cost=additional_cost
    )

def create_products() -> list[Product]:

    return [
        Product("PR01", 0.5, (1.3, 0.2, 0.2), 100, voxel_size=VOXEL_SIZE),
        Product("PR02", 1.0, (0.5, 0.4, 0.3), 80, voxel_size=VOXEL_SIZE),
        Product("PR03", 0.8, (0.8, 0.1, 0.1), 50, voxel_size=VOXEL_SIZE),
        Product("PR04", 1.2, (1.4, 0.4, 0.4), 70, voxel_size=VOXEL_SIZE),
        Product("PR05", 1.0, (0.5, 0.4, 0.3), 80, voxel_size=VOXEL_SIZE),
        Product("PR06", 0.8, (0.8, 0.1, 0.1), 50, voxel_size=VOXEL_SIZE),
        Product("PR07", 0.8, (0.8, 0.1, 0.1), 50, voxel_size=VOXEL_SIZE),
        Product("PR08", 0.8, (0.8, 0.1, 0.1), 50, voxel_size=VOXEL_SIZE),
        Product("PR09", 0.8, (0.8, 0.1, 0.1), 50, voxel_size=VOXEL_SIZE),
        Product("PR10", 0.8, (0.8, 0.1, 0.1), 50, voxel_size=VOXEL_SIZE)
    ]

def place_products(shelf: Shelf, products: list[Product]) -> list[tuple[Product, bool]]:

    placement_results: list[tuple[Product, bool]] = []

    shelf.reset()

    for i, product in enumerate(products):

        print(f"\nPlacing product {i+1}/{len(products)}: {product.product_id} (Dim: {product.dimensions})")

        can_fit = (product.dimensions[0] <= shelf.dimensions[0] and
                   product.dimensions[1] <= shelf.dimensions[1] and
                   product.dimensions[2] <= shelf.dimensions[2])
        
        if not can_fit:
            placement_results.append((product, False))

        was_placed = shelf.place_product(product)
        placement_results.append((product, was_placed))

        if was_placed:
            print(f"Successfully placed {product.product_id}")
        else:
            print(f"Could not place {product.product_id} - no available space found")

    return placement_results

def main() -> None:

    shelf = create_shelf()
    products = create_products()

    _ = place_products(shelf, products)

    if shelf.stored_products:
        for product in shelf.stored_products:
            print(f"""- {product.product_id}
                   at Voxel Position {product.position}
                   with Voxel Dims Used {tuple(int(round(d/shelf.voxel_size)) for d in product.orientation)}""")
    else:
        print("No products successfully placed.")

    shelf.visualize()
    Visualizer().plot_shelf(shelf, elev=60, azim=-60)

if __name__ == "__main__":
    main()