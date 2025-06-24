import random
from utility.product import Product

class BatchFactory:
    """
    Klasa odpowiedzialna za generowanie dynamicznych partii produktów.
    """
    def __init__(self, voxel_size: float):
        self.voxel_size = voxel_size
        self._product_counter = 0

    def create_batch(self, batch_number: int, num_products: int) -> list[Product]:
        """
        Tworzy nową, losową partię produktów.
        
        Args:
            batch_number (int): Numer porządkowy partii (epoki).
            num_products (int): Liczba produktów do wygenerowania w tej partii.

        Returns:
            list[Product]: Lista nowo utworzonych produktów.
        """
        products = []
        for i in range(num_products):
            self._product_counter += 1
            product_id = f"B{batch_number}-P{self._product_counter}"
            
            dims = (
                round(random.uniform(0.1, 1.0), 2),
                round(random.uniform(0.1, 0.4), 2),
                round(random.uniform(0.1, 0.4), 2),
            )
            weight = round(random.uniform(0.2, 5.0), 2)
            frequency = random.choices(
                population=range(1, 101), 
                weights=[1/i for i in range(1, 101)],
                k=1
            )[0]

            products.append(
                Product(
                    product_id=product_id,
                    weight=weight,
                    dimensions=dims,
                    frequency=frequency,
                    voxel_size=self.voxel_size
                )
            )
        print(f"Created batch {batch_number} with {len(products)} new products.")
        return products