from gpxutil.gpx import merge_gpx
import gpxpy
import gpxpy.gpx
from datetime import datetime

def _make_gpx(data):
    gpx = gpxpy.gpx.GPX()
    for track_data in data:
        track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(track)

        for segment_data in track_data:
            segment = gpxpy.gpx.GPXTrackSegment()
            track.segments.append(segment)
            
            for point_data in segment_data:
                # print(point_data)
                lat, lng, dtargs = point_data
                dt = datetime(*dtargs)
                point = gpxpy.gpx.GPXTrackPoint(lat, lng, time=dt)
                segment.points.append(point)

    # print(gpx.to_xml())
    return gpx



def test_merge_gpx():
    print("hallo")

    # one track each, one segment, no overlap
    gpx_a = _make_gpx([
        [ # track
            [ # segment
                (42.0, 10.0, (2018, 5, 12, 10, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 11, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 12, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 13, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 14, 0, 0)),
            ]
        ]   
    ])
   
    gpx_b = _make_gpx([
        [ # track
            [ # segment
                (42.0, 10.0, (2018, 5, 12, 16, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 17, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 18, 0, 0)),
            ]
        ]
    ])
    
    gpx_exp = _make_gpx([
        [ # track
            [ # segment
                (42.0, 10.0, (2018, 5, 12, 10, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 11, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 12, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 13, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 14, 0, 0)),
            ],
        ],
        [ # track
            [ # segment
                (42.0, 10.0, (2018, 5, 12, 16, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 17, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 18, 0, 0)),
            ]
        ]   
    ])

    merged = merge_gpx(gpx_a, gpx_b)
    assert merged.to_xml() == gpx_exp.to_xml()

    # one track each, one segment, has overlap
    gpx_a = _make_gpx([
        [ # track
            [ # segment
                (42.0, 10.0, (2018, 5, 12, 10, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 11, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 12, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 13, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 14, 0, 0)),
            ]
        ]   
    ])
   
    gpx_b = _make_gpx([
        [ # track
            [ # segment
                (42.0, 10.0, (2018, 5, 12, 13, 30, 0)),
                (42.0, 10.0, (2018, 5, 12, 17, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 18, 0, 0)),
            ]
        ]
    ])
    
    gpx_exp = _make_gpx([
        [ # track
            [ # segment
                (42.0, 10.0, (2018, 5, 12, 10, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 11, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 12, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 13, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 14, 0, 0)),
            ],
            [ # segment
                (42.0, 10.0, (2018, 5, 12, 13, 30, 0)),
                (42.0, 10.0, (2018, 5, 12, 17, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 18, 0, 0)),
            ]
        ]   
    ])

    merged = merge_gpx(gpx_a, gpx_b)
    assert merged.to_xml() == gpx_exp.to_xml()


    # gpx_a = """
# <?xml version="1.0" encoding="UTF-8"?>
# <gpx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/0" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd" version="1.0" creator="gpx.py -- https://github.com/tkrajina/gpxpy">
# <trk>
# <trkseg>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T10:00:00Z</time></trkpt>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T11:00:00Z</time></trkpt>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T12:00:00Z</time></trkpt>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T13:00:00Z</time></trkpt>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T14:00:00Z</time></trkpt>
# </trkseg>
# <trkseg>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T20:00:00Z</time></trkpt>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T21:00:00Z</time></trkpt>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T22:00:00Z</time></trkpt>
# </trkseg>
# </trk>
    # """
    # gpx_b = """
# <?xml version="1.0" encoding="UTF-8"?>
# <gpx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/0" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd" version="1.0" creator="gpx.py -- https://github.com/tkrajina/gpxpy">
# <trk>
# <trkseg>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T07:00:00Z</time></trkpt>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T08:00:00Z</time></trkpt>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T09:00:00Z</time></trkpt>
# </trkseg>
# <trkseg>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T16:00:00Z</time></trkpt>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T17:00:00Z</time></trkpt>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T18:00:00Z</time></trkpt>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T19:00:00Z</time></trkpt>
# </trkseg>
# <trkseg>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T20:30:00Z</time></trkpt>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T21:30:00Z</time></trkpt>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T22:30:00Z</time></trkpt>
# <trkpt lat="42.0" lon="10.0"><time>2018-05-12T23:00:00Z</time></trkpt>
# </trkseg>
# </trk>
    # """
