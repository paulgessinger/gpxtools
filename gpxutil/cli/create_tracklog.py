import logging
from glob import glob
import os
import gpxpy

from ..image import ImageMetaData, ImageMetaDataError, ImageList

class CreateTracklog:
    """
    This function creates a tracklog from a series of input images.
    """

    def __init__(self, parser):
        parser.set_defaults(func=self.__call__)
        parser.add_argument("files", 
                            nargs="+",
                            help="Image files to extract GPS positions from. Can be a glob pattern")
        parser.add_argument("outfile",
                            help="Destination file for the GPX tracklog")

    def __call__(self, args):
        logger = logging.getLogger(self.__class__.__name__)
        logger.debug("Is executing")


        files = []
        if len(args.files) == 1 and "*" in args.files[0]:
            logger.debug("Only one input file given, try glob")
            files = glob(os.path.expanduser(args.files[0]), recursive=True)
        else:
            files = args.files

        logger.info("Processing %d files", len(files))


        imagelist = ImageList()

        for file in files:
            try:
                logger.debug("Processing %s", file)
                if not os.path.exists(file):
                    logger.error("Image at %s not found, skipping", file)
                    continue
                meta = ImageMetaData(file)
                imagelist.add(meta)

            except ImageMetaDataError as e:
                logger.error("Error processing %s: %s", file, str(e))
                continue

        with open(args.outfile, "w") as f:
            logger.debug("Writing to %s", args.outfile)
            f.write(imagelist.to_gpx())

        logger.info("Processing complete")



