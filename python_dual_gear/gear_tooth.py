import math
import numpy as np

def teeth_straight(x: float, height: float, width: float):
    assert 0 <= x <= 1
    if x < width/7*2:
        y = height * (x / (width/7*2))
    elif x < width/7*5:
        y = height
    elif x < width:
        y = height * (width - x) / (width/7*2)
    else:
        y = 0.0
    return y-height/2

def teeth_sine(x: float, height: float, width: float):
    assert 0 <= x <= 1
    if x < width:
        return height * math.sin(x * 2 * math.pi)
    else:
        return 0

def teeth_involute(x: float, height: float, width: float):
    assert 0 <= x <= 1
    assert 0 < width < 1
    fake_height = height / (-(2/3-1)**2 + 1)
    if x < width/3:
        y = fake_height*(-(2/width*x-1)**2 + 1)
    elif x < width/3*2:
        y = height
    elif x < width:
        y = fake_height*(-(2/width*x-1)**2 + 1)
    else:
        y = 0
    return y-height/2

def teeth_involute_sin(x: float, height: float, width: float):
    assert 0 <= x <= 1
    assert 0 < width <= 1
    fake_height = height / math.sin(math.pi/3)
    if x < width/3:
        y = fake_height* math.sin(x/width * math.pi)
    elif x < width/3*2:
        y = height
    elif x < width:
        y = fake_height* math.sin(x/width * math.pi)
    else:
        y = 0
    return y-height/2


# return the average driving ratio of the given range
def sample_avg(start, end, polar_contour, center_dist):
    return np.average([d / (center_dist - d) for d in polar_contour[start:end]])


# return a value in [0,1] the map the teeth height
def get_value_on_tooth_domain(i : int, _tooth_samples):
    assert i < _tooth_samples[-1]
    idx = np.argmax(_tooth_samples > i)
    if idx == 0:
        value = i/_tooth_samples[0]
    else:
        value =  (i - _tooth_samples[idx-1])/ (_tooth_samples[idx] - _tooth_samples[idx-1])
    assert 0 <= value <= 1
    return value