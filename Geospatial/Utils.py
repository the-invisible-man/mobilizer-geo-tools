"""
Utils
@author Carlos Granados
"""


def fetch_pending(con):
    while True:
        r = con.execute("SELECT `id`, `overview_path` FROM listing_routes WHERE `synchronized` = 0 AND limit 1")
        if r.length:
            yield r[0]
        else:
            return
