import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, pi
from functools import reduce
from matplotlib import patches
from shapely.geometry import Polygon
from shapely.geometry import Point


def polar_to_rectangular(sample_function: [float], sample_points: [float]) -> [(float, float)]:
    assert len(sample_points) == len(sample_function)
    return [
        (r * cos(theta), r * sin(theta))
        for r, theta in zip(sample_function, sample_points)
    ]


def translation(original_points: [(float, float)], translation_vector: (float, float)) -> [(float, float)]:
    return [(x + translation_vector[0], y + translation_vector[1]) for x, y in original_points]


def rotate(polygon_points: [(float, float)], rotation_angle: float) -> [(float, float)]:
    return [
        (x * cos(rotation_angle) + y * sin(rotation_angle), -x * sin(rotation_angle) + y * cos(rotation_angle))
        for x, y in polygon_points
    ]


def generate_polygon(sample_function, sample_points, rotation_angle=0.0, translation_vector=(0.0, 0.0), update=None,
                     **kwargs):
    default_options = {
        'edgecolor': 'blue',
        'facecolor': None,
        'fill': False,
        'linewidth': 0.5
    }
    polygon_points = polar_to_rectangular(sample_function, sample_points)
    polygon_points = rotate(polygon_points, rotation_angle)
    polygon_points = translation(polygon_points, translation_vector)
    default_options.update(kwargs)
    if update is None:
        return patches.Polygon(np.array(polygon_points), closed=True, **default_options)
    else:
        update.set_xy(np.array(polygon_points))
        return update


def gear_system(sample_functions, sample_points, rotation_angles=(0.0,), gear_positions=((0.0, 0.0),), update=None):
    assert len(sample_functions) == len(sample_points) and len(sample_points) == len(rotation_angles) \
           and len(rotation_angles) == len(gear_positions)
    patches_collection = []
    if update is None:
        for function, points, theta, trans in zip(sample_functions, sample_points, rotation_angles, gear_positions):
            polygon = generate_polygon(function, points, theta, trans)
            patches_collection.append(polygon)
    else:
        assert len(update) == len(sample_functions)
        for function, points, theta, trans, patch in zip(sample_functions, sample_points, rotation_angles,
                                                         gear_positions, update):
            polygon = generate_polygon(function, points, theta, trans, patch)
            patches_collection.append(polygon)
    return patches_collection


def sync_rotation(phi_functions, drive_rotation):
    assert len(phi_functions)
    assert reduce(lambda x, y: len(x) == len(y), phi_functions)
    rotation_angles = [drive_rotation]
    xp = np.linspace(0, 2 * pi, len(phi_functions[0]), endpoint=False)
    for phi in phi_functions:
        angle = np.interp(drive_rotation, xp, phi)
        rotation_angles.append(angle)
    return tuple(rotation_angles)


def plot_frame(subplot, sample_functions: ([float],), range_start: float, range_end: float, phi_functions: [[float]],
               drive_rotation: float, gear_positions=((0.0, 0.0),), save=None):
    if sample_functions == ():
        return
    assert reduce(lambda x, y: len(x) == len(y), sample_functions)
    assert len(phi_functions) == len(sample_functions) - 1
    sample_points = np.linspace(range_start, range_end, len(sample_functions[0]), endpoint=False)
    sample_points = [sample_points] * len(sample_functions)
    for patch in gear_system(sample_functions, sample_points, sync_rotation(phi_functions, drive_rotation),
                             gear_positions):
        subplot.add_patch(patch)
    plt.draw()
    if save is not None:
        # WARNING: saving to png will cause the animation to be not smooth (due to IO and image processing)
        plt.savefig(f'{save}.png')


def plot_sampled_function(sample_functions, phi_functions, filename_prefix, frames, frame_pause, gear_positions,
                          figure_size, canvas_limit, angle_range=(0, 2 * pi)):
    fig, subplot = plt.subplots(figsize=figure_size)
    plt.ion()
    xlim, ylim = canvas_limit
    range_start, range_end = angle_range
    frame_count = 0
    for drive_rotation in np.linspace(range_start, range_end, frames, False):
        subplot.clear()
        subplot.set_xlim(xlim)
        subplot.set_ylim(ylim)
        subplot.axis('off')
        frame_count = frame_count + 1
        if filename_prefix is None:
            plot_frame(subplot, sample_functions, range_start, range_end, phi_functions, drive_rotation, gear_positions)
        else:
            plot_frame(subplot, sample_functions, range_start, range_end, phi_functions, drive_rotation, gear_positions,
                       '%s-%05d' % (filename_prefix, frame_count))
        plt.pause(frame_pause)
    plt.ioff()
    plt.close(fig)


if __name__ == '__main__':
    from compute_dual_gear import compute_dual_gear
    from drive_gears.ellipse_gear import generate_gear

    drive_gear = generate_gear(8192)

    driven_gear, center_distance, phi = compute_dual_gear(drive_gear, 1)
    phi = [value - pi for value in phi]
    plot_sampled_function((drive_gear, driven_gear), (phi,), None, 100, 0.001, [(0, 0), (center_distance, 0)],
                          (8, 8), ((-300, 700), (-500, 500)))
