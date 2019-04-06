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