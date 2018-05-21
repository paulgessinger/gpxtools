from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import logging
import os
from datetime import datetime

import gpxpy
import gpxpy.gpx

class ImageMetaDataError(ValueError):
    pass


class ImageMetaData:
    """
    Extracts meta data from image files using PIL.
    Parts adapted from https://gist.github.com/erans/983821/cce3712b82b3de71c73fbce9640e25adef2b0392
    """

    def __init__(self, path):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Getting image info for %s", path)
        if not os.path.exists(path):
            raise ImageMetaDataError("Image at {} does not exist".format(path))

        try:
            self.image = Image.open(path)
        except OSError as e:
            # this is most likely because of a non-image type
            raise ImageMetaDataError("Not an image")
        self.exif_data = self._get_exif_data()
        self.datetime = datetime.strptime(self.exif_data["DateTime"], "%Y:%m:%d %H:%M:%S")
        self.lat, self.lng = self._get_lat_lng()

    def _get_exif_data(self):
        """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
        exif_data = {}
        info = self.image._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]

                    exif_data[decoded] = gps_data
                else:
                    exif_data[decoded] = value

        return exif_data

    def _get_if_exist(self, data, key):
        if key in data:
            return data[key]
            
        return None

    def _convert_to_degrees(self, value):
        """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
        d0 = value[0][0]
        d1 = value[0][1]
        d = float(d0) / float(d1)

        m0 = value[1][0]
        m1 = value[1][1]
        m = float(m0) / float(m1)

        s0 = value[2][0]
        s1 = value[2][1]
        s = float(s0) / float(s1)

        return d + (m / 60.0) + (s / 3600.0)

    def _get_lat_lng(self):
        """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
        lat = None
        lon = None


        if "GPSInfo" in self.exif_data:
            gps_info = self.exif_data["GPSInfo"]

            gps_latitude = self._get_if_exist(gps_info, "GPSLatitude")
            gps_latitude_ref = self._get_if_exist(gps_info, 'GPSLatitudeRef')
            gps_longitude = self._get_if_exist(gps_info, 'GPSLongitude')
            gps_longitude_ref = self._get_if_exist(gps_info, 'GPSLongitudeRef')

            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                lat = self._convert_to_degrees(gps_latitude)
                if gps_latitude_ref != "N":                     
                    lat = 0 - lat

                lon = self._convert_to_degrees(gps_longitude)
                if gps_longitude_ref != "E":
                    lon = 0 - lon

        return lat, lon

class ImageList:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.images = []

    def add(self, image):
        if image.lat is None or image.lng is None:
            self.logger.warning("Not adding image without location data")
            return
        self.images.append(image)

    def to_gpx(self):
        self.images = sorted(self.images, key=lambda i: i.datetime)

        gpx = gpxpy.gpx.GPX()
        track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(track)


        prev_image = None
        current_segment = gpxpy.gpx.GPXTrackSegment()
        track.segments.append(current_segment)

        for img in self.images:
            print(img.datetime, img.lat, img.lng)
            point = gpxpy.gpx.GPXTrackPoint(img.lat, img.lng, time=img.datetime)

            if prev_image is not None:
                if prev_image.datetime.date() != img.datetime.date():
                    self.logger.debug("new day => new segment")
                    current_segment = gpxpy.gpx.GPXTrackSegment()
                    track.segments.append(current_segment)

            prev_image = img
            current_segment.points.append(point)


        return gpx.to_xml()
