import random
import copy
import numpy as np
from utility.product import Product
from utility.rack import Rack
from utility.shelf import Shelf
from optimization_algorithms.optimizer import Optimizer

class AntColonyOptimizer(Optimizer):
    """
    Rozwiązuje problem rozmieszczenia za pomocą algorytmu optymalizacji mrowiskowej (ACO).
    """

    def __init__(self, num_ants=10, generations=50, alpha=1.0, beta=2.0, evaporation_rate=0.5, q=100.0):
        """
        Args:
            num_ants (int): Liczba mrówek w każdej generacji.
            generations (int): Liczba iteracji algorytmu.
            alpha (float): Wpływ śladu feromonowego na decyzję mrówki.
            beta (float): Wpływ informacji heurystycznej (atrakcyjności) na decyzję.
            evaporation_rate (float): Współczynnik parowania feromonów (0 < rho < 1).
            q (float): Ilość feromonu zostawianego przez mrówki.
        """
        self.num_ants = num_ants
        self.generations = generations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.q = q

        self._best_cost = float('inf')
        self.best_solution_ever = None

    def solve(self, batch: list[Product], racks: list[Rack]):
        self._best_cost = float('inf')
        self.best_solution_ever = None

        all_shelves = [shelf for rack in racks for shelf in rack.shelves]
        num_products = len(batch)
        num_shelves = len(all_shelves)

        if not all_shelves or not batch:
            print("No shelves or products to process.")
            self._best_cost = 0
            return
            
        # 1. Inicjalizacja feromonów i heurystyk
        pheromones = np.ones((num_products, num_shelves))
        attractiveness = self._calculate_attractiveness(all_shelves)

        print(f"  > Starting ACO: {self.generations} generations, {self.num_ants} ants per generation.")

        for gen in range(self.generations):
            all_ant_solutions = []
            
            # 2. Każda mrówka buduje swoje rozwiązanie
            for ant in range(self.num_ants):
                temp_shelves = copy.deepcopy(all_shelves)
                
                solution = self._construct_solution_for_ant(batch, temp_shelves, pheromones, attractiveness)
                cost, unplaced = self._evaluate_solution(solution, batch, all_shelves)
                
                all_ant_solutions.append((solution, cost, unplaced))
            
            # 3. Aktualizacja feromonów
            self._update_pheromones(pheromones, all_ant_solutions)

            # Śledzenie najlepszego rozwiązania
            best_ant_in_gen = min(all_ant_solutions, key=lambda x: x[1] + x[2] * 1e9)
            if best_ant_in_gen[1] < self._best_cost and best_ant_in_gen[2] == 0:
                self._best_cost = best_ant_in_gen[1]
                self.best_solution_ever = best_ant_in_gen[0]
        
        # 4. Zastosuj najlepsze znalezione rozwiązanie
        print(f"  > ACO finished. Best cost for this batch: {self._best_cost:.2f}")
        unplaced_products: list[Product] = []
        if self.best_solution_ever:
            unplaced_products = self._apply_solution(self.best_solution_ever, batch, all_shelves)
            if unplaced_products:
                print(f"  > Could not place {len(unplaced_products)} products. They will be carried over.")
        else:
            print("  > No valid solution found for this batch. All products carried over.")
            unplaced_products = batch[:]

        return unplaced_products

    def _calculate_attractiveness(self, shelves: list[Shelf]) -> np.ndarray:
        """Oblicza heurystyczną atrakcyjność każdej półki (odwrotność kosztu)."""
        costs = np.array([s.access_cost + s.operational_cost for s in shelves])
        return 1.0 / (costs + 1e-10)

    def _construct_solution_for_ant(self, batch: list[Product], temp_shelves: list[Shelf], pheromones: np.ndarray, attractiveness: np.ndarray) -> list[int]:
        """Jedna mrówka konstruuje jedno kompletne rozwiązanie (przypisanie produktów do półek)."""
        solution = [-1] * len(batch)
        
        product_indices = sorted(range(len(batch)), key=lambda i: batch[i].volume, reverse=True)
        
        for prod_idx in product_indices:
            product = batch[prod_idx]
            
            shelf_probs = (pheromones[prod_idx] ** self.alpha) * (attractiveness ** self.beta)
            
            for shelf_idx, shelf in enumerate(temp_shelves):
                if not shelf.find_placement_position(product.dims_in_voxels()):
                    shelf_probs[shelf_idx] = 0
            
            sum_probs = np.sum(shelf_probs)
            if sum_probs > 0:
                shelf_probs /= sum_probs
            else:
                continue

            chosen_shelf_idx = np.random.choice(len(temp_shelves), p=shelf_probs)
            solution[prod_idx] = chosen_shelf_idx
            
            temp_shelves[chosen_shelf_idx].place_product(product)
            
        return solution

    def _update_pheromones(self, pheromones: np.ndarray, ant_solutions: list):
        """Aktualizuje macierz feromonów: parowanie i wzmacnianie."""
        
        pheromones *= (1 - self.evaporation_rate)

        for solution, cost, unplaced in ant_solutions:
            if unplaced > 0: continue

            pheromone_deposit = self.q / (cost + 1)
            
            for prod_idx, shelf_idx in enumerate(solution):
                if shelf_idx != -1:
                    pheromones[prod_idx][shelf_idx] += pheromone_deposit

    def _evaluate_solution(self, solution: list[int], batch: list[Product], original_shelves: list[Shelf]) -> tuple[float, int]:
        """Ocenia koszt danego rozwiązania bez modyfikowania stanu magazynu."""
        temp_shelves = copy.deepcopy(original_shelves)
        total_cost = 0.0
        unplaced_count = 0
        
        for prod_idx, shelf_idx in enumerate(solution):
            if shelf_idx == -1:
                unplaced_count += 1
                continue
                
            product = batch[prod_idx]
            shelf = temp_shelves[shelf_idx]
            
            if shelf.place_product(product):
                total_cost += product.frequency * (shelf.access_cost + shelf.operational_cost)
            else:
                unplaced_count += 1
                
        return total_cost, unplaced_count

    def _apply_solution(self, solution: list[int], batch: list[Product], shelves: list[Shelf]) -> list[Product]:
        """Finalnie umieszcza produkty i ZWRACA listę tych, które się nie zmieściły."""
        unplaced_products: list[Product] = []
        
        for prod_idx, shelf_idx in enumerate(solution):
            product = batch[prod_idx]
            if shelf_idx != -1:
                if not shelves[shelf_idx].place_product(product):
                    unplaced_products.append(product)
            else:
                unplaced_products.append(product)

        return unplaced_products

    @property
    def cost(self) -> float:
        return self._best_cost if self._best_cost != float('inf') else 0