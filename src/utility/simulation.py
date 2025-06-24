# utility/simulation_scenario.py

import random
from utility.batch_factory import BatchFactory
from utility.product import Product

class SimulationScenario:
    """
    Klasa odpowiedzialna za przygotowanie w pełni deterministycznego scenariusza
    symulacji, włączając w to partie przychodzące i listy produktów do usunięcia.
    """
    def __init__(self,
                 batch_factory: BatchFactory,
                 num_epochs: int,
                 products_per_epoch: int,
                 base_removal_chance: float = 0.1):
                 
        self.batch_factory = batch_factory
        self.num_epochs = num_epochs
        self.products_per_epoch = products_per_epoch
        self.base_removal_chance = base_removal_chance

    def generate(self) -> tuple[list[list[Product]], list[list[str]]]:
        """
        Generuje scenariusz: listę partii i listę decyzji o usunięciu.

        Returns:
            tuple: 
                - Lista partii (list of list of Product)
                - Lista list ID produktów do usunięcia w każdej epoce.
        """
        print("--- Generating deterministic simulation scenario... ---")
        
        # 1. Wygeneruj wszystkie przychodzące partie z góry
        batches = [
            self.batch_factory.create_batch(i + 1, self.products_per_epoch)
            for i in range(self.num_epochs)
        ]

        # 2. Przeprowadź symulację "w pamięci", aby podjąć decyzje o usunięciu
        removal_decisions: list[list[str]] = []
        simulated_storage: list[Product] = []

        for i in range(self.num_epochs):
            # Faza usuwania dla bieżącej epoki
            products_to_remove_this_epoch = []
            if simulated_storage:
                max_freq = max(p.frequency for p in simulated_storage) if simulated_storage else 1
                for product in simulated_storage:
                    removal_probability = self.base_removal_chance + (product.frequency / max_freq) * 0.5
                    if random.random() < removal_probability:
                        products_to_remove_this_epoch.append(product)
            
            # Zapisz ID produktów do usunięcia
            removal_decisions.append([p.product_id for p in products_to_remove_this_epoch])
            
            # Zaktualizuj stan symulowanego magazynu
            # Usuń produkty
            ids_to_remove = set(p.product_id for p in products_to_remove_this_epoch)
            simulated_storage = [p for p in simulated_storage if p.product_id not in ids_to_remove]
            
            # Dodaj nowe produkty
            simulated_storage.extend(batches[i])
        
        print("--- Scenario generation complete. ---")
        return batches, removal_decisions