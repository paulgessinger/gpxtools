import gpxpy
import gpxpy.gpx
from datetime import datetime
import operator

from .util import Interval

def interval_from_track(track):
    total_intvl = None
    for segment in track.segments:
        intvl = interval_from_segment(segment)
        if total_intvl is None:
            total_intvl = intvl
        else:
            total_intvl = total_intvl + intvl

    return total_intvl

def interval_from_segment(segment):
    dts = [p.time for p in segment.points]
    intvl = Interval(min(dts), max(dts))
    return intvl

def _merge(elements, do_merge=operator.add):
    while True:
        noverlap = 0

        for i in range(len(elements)):
            if elements[i] is None: 
                # we already merged this element as a track b
                continue

            element_a, intvl_a = elements[i]
            for j in range(i+1, len(elements)):
                # print(i, j)

                if elements[j] is None: 
                    # we already merged this track as a track b
                    continue

                element_b, intvl_b = elements[j]
                
                # print(intvl_a, intvl_b)
                # print(intvl_a.overlap(intvl_b))
                if intvl_a.overlap(intvl_b):
                    # print("overlap", intvl_a, intvl_b)
                    new_element = do_merge(element_a, element_b)
                    
                    # replace element a with merged, remove other
                    elements[i] = (new_element, intvl_a + intvl_b)
                    elements[j] = None
                    noverlap += 1
                    break # break out of inner, we have a overlap for track a already

        if noverlap == 0:
            # we did not find any overlaps, we're done
            break

    elements = [t for t in elements if t is not None]
    return elements

def merge_segments(segments):
    segments = [(seg, interval_from_segment(seg)) for seg in segments]

    def do_merge(seg_a, seg_b):
        seg = gpxpy.gpx.GPXTrackSegment()
        seg.points = sorted(seg_b.points + seg_a.points, key=lambda p: p.time)
        return seg
    merged_segments = _merge(segments, do_merge=do_merge)

    return [seg for seg, _ in merged_segments]

def merge_tracks(tracks):
    all_tracks = [(track, interval_from_track(track)) for track in tracks]

    def do_merge(ta, tb):
        track = gpxpy.gpx.GPXTrack()
        track.segments = merge_segments(ta.segments + tb.segments)
        return track

    merged_tracks = _merge(all_tracks, do_merge=do_merge)

    return [track for track, _ in merged_tracks]


def merge_gpx(a, b):
    gpx = gpxpy.gpx.GPX()

    tracks = merge_tracks(a.tracks + b.tracks)
    gpx.tracks = tracks

    return gpx
