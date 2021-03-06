from matplotlib.lines import Line2D
from drive_gears.shape_processor import toCartesianCoordAsNp
import matplotlib.pyplot as plt
import numpy as np
from plot.qt_plot import Plotter


# set up the plotting window
def init_plot():
    fig, plts = plt.subplots(3, 3)
    fig.set_size_inches(16, 9)
    plt.ion()
    plt.show()
    return fig, plts


def plot_cartesian_shape(ax, title, contour, face_color=None, edge_color=None):
    ax.set_title(title)
    ax.fill(contour[:, 0], contour[:, 1], "g", facecolor='lightsalmon' if face_color is None else face_color,
            edgecolor='orangered' if edge_color is None else edge_color, linewidth=3, alpha=0.3)
    ax.axis('equal')


def plot_polar_shape(ax, title, polar_contour, center, sample_num):
    cartesian_contour = toCartesianCoordAsNp(polar_contour, center[0], center[1])
    ax.set_title(title)
    ax.fill(cartesian_contour[:, 0], cartesian_contour[:, 1], "g", alpha=0.3)
    for p in cartesian_contour[1:-1: int(len(cartesian_contour) / 32)]:
        l = Line2D([center[0], p[0]], [center[1], p[1]], linewidth=1)
        ax.add_line(l)
    ax.scatter(center[0], center[1], s=10, c='b')
    ax.axis('equal')


def plot_contour_and_save(plotter: Plotter, contour: np.ndarray, file_path: str, face_color=None, edge_color=None,
                          center=None):
    raise

