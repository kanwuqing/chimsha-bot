import win32com.client
objShell = win32com.client.Dispatch("WScript.Shell")
allUserProgramsMenu = objShell.SpecialFolders("AllUsersPrograms")
# print(allUserProgramsMenu)
shortcut = objShell.CreateShortCut("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\搜狗输入法医生版\\皮肤小盒子.lnk")
print(shortcut.Targetpath)



import os
import tkinter as tk
from tkinter import filedialog



def file_ext(filename, level=1):
    """
    return extension of filename

    Parameters:
    -----------
    filename: str
        name of file, path can be included
    level: int
        level of extension.
        for example, if filename is 'sky.png.bak', the 1st level extension
        is 'bak', and the 2nd level extension is 'png'

    Returns:
    --------
    extension of filename
    """
    return filename.split('.')[-level]


def _contain_file(path, extensions):
    """
    check whether path contains any file whose extension is in extensions list

    Parameters:
    -----------
    path: str
        path to be checked
    extensions: str or list/tuple of str
        extension or extensions list

    Returns:
    --------
    return True if contains, else return False
    """
    assert os.path.exists(path), 'path must exist'
    assert os.path.isdir(path), 'path must be dir'

    if isinstance(extensions, str):
        extensions = [extensions]

    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            if (extensions is None) or (file_ext(file) in extensions):
                return True
    return False


def _process_extensions(extensions=None):
    """
    preprocess and check extensions, if extensions is str, convert it to list.

    Parameters:
    -----------
    extensions: str or list/tuple of str
        file extensions

    Returns:
    --------
    extensions: list/tuple of str
        file extensions
    """
    if extensions is not None:
        if isinstance(extensions, str):
            extensions = [extensions]
        assert isinstance(extensions, (list, tuple)), \
            'extensions must be str or list/tuple of str'
        for ext in extensions:
            assert isinstance(ext, str), 'extension must be str'
    return extensions


def get_files(path, extensions=None, is_recursive=True):
    """
    read files in path. if extensions is None, read all files, if extensions
    are specified, only read the files who have one of the extensions. if
    is_recursive is True, recursively read all files, if is_recursive is False,
    only read files in current path.

    Parameters:
    -----------
    path: str
        path to be read
    extensions: str or list/tuple of str
        file extensions
    is_recursive: bool
        whether read files recursively. read recursively is True, while just
        read files in current path if False

    Returns:
    --------
    files: the obtained files in path
    """
    extensions = _process_extensions(extensions)
    files = []
    # get files in current path
    if not is_recursive:
        for name in os.listdir(path):
            fullname = os.path.join(path, name)
            if os.path.isfile(fullname):
                if (extensions is None) or (file_ext(fullname) in extensions):
                    files.append(fullname)
        return files
    # get files recursively
    for main_dir, _, sub_file_list in os.walk(path):
        for filename in sub_file_list:
            fullname = os.path.join(main_dir, filename)
            if (extensions is None) or (file_ext(fullname) in extensions):
                files.append(fullname)
    return files


def get_folders(path, extensions=None, is_recursive=True):
    """
    read folders in path. if extensions is None, read all folders, if
    extensions are specified, only read the folders who contain any files that
    have one of the extensions. if is_recursive is True, recursively read all
    folders, if is_recursive is False, only read folders in current path.

    Parameters:
    -----------
    path: str
        path to be read
    extensions: str or list/tuple of str
        file extensions
    is_recursive: bool
        whether read folders recursively. read recursively is True, while just
        read folders in current path if False

    Returns:
    --------
    folders: the obtained folders in path
    """
    extensions = _process_extensions(extensions)
    folders = []
    # get folders in current path
    if not is_recursive:
        for name in os.listdir(path):
            fullname = os.path.join(path, name)
            if os.path.isdir(fullname):
                if (extensions is None) or \
                        (_contain_file(fullname, extensions)):
                    folders.append(fullname)
        return folders
    # get folders recursively
    for main_dir, _, _ in os.walk(path):
        if (extensions is None) or (_contain_file(main_dir, extensions)):
            folders.append(main_dir)
    return folders


if __name__ == '__main__':
    path = allUserProgramsMenu

    files = get_files(path)
    # print(files)

    folders = get_folders(path)
    # print(folders)
