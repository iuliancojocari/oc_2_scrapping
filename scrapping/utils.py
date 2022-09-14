import os


def create_directory(directory):
    """
    Create new directory
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
