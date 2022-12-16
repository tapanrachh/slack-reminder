import re


def remove_extra_spaces(string):
    string = string.strip()
    string = re.sub(' +', ' ', string)
    return string


def are_valid_hours(arg):
    if not arg:
        return False
    arg = str(arg)
    try:
        arg = int(arg)
        if arg > -1 and arg < 24:
            return str(arg)
    except Exception:
        return False


def are_valid_minutes(arg):
    if not arg:
        return False
    arg = str(arg)
    try:
        arg = int(arg)
        if arg > -1 and arg < 60:
            return str(arg)
    except Exception:
        return False
