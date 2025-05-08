import os


def check_dir_path(dir_path: str, raise_error: bool = False) -> bool:
    """
    Check if the directory exists

    :param dir_path: the path to the directory
    :param raise_error: the parameter to identify whether is need to raise an error if there is no such directory
    :return: boolean value which reflects whether the directory exists
    """
    if os.path.exists(dir_path):
        print(f"Folder '{dir_path}' exists.")
        return True
    if raise_error:
        raise FileNotFoundError(f"The path '{dir_path}' does not exist.")
    print(f"The path '{dir_path}' does not exist.")
    return False


def make_dir(dir_path: str) -> None:
    """
    Create the directory

    :param dir_path: the path to the directory
    :return: None
    """
    os.makedirs(dir_path)
    print(f"Folder '{dir_path}' created.")


def check_dir_content(dir_path: str, raise_error: bool = False) -> bool:
    """
    Check if the directory contains files

    :param dir_path: the path to the directory
    :param raise_error: the parameter to identify whether is need to raise an error if there is no such directory
    :return: boolean value which reflects whether the directory contains files
    """
    if not os.listdir(dir_path):
        if raise_error:
            raise FileNotFoundError(f"There are no files in '{dir_path}'.")
        print(f"There are no files in the '{dir_path}'")
        return False
    return True


def empty_directory(dir_path: str) -> None:
    """
    Delete files from the directory

    :param dir_path: the path to the directory
    :return: None
    """
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
