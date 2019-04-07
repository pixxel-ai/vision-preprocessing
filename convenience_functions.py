#%%
from pathlib import Path

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
# Testing is_file()

if __name__=='__main__':
    TEST = Path.cwd()/'convenience_functions.py'
    print(is_file(TEST))
    TEST = Path.cwd()/'convenience_functions2.py'
    print(is_file(TEST))

    #%%
    DELETE = Path.cwd()/'MSK_OUT'/'I_0crop2.png'
    delete_file(DELETE)