# views/visualizer.py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import itertools
import numpy as np
import math # <-- Nowy import
from utility.shelf import Shelf
from utility.rack import Rack # <-- Nowy import

class Visualizer:
     
    def __init__(self):
        # Usunięto stąd self.fig i self.ax, będą tworzone na żądanie
        self._color_cycle = itertools.cycle(plt.cm.tab10.colors)
        self._product_color_map: dict[str, tuple[float, float, float]] = {}
        
    def _get_product_color(self, product_id: str) -> tuple[float, float, float]:
        if product_id not in self._product_color_map:
            self._product_color_map[product_id] = next(self._color_cycle)
        return self._product_color_map[product_id]
     
    def plot_shelf(self, shelf: Shelf, elev: float | None = None, azim: float | None = None) -> None:
        """
        Tworzy i wyświetla wykres dla JEDNEJ, konkretnej półki.
        """
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        self._draw_single_shelf_on_ax(ax, shelf)

        if elev is not None or azim is not None:
            ax.view_init(elev=elev, azim=azim)
            
        plt.show()
        self.close_plot()

    def plot_warehouse_state(self, racks: list[Rack], run_name: str) -> None:
        """
        Tworzy jeden zbiorczy obraz zawierający wizualizację wszystkich półek w magazynie.
        """
        all_shelves = [shelf for rack in racks for shelf in rack.shelves]
        if not all_shelves:
            return
            
        num_shelves = len(all_shelves)
        # Ustalenie siatki subplotów, np. 4 kolumny
        ncols = 4
        nrows = math.ceil(num_shelves / ncols)
        
        fig, axes = plt.subplots(
            nrows=nrows, 
            ncols=ncols, 
            figsize=(5 * ncols, 4 * nrows), 
            subplot_kw={'projection': '3d'}
        )
        
        # Ustawienie głównego tytułu dla całej figury
        fig.suptitle(f'Warehouse State after "{run_name.upper()}" run', fontsize=20, y=0.98)
        
        # axes.flat ułatwia iterację po siatce 2D jak po liście 1D
        for i, ax in enumerate(axes.flat):
            if i < num_shelves:
                shelf = all_shelves[i]
                self._draw_single_shelf_on_ax(ax, shelf)
            else:
                # Ukryj nieużywane subploty
                ax.set_visible(False)
        
        plt.tight_layout(rect=[0, 0, 1, 0.96]) # Dopasuj układ, zostawiając miejsce na suptitle
        
        output_filename = f"final_state_{run_name}_warehouse.png"
        fig.savefig(output_filename, bbox_inches='tight')
        print(f"  > Warehouse state visualization saved to: {output_filename}")
        plt.close(fig) # Zamknij figurę, aby zwolnić pamięć

    def _draw_single_shelf_on_ax(self, ax: plt.Axes, shelf: Shelf) -> None:
        """
        Prywatna metoda pomocnicza, która rysuje zawartość jednej półki na podanym obiekcie Axes.
        """
        # Resetowanie mapowania kolorów dla każdej nowej wizualizacji
        self._product_color_map = {}
        self._color_cycle = itertools.cycle(plt.cm.tab10.colors)

        ax.set_xlim([0, shelf.shelf_dimensions[0]])
        ax.set_ylim([0, shelf.shelf_dimensions[1]])
        ax.set_zlim([0, shelf.shelf_dimensions[2]])

        ax.set_xlabel('L', fontsize=8)
        ax.set_ylabel('W', fontsize=8)
        ax.set_zlabel('H', fontsize=8)
        ax.set_title(f'{shelf.shelf_id} ({shelf.get_products_count} prod.)', fontsize=10)
        ax.tick_params(axis='both', which='major', labelsize=6)

        # Rysowanie produktów
        for product in shelf.stored_products:
            if product.position is not None and product.orientation is not None:
                pos_physical = (product.position[0] * shelf.voxel_size,
                                product.position[1] * shelf.voxel_size,
                                product.position[2] * shelf.voxel_size)
                dims_physical = product.orientation
                color = self._get_product_color(product.product_id)
                self._plot_box_3d(ax, pos_physical, dims_physical, color=color, alpha=0.7)
        
        # Ustawienie proporcji, aby półki nie były zniekształcone
        max_range = max(shelf.shelf_dimensions)
        ax.set_box_aspect([
            shelf.shelf_dimensions[0] / max_range,
            shelf.shelf_dimensions[1] / max_range,
            shelf.shelf_dimensions[2] / max_range
        ])

    def _plot_box_3d(self, ax: plt.Axes, position: tuple[float, float, float], dimensions: tuple[float, float, float], **kwargs) -> Poly3DCollection:
        # ... (ta metoda pozostaje bez zmian) ...
        x, y, z = position
        dx, dy, dz = dimensions
        corners = np.array([[x,y,z], [x+dx,y,z], [x,y+dy,z], [x,y,z+dz], [x+dx,y+dy,z], [x+dx,y,z+dz], [x,y+dy,z+dz], [x+dx,y+dy,z+dz]])
        triangles = [[0,1,4],[0,4,2],[3,5,7],[3,7,6],[0,1,5],[0,5,3],[2,4,7],[2,7,6],[0,2,6],[0,6,3],[1,4,7],[1,7,5]]
        collection = Poly3DCollection([corners[tri] for tri in triangles], **kwargs)
        ax.add_collection3d(collection)
        return collection
    
    def close_plot(self) -> None:
        # Ta metoda nie jest już tak krytyczna, bo zamykamy figury po zapisaniu
        plt.close('all')