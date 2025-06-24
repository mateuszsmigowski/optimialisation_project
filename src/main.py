import time

from utility.shelf import Shelf
from utility.warehouse_factory import WarehouseFactory
from utility.warehouse_manager import WarehouseManager
from utility.batch_factory import BatchFactory
from utility.simulation import SimulationScenario

from views.visualizer_warehouse import Visualizer

from optimization_algorithms.greedy import GreedyOptimizer
from optimization_algorithms.genetic import GeneticOptimizer
from optimization_algorithms.ant import AntColonyOptimizer

def run_and_report(algorithm, racks, batches, removals, visualizer, run_name: str):
    
    print(f"\n{'='*20} RUNNING SIMULATION FOR: {run_name.upper()} {'='*20}")
    
    manager = WarehouseManager(racks=racks)
    
    start_time = time.perf_counter()
    manager.start_simulation(algorithm=algorithm, batches=batches, removal_decisions=removals)
    end_time = time.perf_counter()
    
    print(f"--- {run_name.upper()} finished in {end_time - start_time:.2f} seconds ---")
    visualizer.plot_warehouse_state(racks, run_name)
    
    return manager.total_cost_incurred

def main() -> None:

    # 1. Konfiguracja symulacji
    NUM_EPOCHS = 5
    PRODUCTS_PER_EPOCH = 25

    # 2. Inicjalizacja komponentów
    voxel_size = Shelf.voxel_size
    warehouse_factory = WarehouseFactory() 
    batch_factory = BatchFactory(voxel_size=voxel_size)
    
    # 3. Wygeneruj jeden, spójny scenariusz dla wszystkich algorytmów
    scenario_generator = SimulationScenario(
        batch_factory=batch_factory,
        num_epochs=NUM_EPOCHS,
        products_per_epoch=PRODUCTS_PER_EPOCH
    )
    simulation_batches, removal_decisions = scenario_generator.generate()
    print("-------------------------------------------\n")

    genetic_optimizer = GeneticOptimizer(
        population_size=100, 
        generations=50,
        mutation_rate=0.05,
        crossover_rate=0.8
    )
    greedy_optimizer = GreedyOptimizer()
    aco_optimizer = AntColonyOptimizer(
        num_ants=10,
        generations=50,
        alpha=1.0,
        beta=2.0,
        evaporation_rate=0.5
    )

    visualizer = Visualizer()

    genetic_cost = run_and_report(
        genetic_optimizer, 
        warehouse_factory.make_racks(), 
        simulation_batches, 
        removal_decisions,
        visualizer, 
        "genetic"
    )
    
    greedy_cost = run_and_report(
        greedy_optimizer, 
        warehouse_factory.make_racks(), 
        simulation_batches, 
        removal_decisions,
        visualizer, 
        "greedy"
    )

    aco_cost = run_and_report(
        aco_optimizer, 
        warehouse_factory.make_racks(), 
        simulation_batches, 
        removal_decisions,
        visualizer, 
        "aco"
    )
    
    print("\n\n========== FINAL COMPARISON ==========")
    print(f"Genetic Algorithm Total Cost:   {genetic_cost:.2f}")
    print(f"Greedy Algorithm Total Cost:    {greedy_cost:.2f}")
    print(f"Ant Colony Optimizer Total Cost:{aco_cost:.2f}")
    print("======================================")

if __name__ == "__main__":
    main()