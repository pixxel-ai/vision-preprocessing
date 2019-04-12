#%%
from pathlib import Path
from functools import partial
from tqdm import tqdm_notebook as tqdm

#%%
def find_number_in_string(s):
    """
    Finds and returns a number sequence in a given string.
    Assumes : The string has only one continuously unbroken sequence of numbers. If there are multiple sequences,
    the first one will be returned.
    :param s: String containing number sequence. Type : str or pathlib.Path
    :return: String representation of the Number found in the string.
    """
    s = str(s)
    start = None # starting index
    end = None  # ending index
    for i in range(len(s)):
        if s[i].isdigit(): # start going over complete number sequence
            start=i
            end = i
            for j in range(start, len(s)): # loop until characters are still numbers
                if not s[j].isdigit():
                    break
                end = j
            break
    return str(int(s[start : end + 1]))  # adding 1 to end index so as to include the end index


#%%
def is_file(PATH)-> bool:
    """
    Returns True if the file at `PATH` exists with Size > 0
    """
    PATH = Path(PATH)
    file_exists = PATH.is_file()  # Checks existence of file
    if file_exists:
        if PATH.stat().st_size > 0:  # Checks file size
            return True
    return False

def delete_file(PATH)-> bool:
    PATH = Path(PATH)
    if PATH.is_file():
        PATH.unlink()
    else:
        raise FileNotFoundError
    return True

#%%
def rename_folder(PATH, rename_func):
    """
    Renames every file in given folder specified by `PATH` according to `rename_func`
    :param PATH: pathlib.Path : Path of the folder containing files to rename
    :param rename_func: callable : function that takes as input a path of a file and
                                  returns the `path` to which the file is to be renamed
    :return: returns True if all files are succesfully renamed
    """
    PATH = Path(PATH).absolute()
    for f in tqdm(PATH.iterdir()):
        f.rename(rename_func(f))
    return True

def change_suffix(file, ext):
    """
    gives a file's name with extension replaced with `ext`
    :param file: file to be renamed
    :param ext: extension to replace the existing extension of `file`
    :return: new `path` to file with the extension changed to `ext`
    """
    file = Path(file)
    return file.with_suffix(ext)