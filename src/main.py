from utility.shelf import Shelf
from views.visualizer import Visualizer
from utility.warehouse_factory import WarehouseFactory
from utility.warehouse_manager import WarehouseManager
from utility.batch_factory import BatchFactory

from optimization_algorithms.greedy import GreedyOptimizer
from optimization_algorithms.genetic import GeneticOptimizer

def main() -> None:

    NUM_EPOCHS = 5
    PRODUCTS_PER_EPOCH = 8

    voxel_size = Shelf.voxel_size
    warehouse_factory = WarehouseFactory() 
    batch_factory = BatchFactory(voxel_size=voxel_size)
    
    print("--- Pre-generating batches for simulation ---")
    simulation_batches = [
        batch_factory.create_batch(batch_number=i+1, num_products=PRODUCTS_PER_EPOCH)
        for i in range(NUM_EPOCHS)
    ]
    print("-------------------------------------------\n")


    # =================================================================
    #                   SYMULACJA Z ALGORYTMEM GENETYCZNYM
    # =================================================================
    genetic_racks = warehouse_factory.make_racks()
    
    genetic_optimizer = GeneticOptimizer(
        population_size=100, 
        generations=50,
        mutation_rate=0.05,
        crossover_rate=0.8
    )

    genetic_manager = WarehouseManager(racks=genetic_racks)
    genetic_manager.start_simulation(algorithm=genetic_optimizer, batches=simulation_batches)


    # =================================================================
    #                   SYMULACJA Z ALGORYTMEM ZACHŁANNYM
    # =================================================================
    greedy_racks = warehouse_factory.make_racks()

    greedy_optimizer = GreedyOptimizer()
    
    greedy_manager = WarehouseManager(racks=greedy_racks)
    greedy_manager.start_simulation(algorithm=greedy_optimizer, batches=simulation_batches)
    

    # =================================================================
    #                           PODSUMOWANIE
    # =================================================================
    print("\n\n========== FINAL COMPARISON ==========")
    print(f"Genetic Algorithm Total Cost:   {genetic_manager.total_cost_incurred:.2f}")
    print(f"Greedy Algorithm Total Cost:    {greedy_manager.total_cost_incurred:.2f}")
    print("======================================")

if __name__ == "__main__":
    main()