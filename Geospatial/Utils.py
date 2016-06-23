"""
Utils
@author Carlos Granados
"""


def fetch_pending(con):
    while True:
        r = con.execute("SELECT A.`id`, A.`overview_path`, B.fk_listing_id FROM listing_routes as A JOIN listings_metadata AS B on A.id = B.`fk_listing_route_id` WHERE `status` = 'queued' AND `attempts` < 3 limit 1")
        row = list(r)
        if len(row):
            yield row[0]
        else:
            return


def prepare_data(data, path):
    print data


def mark_in_progress(id, con):
    con.execute("UPDATE listing_routes SET `status` = 'in_progress' WHERE id = '" + id + "'")


def mark_queued(id, con):
    con.execute("UPDATE listing_routes SET `status` = 'queued' WHERE id = '" + id + "'")


def mark_done(id, cod):
    cod.execute("UPDATE listing_routes SET `status` = 'done' WHERE id = '" + id  + "'")