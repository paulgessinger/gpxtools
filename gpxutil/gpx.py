import gpxpy
import gpxpy.gpx
from datetime import datetime

from .util import Interval

def interval_from_track(track):
    total_intvl = None
    for segment in track.segments:
        dts = [p.time for p in segment.points]
        intvl = Interval(min(dts), max(dts))

        if total_intvl is None:
            total_intvl = intvl
        else:
            total_intvl = total_intvl + intvl

    return total_intvl

def merge_segments(segments):
    return segments

def merge_tracks(tracks):
    all_tracks = [(track, interval_from_track(track)) for track in tracks]

    while True:
        noverlap = 0

        for i in range(len(all_tracks)):
            if all_tracks[i] is None: 
                # we already merged this track as a track b
                continue

            track_a, intvl_a = all_tracks[i]
            for j in range(i+1, len(all_tracks)):
                print(i, j)

                if all_tracks[j] is None: 
                    # we already merged this track as a track b
                    continue

                track_b, intvl_b = all_tracks[j]
                
                print(intvl_a, intvl_b)
                print(intvl_a.overlap(intvl_b))
                if intvl_a.overlap(intvl_b):
                    print("overlap", intvl_a, intvl_b)
                    new_track = gpxpy.gpx.GPXTrack()
                    new_track.segments = merge_segments(track_a.segments + track_b.segments)
                    
                    # replace track a with merged, remove track b
                    all_tracks[i] = (new_track, intvl_a + intvl_b)
                    all_tracks[j] = None
                    noverlap += 1
                    break # break out of inner, we have a overlap for track a already

        if noverlap == 0:
            # we did not find any overlaps, we're done
            break

    all_tracks = [t for t in all_tracks if t is not None]

    return [track for track, _ in all_tracks]


def merge_gpx(a, b):
    print("merging")

    gpx = gpxpy.gpx.GPX()

    tracks = merge_tracks(a.tracks + b.tracks)
    gpx.tracks = tracks

    return gpx
