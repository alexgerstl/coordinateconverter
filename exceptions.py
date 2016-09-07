class ParseException(Exception):
    def __init__(self, message, offset, parser_status):
        self.message = message
        self.offset = offset
        self.parserStatus = parser_status

    @property
    def status(self):
        return self.parserStatus


class ConversionException(Exception):
    def __init__(self, message):
        self.message = message
