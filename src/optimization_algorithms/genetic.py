import random
import copy
from utility.product import Product
from utility.rack import Rack
from utility.shelf import Shelf
from optimization_algorithms.optimizer import Optimizer

class GeneticOptimizer(Optimizer):

    def __init__(self, population_size=50, generations=100, mutation_rate=0.05, crossover_rate=0.8, tournament_size=3):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.tournament_size = tournament_size
        
        self._best_cost = float('inf')
        self.best_solution_ever = None

    def solve(self, batch: list[Product], racks: list[Rack]):
        """Główna metoda uruchamiająca ewolucję dla danej partii produktów."""

        self._best_cost = float('inf')
        self.best_solution_ever = None

        all_shelves = [shelf for rack in racks for shelf in rack.shelves]
        if not all_shelves:
            print("No shelves available for placement.")
            return

        num_products = len(batch)
        num_shelves = len(all_shelves)

        # 1. Inicjalizacja populacji
        population = self._initialize_population(num_products, num_shelves)

        print(f"  > Starting GA for new batch: {self.generations} generations, {self.population_size} population size.")

        for gen in range(self.generations):
            # 2. Ewaluacja populacji
            fitness_scores = [self._calculate_fitness(ind, batch, all_shelves) for ind in population]

            best_fitness_in_gen = max(fitness_scores)
            best_cost_in_gen = 1 / best_fitness_in_gen if best_fitness_in_gen > 0 else float('inf')

            if best_cost_in_gen < self._best_cost:
                self._best_cost = best_cost_in_gen
                best_individual_index = fitness_scores.index(best_fitness_in_gen)
                self.best_solution_ever = population[best_individual_index]
            
        # 5. Po zakończeniu ewolucji, zastosuj najlepsze znalezione rozwiązanie do PRAWDZIWYCH półek
        print(f"  > Evolution finished. Best cost for this batch: {self._best_cost:.2f}")
        unplaced_products: list[Product] = []
        if self.best_solution_ever:
            _cost, unplaced_products = self._evaluate_individual(
                self.best_solution_ever, batch, all_shelves, apply_placement=True
            )
            if unplaced_products:
                print(f"  > Could not place {len(unplaced_products)} products. They will be carried over.")
        else:
            print("  > No valid solution found for this batch. All products carried over.")
            unplaced_products = batch[:]

        return unplaced_products

    def _initialize_population(self, num_products: int, num_shelves: int) -> list[list[int]]:
        """Tworzy losową populację początkową."""
        population = []
        for _ in range(self.population_size):
            individual = [random.randint(0, num_shelves - 1) for _ in range(num_products)]
            population.append(individual)
        return population
    
    def _selection(self, population: list[list[int]], fitness_scores: list[float]) -> list[list[int]]:
        """Wybiera rodziców za pomocą selekcji turniejowej."""
        parents = []
        for _ in range(self.population_size):
            
            tournament_indices = random.sample(range(self.population_size), self.tournament_size)
            
            winner_index = max(tournament_indices, key=lambda i: fitness_scores[i])
            parents.append(population[winner_index])
            
        return parents

    def _crossover(self, parent1: list[int], parent2: list[int]) -> tuple[list[int], list[int]]:
        """Wykonuje krzyżowanie jednopunktowe."""
        if len(parent1) <= 1:
            return parent1[:], parent2[:]
            
        crossover_point = random.randint(1, len(parent1) - 1)
        
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        
        return child1, child2

    def _mutate(self, individual: list[int], num_shelves: int):
        """Losowo zmienia geny w chromosomie (przypisania do półek)."""
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                individual[i] = random.randint(0, num_shelves - 1)


    def _calculate_fitness(self, individual: list[int], batch: list[Product], original_shelves: list[Shelf]) -> float:
        """Oblicza wartość fitness dla danego osobnika (rozwiązania)."""
        cost, unplaced_list = self._evaluate_individual(individual, batch, original_shelves)
        unplaced_count = len(unplaced_list)
        penalty = unplaced_count * 1_000_000 
        total_cost = cost + penalty
        
        return 1.0 / (1.0 + total_cost)

    def _evaluate_individual(self, individual: list[int], batch: list[Product], original_shelves: list[Shelf], apply_placement: bool = False) -> tuple[float, list[Product]]:
        """
        Symuluje umieszczanie produktów i oblicza koszt.
        """
        
        if apply_placement:
            shelves_to_use = original_shelves
        else:
            shelves_to_use = copy.deepcopy(original_shelves)

        total_cost = 0.0
        unplaced_products_list: list[Product] = []

        sorted_indices = sorted(range(len(batch)), key=lambda i: batch[i].volume, reverse=True)

        for i in sorted_indices:
            product = batch[i]
            shelf_index = individual[i]
            shelf = shelves_to_use[shelf_index]

            if shelf.place_product(product):
                total_cost += product.frequency * (shelf.access_cost + shelf.operational_cost)
            else:
                unplaced_products_list.append(product)
        
        return total_cost, unplaced_products_list

    @property
    def cost(self) -> float:
        return self._best_cost