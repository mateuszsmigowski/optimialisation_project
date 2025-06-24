from utility.product import Product
from utility.rack import Rack
from utility.shelf import Shelf
from optimization_algorithms.optimizer import Optimizer

class GreedyOptimizer(Optimizer):
    """
    Rozwiązuje problem rozmieszczenia za pomocą prostego algorytmu zachłannego.
    Działa na aktualnym stanie magazynu, umieszczając nową partię produktów.
    """
    
    def __init__(self):
        self._total_cost_for_batch = 0.0

    def solve(self, batch: list[Product], racks: list[Rack]):
        """
        Rozmieszcza produkty z partii na już częściowo zapełnionych półkach.
        
        Strategia:
        1. Posortuj nowe produkty według priorytetu (np. malejąca częstotliwość).
        2. Utwórz listę wszystkich dostępnych półek i posortuj je według kosztu (rosnąco).
        3. Dla każdego produktu z partii, przejdź przez posortowaną listę półek i 
           umieść go na pierwszej (najtańszej) półce, która ma wystarczająco 
           dużo wolnego miejsca.
        """
        self._total_cost_for_batch = 0.0
        
        sorted_products = sorted(batch, key=lambda p: p.frequency, reverse=True)
        
        all_shelves: list[Shelf] = [shelf for rack in racks for shelf in rack.shelves]
        
        sorted_shelves = sorted(all_shelves, key=lambda s: s.access_cost + s.operational_cost)
        
        unplaced_products_count = 0
        print(f"  > Starting Greedy Optimizer for new batch of {len(batch)} products.")

        for product in sorted_products:
            placed = False
            for shelf in sorted_shelves:
                
                if shelf.place_product(product):
                    
                    cost_for_product = product.frequency * (shelf.access_cost + shelf.operational_cost)
                    self._total_cost_for_batch += cost_for_product
                    placed = True
                    break
            
            if not placed:
                unplaced_products_count += 1

        print(f"  > Greedy Optimizer finished. Cost for this batch: {self.cost:.2f}")
        if unplaced_products_count > 0:
            print(f"  > Could not place {unplaced_products_count} products.")

    @property
    def cost(self) -> float:
        """Zwraca koszt poniesiony tylko dla ostatnio przetworzonej partii."""
        return self._total_cost_for_batch