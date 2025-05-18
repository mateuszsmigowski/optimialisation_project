import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import itertools
import numpy as np
from utility.shelf import Shelf

class Visualizer:
     
    def __init__(self):
    
        self.fig: plt.Figure | None = None
        self.ax: plt.Axes | None = None
        self._color_cycle = itertools.cycle(plt.cm.tab10.colors)
        self._product_color_map: dict[str, tuple[float, float, float]] = {}
        
    def _get_product_color(self, product_id: str) -> tuple[float, float, float]:
    
        if product_id not in self._product_color_map:
            self._product_color_map[product_id] = next(self._color_cycle)[:3]
                
        return self._product_color_map[product_id]
     
    def plot_shelf(self, shelf: Shelf, elev: float | None = None, azim: float | None = None, show=True) -> plt.Axes:
        
        if self.fig is None or self.ax is None:
            self.fig = plt.figure(figsize=(10, 8))
            self.ax = self.fig.add_subplot(111, projection='3d')
        else:
            self.ax.clear()
            self.ax.projection('3d')
        
        ax = self.ax
        
        ax.set_xlim([0, shelf.dimensions[0]])
        ax.set_ylim([0, shelf.dimensions[1]])
        ax.set_zlim([0, shelf.dimensions[2]])

        ax.set_xlabel('Length')
        ax.set_ylabel('Width')
        ax.set_zlabel('Height')
        ax.set_title(f'Shelf: {shelf.shelf_id}')
        
        x, y, z = shelf.dimensions
        points = [(0,0,0), (x,0,0), (0,y,0), (0,0,z), (x,y,0), (x,0,z), (0,y,z), (x,y,z)]
        edges = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 4), (2, 6), (3, 5), (3, 6), (4, 7), (5, 7), (6, 7)]
        for i, j in edges:
            p1 = points[i]
            p2 = points[j]
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 'k--')
            
        product_handles = []
        for product in shelf.stored_products:
            
            if product.position is not None and product.orientation is not None:
                
                pos_physical = (product.position[0] * shelf.voxel_size,
                                product.position[1] * shelf.voxel_size,
                                product.position[2] * shelf.voxel_size)

                dims_physical = product.orientation

                color = self._get_product_color(product.product_id)

                box_collection = self._plot_box_3d(ax, pos_physical, dims_physical, color=color, alpha=0.8, label=product.product_id)

        if shelf.stored_products:
            
            unique_products = list(dict.fromkeys(shelf.stored_products))
            handles = [plt.Line2D([0], [0], linestyle="none", marker="s", alpha=0.8, markersize=10, color=self._get_product_color(p.product_id), label=p.product_id) for p in unique_products]
            ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(1, 1))
            
        max_range = max(shelf.dimensions)
        ax.set_box_aspect([shelf.dimensions[0] / max_range,
                           shelf.dimensions[1] / max_range,
                           shelf.dimensions[2] / max_range])
        
        if elev is not None or azim is not None:
            
            ax.view_init(elev=elev, azim=azim)
            
        if show:
            
            plt.show()

        return ax
    
    def _plot_box_3d(self, ax: plt.Axes, position: tuple[float, float, float], dimensions: tuple[float, float, float], **kwargs) -> Poly3DCollection:

        x, y, z = position
        dx, dy, dz = dimensions

        corners = np.array([
            [x, y, z],
            [x + dx, y, z],
            [x, y + dy, z],
            [x, y, z + dz],
            [x + dx, y + dy, z],
            [x + dx, y, z + dz],
            [x, y + dy, z + dz],
            [x + dx, y + dy, z + dz],
        ])

        triangles = [
            [0, 1, 4], [0, 4, 2],  # Bottom face
            [3, 5, 7], [3, 7, 6],  # Top face
            [0, 1, 5], [0, 5, 3],  # Front face
            [2, 4, 7], [2, 7, 6],  # Back face
            [0, 2, 6], [0, 6, 3],  # Left face
            [1, 4, 7], [1, 7, 5],  # Right face
        ]

        collection = Poly3DCollection([corners[tri] for tri in triangles], **kwargs)
        ax.add_collection3d(collection)

        return collection
    
    def close_plot(self) -> None:
        
        if self.fig:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
            self._product_color_map = {}
            