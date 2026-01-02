import re
import sys
import argparse
from datetime import datetime

def check_file(filename):
    # Regex to capture: Day (Wed) and Date (29 Jan 2025)
    pattern = r"<Value>([A-Za-z]{3}),\s+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})"
    failed = False

    try:
        with open(filename, 'r') as f:
            content = f.read()
            matches = re.finditer(pattern, content)

            for match in matches:
                provided_day = match.group(1)
                date_str = match.group(2)

                try:
                    date_obj = datetime.strptime(date_str, "%d %b %Y")
                    actual_day = date_obj.strftime("%a")

                    if provided_day != actual_day:
                        print(f"❌ {filename}: Found '{provided_day}', but {date_str} is a {actual_day}")
                        failed = True
                except ValueError:
                    print(f"⚠️ {filename}: Could not parse date format in '{match.group(0)}'")
                    failed = True

    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return 1

    return 1 if failed else 0

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    exit_code = 0
    for filename in args.filenames:
        if check_file(filename) != 0:
            exit_code = 1
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
