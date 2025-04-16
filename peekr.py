import sys
import os
import fnmatch
import datetime

def parse_options(args):
    """
    Parses command-line arguments and returns a dictionary of options.

    Supported options:
    - -n or -name <pattern>: filename pattern to search for (required)
    - -atime <days>: last accessed within specified number of days
    - -t or -type <f|d>: specify file type; 'f' for file, 'd' for directory
    - -m or --max-depth <depth>: max depth for directory traversal
    - <search_dir>: the directory to begin searching in (defaults to current dir)

    Returns:
        dict: Parsed options
    """
    options = {
        "name": None,
        "atime": None,
        "type": 'f',
        "maxdepth": 1,
        "search_dir": '.'
    }
    i = 0

    while i < len(args):
        arg = args[i]
        if arg.startswith('-'):
            if arg in ['-n', '-name']:
                i += 1
                if i < len(args):
                    options['name'] = args[i]

            elif arg == '-atime':
                i += 1
                if i < len(args):
                    try:
                        options['atime'] = int(args[i])
                    except ValueError:
                        print(f"Error: Invalid time value: {args[i]}")
                        sys.exit(1)

            elif arg in ['-t', '-type']:
                i += 1
                if i < len(args):
                    try:
                        if args[i].lower() not in ['f', 'd']:
                            raise ValueError()
                        options['type'] = args[i].lower()
                    except ValueError:
                        print(f"Invalid file type: {args[i]}. Try again with 'f' or 'd'")
                        sys.exit(1)

            elif arg in ['-m', '--max-depth']:
                i += 1
                if i < len(args):
                    try:
                        options['maxdepth'] = int(args[i])
                    except ValueError:
                        print(f"Error: Invalid depth value: {args[i]}")
                        sys.exit(1)

            else:
                print(f"Error: Unknown option: {arg}")
                sys.exit(1)
        else:
            options['search_dir'] = args[i]
        i += 1

    if not options['name']:
        print("Please provide a file name with -n or -name option")
        sys.exit(1)

    return options


def matchFile(file_path, options):
    """
    Checks whether a file matches the search criteria.

    Args:
        file_path (str): Full path of the file or directory
        options (dict): Search options

    Returns:
        bool: True if the file matches all criteria, False otherwise
    """
    file_name = os.path.basename(file_path)

    if not fnmatch.fnmatch(file_name, options['name']):
        return False

    is_file = os.path.isfile(file_path)

    if options['type'] == 'f' and not is_file:
        return False
    if options['type'] == 'd' and is_file:
        return False

    if options['atime'] is not None:
        last_access = datetime.datetime.fromtimestamp(os.path.getatime(file_path))
        days_since_access = (datetime.datetime.now() - last_access).days
        if days_since_access > options['atime']:
            return False

    return True


def traverse(curr_dir, curr_depth, options):
    """
    Recursively traverses directories up to a specified depth and prints
    files that match the criteria.

    Args:
        curr_dir (str): Current directory path
        curr_depth (int): Current depth in the directory tree
        options (dict): Search options
    """
    if curr_depth <= options['maxdepth']:
        try:
            for entry in os.listdir(curr_dir):
                entry_path = os.path.join(curr_dir, entry)

                if matchFile(entry_path, options):
                    print(entry_path)

                if os.path.isdir(entry_path):
                    traverse(entry_path, curr_depth + 1, options)
        except (PermissionError, OSError):
            pass


def peek(options):
    """
    Starts the file search based on given options.

    Args:
        options (dict): Search options
    """
    search_dir = options['search_dir']
    traverse(search_dir, 1, options)


if __name__ == '__main__':
    options = parse_options(sys.argv)
    peek(options)
