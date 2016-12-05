class ParseException(Exception):
    def __init__(self, message):
        self.message = message


class ConversionException(Exception):
    def __init__(self, message):
        self.message = message
