from utility.product import Product
from utility.shelf import Shelf
from views.visualizer import Visualizer
from utility.warehouse_factory import Warehouse_Factory
from utility.batch_factory import Batch_Factory

def main() -> None:

    racks = Warehouse_Factory().make_racks()
    products = Batch_Factory().make_products()
    
    [print(rack) for rack in racks]
    [[print(shelf) for shelf in rack.shelves] for rack in racks]

    # if shelf.stored_products:
    #     for product in shelf.stored_products:
    #         print(f"""- {product.product_id}
    #                at Voxel Position {product.position}
    #                with Voxel Dims Used {tuple(int(round(d/shelf.voxel_size)) for d in product.orientation)}""")
    # else:
    #     print("No products successfully placed.")

    # shelf.visualize()
    # Visualizer().plot_shelf(shelf, elev=60, azim=-60)

if __name__ == "__main__":
    main()