import math
import numbers
import numpy

__author__      = "Carlos Granados"
__copyright__   = "Polivet.org"
__credits__     = ["Carlos Granados"]

__license__     = "PSL"
__version__     = "0.0.1"

"""
Mathematical functions for manipulating geospatial points
"""


def move_towards(point_1, point_2, distance):
    """
    :param point_1:
    :param point_2:
    :param distance:
    :return:
    """
    LAT  = 0
    LONG = 1
    EARTH_RADIUS = 6371000

    lat1 = math.radians(point_1[LAT])
    lng1 = math.radians(point_1[LONG])
    lat2 = math.radians(point_2[LAT])
    dLon = math.radians(point_2[LONG] - point_1[LONG])

    """
    Find the bearing from this point to the next.
    """
    bearing = math.atan2(
        math.sin(dLon) * math.cos(lat2),
        math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
    )

    angle_distance = distance / EARTH_RADIUS

    """
    Calculate the destination point, given the source and bearing.
    """
    lat2 = math.asin(
        math.sin(lat1) * math.cos(angle_distance) + math.cos(lat1) * math.sin(angle_distance) * math.cos(bearing)
    )

    lng2 = lng1 + math.atan2(
        math.sin(bearing) * math.sin(angle_distance) * math.cos(lat1),
        math.cos(angle_distance) - math.sin(lat1) * math.sin(lat2)
    )

    if lat2.real is False or lng2.real is False:
        return None

    return math.degrees(lat2), math.degrees(lng2)


def get_polyline_length(points):
    """
    :param points:
    :return:
    """
    out = 0

    for index in range(len(points)):
        """
        Get the distance from one point to another
        and add each result to get the total length
        """
        out += km_to(points[index], points[index+1])

        if (index + 1) == (len(points) - 1):
            break

    return out


def km_to(point_1, point_2):
    """
    :param point_1: tuple
    :param point_2: tuple
    :return:
    """
    LAT  = 0
    LONG = 1

    ra = math.pi/180
    b = point_1[LAT] * ra
    c = point_2[LAT] * ra
    d = b - c
    g = point_1[LONG] * ra - point_2[LONG] * ra
    f = 2 * math.asin(math.sqrt(math.pow(math.sin(d/2), 2) + math.cos(b) * math.cos(c) * math.pow(math.sin(g/2), 2)))

    return f * 6378.137


def move_along_path(points, distance, index=0):
    """
    :param points: tuple[]
    :param distance: In kilometers
    :param index: int
    :return:
    """

    if index < len(points) - 1:
        """
        There is still at least one point further from this point.
        Get the distance from this point to the next point
        """
        distanceToNextPoint = km_to(points[index], points[index + 1])

        if distance <= distanceToNextPoint:
            """
            distanceToNextPoint is within this point and the next.
            Return the destination point with moveTowards().
            """
            return move_towards(points[index], points[index + 1], distance)
        else:
            """
            The destination is further from the next point. Subtract
            distanceToNextPoint from distance and continue recursively.
            """
            return move_along_path(points, distance - distanceToNextPoint, index + 1)
    else:
        """
        There are no further points. The distance exceeds the length
        of the full path. Return null.
        """
        return None


def segment_polyline(points, segmentation_distance):
    """
    Splits polyline into segments of n meters
    :param points:
    :param segmentation_distance:
    :return:
    """
    segmentation_needle = 0
    final = []

    while True:
        next_point = move_along_path(points, segmentation_needle)

        if next_point is not None:
            final.append(next_point)
            segmentation_needle += segmentation_distance
        else:
            break

    return final
