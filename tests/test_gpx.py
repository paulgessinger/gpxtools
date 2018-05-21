from gpxutil.gpx import merge_gpx, merge_segments
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

def _make_segment(data):
    segment = gpxpy.gpx.GPXTrackSegment()
    for point_data in data:
        lat, lng, dtargs = point_data
        dt = datetime(*dtargs)
        point = gpxpy.gpx.GPXTrackPoint(lat, lng, time=dt)
        segment.points.append(point)
    return segment

def test_merge_segments():
    # no overlap
    seg_a = _make_segment([
        (42.0, 10.0, (2018, 5, 12, 10, 0, 0)),
        (42.0, 10.0, (2018, 5, 12, 11, 0, 0)),
        (42.0, 10.0, (2018, 5, 12, 12, 0, 0)),
        (42.0, 10.0, (2018, 5, 12, 13, 0, 0)),
        (42.0, 10.0, (2018, 5, 12, 14, 0, 0)),
    ])

    seg_b = _make_segment([
        (42.0, 10.0, (2018, 5, 12, 16, 0, 0)),
        (42.0, 10.0, (2018, 5, 12, 17, 0, 0)),
        (42.0, 10.0, (2018, 5, 12, 18, 0, 0)),
    ])

    merged_segs = merge_segments([seg_a, seg_b])
    assert len(merged_segs) == 2
    assert merged_segs[0].points[0].time == seg_a.points[0].time
    assert merged_segs[1].points[2].time == seg_b.points[2].time



    # with overlap
    seg_a = _make_segment([
        (42.0, 10.0, (2018, 5, 12, 10, 0, 0)),
        (42.0, 10.0, (2018, 5, 12, 11, 0, 0)),
        (42.0, 10.0, (2018, 5, 12, 12, 0, 0)),
        (42.0, 10.0, (2018, 5, 12, 13, 0, 0)),
        (42.0, 10.0, (2018, 5, 12, 14, 0, 0)),
    ])

    seg_b = _make_segment([
        (42.0, 10.0, (2018, 5, 12, 13, 30, 0)),
        (42.0, 10.0, (2018, 5, 12, 17, 0, 0)),
        (42.0, 10.0, (2018, 5, 12, 18, 0, 0)),
    ])
    
    merged_segs = merge_segments([seg_a, seg_b])
    assert len(merged_segs) == 1
    assert len(merged_segs[0].points) == 8
    assert merged_segs[0].points[0].time == seg_a.points[0].time
    assert merged_segs[0].points[7].time == seg_b.points[2].time

    # with overlap and extra
    seg_c = _make_segment([
        (42.0, 10.0, (2018, 5, 12, 20, 0, 0)),
        (42.0, 10.0, (2018, 5, 12, 23, 0, 0)),
    ])

    merged_segs = merge_segments([seg_a, seg_b, seg_c])
    assert len(merged_segs) == 2
    assert len(merged_segs[0].points) == 8
    assert len(merged_segs[1].points) == 2
    assert merged_segs[0].points[0].time == seg_a.points[0].time
    assert merged_segs[0].points[7].time == seg_b.points[2].time
    assert merged_segs[1].points[0].time == seg_c.points[0].time
    assert merged_segs[1].points[1].time == seg_c.points[1].time


    # with bridged overlap
    seg_a = _make_segment([
        (42.0, 10.0, (2018, 5, 12, 10, 0, 0)),
        (42.0, 10.0, (2018, 5, 12, 14, 0, 0)),
    ])

    seg_b = _make_segment([
        (42.0, 10.0, (2018, 5, 12, 13, 0, 0)),
        (42.0, 10.0, (2018, 5, 12, 18, 0, 0)),
    ])
    
    seg_c = _make_segment([
        (42.0, 10.0, (2018, 5, 12, 17, 0, 0)),
        (42.0, 10.0, (2018, 5, 12, 20, 0, 0)),
    ])

    merged_segs = merge_segments([seg_a, seg_b, seg_c])
    assert len(merged_segs) == 1
    assert len(merged_segs[0].points) == 6
    assert merged_segs[0].points[0].time == seg_a.points[0].time
    assert merged_segs[0].points[5].time == seg_c.points[1].time


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
                (42.0, 10.0, (2018, 5, 12, 13, 30, 0)),
                (42.0, 10.0, (2018, 5, 12, 14, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 17, 0, 0)),
                (42.0, 10.0, (2018, 5, 12, 18, 0, 0)),
            ]
        ]   
    ])

    merged = merge_gpx(gpx_a, gpx_b)
    assert merged.to_xml() == gpx_exp.to_xml()

