from sqlitedict import SqliteDict
from constants import DB_FILE


def save(key, value, cache_file=DB_FILE):
    try:
        with SqliteDict(cache_file) as mydict:
            mydict[key] = value  # Using dict[key] to store
            mydict.commit()  # Need to commit() to actually flush the data
            return True
    except Exception as ex:
        print("Error during storing data (Possibly unsupported):", ex)


def load(key, cache_file=DB_FILE):
    try:
        with SqliteDict(cache_file) as mydict:
            # No need to use commit(), since we are only loading data!
            value = mydict[key]
        return value
    except Exception as ex:
        print("Error during loading data:", ex)


def load_all(cache_file=DB_FILE):
    try:
        with SqliteDict(cache_file) as mydict:
            # No need to use commit(), since we are only loading data!
            value = list(mydict.items())
        return value
    except Exception as ex:
        print("Error during loading data:", ex)
