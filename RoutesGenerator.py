import polyline
import sqlalchemy
import elasticsearch
from GeoMath import *

"""
This file grabs encoded polylines from our database and segments them
into 15  mile pieces.  The polyline is segmented by geopoints and the
points are stored in elasticsearchf for geospatial querying.

@author Carlos Granados
"""

"""
Note  that all  of our math functions assume metric system,
we  will need  to convert  from miles to  kilometers before
anything. The following is the meter equivalent of 15 miles

"""
segmentation_space = 24140.2

points = segment_polyline([], segmentation_space)
