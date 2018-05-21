import logging
import shutil
from functools import reduce

import gpxpy
import gpxpy.gpx

from ..gpx import merge_gpx

class MergeFilesCommand:
    """
    Merge multiple GPX files into one. Overlapping segments will be merged.
    """
    def __init__(self, parser):
        parser.set_defaults(func=self.__call__)
        parser.add_argument("outfile", help="Destination for the merged file.")
        parser.add_argument("files", nargs="+", help="Input files to be merged.")


    def __call__(self, args):
        logger = logging.getLogger(self.__class__.__name__)
        logger.debug("Executing")

        if len(args.files) == 1:
            shutil.copyfile(args.files[0], args.outfile)
            logger.warning("Only one input file provided, copying.")
            return

        def read(file):
            with open(file, "r") as f:
                gpxpy.parse(f)

        gpxs = map(read, args.files)

        merged = reduce(merge_gpx, gpxs)

