import random
from utility.product import Product
from utility.rack import Rack
from utility.shelf import Shelf
from optimization_algorithms.optimizer import Optimizer

class WarehouseManager:
    
    def __init__(self, racks: list[Rack]):
        self.racks: list[Rack] = racks
        self.total_cost_incurred = 0.0
        self.pending_products: list[Product] = []

    # Zmieniona sygnatura - przyjmuje teraz `removal_decisions`
    def start_simulation(self, algorithm: Optimizer, batches: list[list[Product]], removal_decisions: list[list[str]]):
        num_epochs = len(batches)
        print(f"--- Starting Warehouse Simulation for {num_epochs} epochs using {algorithm.__class__.__name__} ---")
        
        for epoch, new_batch in enumerate(batches, 1):
            print(f"\n===== EPOCH {epoch}/{num_epochs} =====")
            
            ids_to_remove = removal_decisions[epoch - 1]
            self._remove_departing_products(ids_to_remove)
            
            # Łączymy nowe produkty z tymi, które czekały w kolejce
            batch_to_process = self.pending_products + new_batch
            print(f"Processing batch of {len(batch_to_process)} products ({len(self.pending_products)} carried over, {len(new_batch)} new).")
            
            # Czyścimy kolejkę przed uruchomieniem algorytmu
            self.pending_products = []

            if batch_to_process:
                # Algorytm zwraca produkty, które się nie zmieściły
                unplaced = algorithm.solve(batch=batch_to_process, racks=self.racks)
                # Zapisujemy je do kolejki na następną epokę
                self.pending_products = unplaced
                
                self.total_cost_incurred += algorithm.cost
            
            self.print_epoch_summary()

        print("\n--- Simulation Finished ---")
        if self.pending_products:
            print(f"Warning: {len(self.pending_products)} products remained unplaced after the final epoch.")
        print(f"Total cumulative cost for {algorithm.__class__.__name__}: {self.total_cost_incurred:.2f}")

    # Metoda została całkowicie zmieniona
    def _remove_departing_products(self, products_to_remove_ids: list[str]):
        """
        Usuwa z magazynu produkty o podanych ID.
        """
        if not products_to_remove_ids:
            print("No products designated for removal in this epoch.")
            return

        print(f"Attempting to remove {len(products_to_remove_ids)} designated products...")
        
        # Stworzenie mapy dla szybkiego dostępu do produktów po ID
        product_map = {
            prod.product_id: prod
            for rack in self.racks 
            for shelf in rack.shelves 
            for prod in shelf.stored_products
        }
        
        count = 0
        for product_id in products_to_remove_ids:
            product_to_remove = product_map.get(product_id)
            if product_to_remove and product_to_remove.assigned_shelf:
                product_to_remove.assigned_shelf.remove_product(product_to_remove)
                count += 1
                
        print(f"Successfully removed {count} products.")
    
    # ... print_epoch_summary bez zmian ...
    def print_epoch_summary(self):
        """Wyświetla podsumowanie stanu magazynu."""
        total_products = 0
        total_occupied_voxels = 0
        total_voxels_capacity = 0

        for rack in self.racks:
            for shelf in rack.shelves:
                total_products += shelf.get_products_count
                total_occupied_voxels += shelf.occupied_voxels_count
                total_voxels_capacity += Shelf.total_voxels

        occupancy_percent = (total_occupied_voxels / total_voxels_capacity) * 100 if total_voxels_capacity > 0 else 0
        
        print("\n--- Epoch Summary ---")
        print(f"Total products in warehouse: {total_products}")
        print(f"Warehouse space occupancy: {occupancy_percent:.2f}%")
        print("--------------------")