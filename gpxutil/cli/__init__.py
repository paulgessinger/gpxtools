import argparse
import logging
import sys

from .create_tracklog import CreateTracklog

# def create_tracklog(args):


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    subparsers = parser.add_subparsers(help="subcommands", dest="subcommand")
    subparsers.required = True

    create_tracklog_parser = subparsers.add_parser("create-tracklog", help=CreateTracklog.__doc__)
    CreateTracklog(create_tracklog_parser)


    args = parser.parse_args()

    logging.basicConfig(format='%(levelname)-8s %(name)s : %(message)s', level=logging.INFO if not args.verbose else logging.DEBUG)

    try:
        args.func(args)
    except Exception as e:
        logging.critical(str(e))
        if args.verbose:
            raise e
        else:
            sys.exit(1)

    # print(args, len(files))
