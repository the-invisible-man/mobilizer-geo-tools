import polyline
from sqlalchemy import create_engine
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pprint
from GeoMath import *
from Utils import *
from pprint import pprint

"""
This file grabs encoded polylines from our database and segments them
into 15  mile pieces.  The polyline is segmented by geopoints and the
points are stored in Elasticsearch for geospatial querying.

@author Carlos Granados
"""

"""
Note  that all  of our math functions assume metric system,
we  will need  to convert  from miles to  kilometers before
anything. The following is the meter equivalent of 15 miles

"""


engine = create_engine('mysql://homestead:secret@localhost:443/homestead')
connection = engine.connect()
es = Elasticsearch(['192.168.10.10'])
index = "listings"
doc_type = "route"
"""
Fetch all jobs
"""
for job in fetch_pending(connection):
    overview_path = job['overview_path']
    id = job['id']
    listing_id = job['fk_listing_id']
    docs = []

    mark_in_progress(id, connection)

    path = polyline.decode(overview_path)

    # We grabbed the jobs, save geospatial data to elasticsearch
    for point in path:
        # we need to invert these points to follow the GeoJSON format
        formatted_point = [point[1], point[0]]
        action = {
            "_index": "listings",
            "_type": "route",
            "_source" : {
                "listing_id": listing_id,
                "location": formatted_point
            }
        }
        docs.append(action)

    # Now we will apply this experimental algorithm to expand
    # the path and get even more points. If this works we'll be
    # able to match riders with more results and with more precision.
    # This is probably a really bad idea since the math isn't so precise
    # and the segmentation isn't always the length specified, it'll vary
    # from point to point, but it should lie within the desired range.
    # for point in segment_polyline(path, 24140):
        # geopoint = {"id": listing_id, "location": point}
        # docs.append(geopoint)

    print "pushed " + len(docs).__str__() + " docs"
    # Push data to elasticsearch
    helpers.bulk(es, docs)
    mark_done(id, connection)