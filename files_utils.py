import os
import fnmatch


def glob_files(directory, glob):  # pylint: disable=redefined-builtin
    """
    Return a list of files in a directory matching a glob and extension.

    Parameters
    ----------
    directory : str
        The directory to search.
    glob : str
        The glob to match.

    Returns
    -------
    list of str
        The list of files.
    """
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if fnmatch.fnmatch(f, glob)
    ]

def load_code_from_file(file_path):
    """
    Load code from a file.

    Parameters
    ----------
    file_path : str
        The path to the file.

    Returns
    -------
    str
        The code.
    """
    with open(file_path, 'r') as f:
        return f.read()

