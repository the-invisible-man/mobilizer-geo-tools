import polyline
import sqlalchemy
import elasticsearch
import pprint
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

doc = {
    "listing_id": "5e37d91a-23d4-11e6-b67b-9e71128cae77",
    "location": "40.795615, -74.165099"
}