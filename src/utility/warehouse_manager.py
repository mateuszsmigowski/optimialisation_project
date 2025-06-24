import random
from utility.product import Product
from utility.rack import Rack
from utility.shelf import Shelf
from optimization_algorithms.optimizer import Optimizer

class WarehouseManager:
    
    def __init__(self, racks: list[Rack]):
        self.racks: list[Rack] = racks
        self.total_cost_incurred = 0.0

    def start_simulation(self, algorithm: Optimizer, batches: list[list[Product]]):
        """Uruchamia pełną symulację na podstawie pre-generowanych partii."""
        num_epochs = len(batches)
        print(f"--- Starting Warehouse Simulation for {num_epochs} epochs using {algorithm.__class__.__name__} ---")
        
        for epoch, new_batch in enumerate(batches, 1):
            print(f"\n===== EPOCH {epoch}/{num_epochs} =====")
            
            # 1. Faza usuwania produktów
            self._remove_departing_products()
            
            # 2. Faza dostawy nowych produktów (już dostarczona w argumencie)
            print(f"Processing pre-generated batch {epoch} with {len(new_batch)} products.")

            # 3. Faza optymalizacji i umieszczania
            if new_batch:
                algorithm.solve(batch=new_batch, racks=self.racks)
                self.total_cost_incurred += algorithm.cost
            
            # 4. Statystyki po epoce
            self.print_epoch_summary()

        print("\n--- Simulation Finished ---")
        print(f"Total cumulative cost for {algorithm.__class__.__name__}: {self.total_cost_incurred:.2f}")

    def _remove_departing_products(self, base_removal_chance: float = 0.1):
        """
        Usuwa produkty z magazynu na podstawie ich częstotliwości.
        Produkty o wyższej częstotliwości mają większą szansę na usunięcie.
        """
        products_to_remove = []
        all_stored_products = [prod for rack in self.racks for shelf in rack.shelves for prod in shelf.stored_products]
        
        if not all_stored_products:
            print("Warehouse is empty. No products to remove.")
            return

        max_freq = max(p.frequency for p in all_stored_products) if all_stored_products else 1
        
        for product in all_stored_products:
            removal_probability = base_removal_chance + (product.frequency / max_freq) * 0.5
            if random.random() < removal_probability:
                products_to_remove.append(product)
        
        print(f"Attempting to remove {len(products_to_remove)} products...")
        count = 0
        for product in products_to_remove:
            if product.assigned_shelf:
                product.assigned_shelf.remove_product(product)
                count += 1
        print(f"Successfully removed {count} products.")

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