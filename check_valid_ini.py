import configparser
from io import StringIO

def is_valid_ini(ini_string: str) -> bool:
    """This functions returns true if the string ini_string is a valid INI file, else false"""
    config = configparser.ConfigParser()
    ini_stream = StringIO(ini_string)
    
    try:
        config.read_file(ini_stream)
        # If no sections are parsed, it's not valid
        if len(config.sections()) == 0:
            return False
        return True
    except (configparser.MissingSectionHeaderError, configparser.ParsingError):
        return False