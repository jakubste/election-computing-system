class BadDataFormatException(Exception):
    def __str__(self):
        return 'Empty line instead of vote data'
