"""pre-commit hook to validate fixlet id in BigFix BES files."""

import argparse
import os
import re

MAX_ID = 2147483647  # maximum allowable Fixlet ID

def build_argument_parser():
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("filenames", nargs="*", help="Filenames to check.")
    return parser

def validate_filename_id(filename):
    """Validate if the Fixlet ID in the filename is not greater than MAX_ID."""
    basename = os.path.basename(filename)
    match = re.match(r"(\d+)", basename)
    if match:
        file_id = int(match.group(1))
        if file_id > MAX_ID:
            print(f"Error: ID {file_id} in file {filename} is greater than the maximum allowed value {MAX_ID}.")
            return False
    return True

def main(argv=None):
    """Main process."""
    argparser = build_argument_parser()
    args = argparser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        if not validate_filename_id(filename):
            retval += 1

    return retval

if __name__ == "__main__":
    exit(main())
