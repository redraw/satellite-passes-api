import math


def az_to_octant(azimuth):
    octants = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    idx = azimuth / (2*math.pi/8)
    return octants[round(idx) % 8]
