class MuseumpyError(Exception):
    """
    General MuseumPlus error class to provide a superclass for all other errors
    """


class MuseumPlusError(MuseumpyError):
    """
    MuseumPlus error raised when an error with the communication with MuseumPlus occurs
    """


class XMLParsingError(MuseumpyError):
    """
    The error raised when parsing the XML.
    """


class NoMoreRecordsError(MuseumpyError):
    """
    This error is raised if all records have been loaded (or no records are
    present)
    """
