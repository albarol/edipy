# coding: utf-8

class EDIException(Exception):
    message = u"EDIException"

    def __init__(self, message=None):
        if message is not None:
            self.message = message


class WrongLayoutError(EDIException):
    message = u"The layout declared is not matching with data read."


class ValidationError(EDIException):
    message = u"Field has invalid data."


class BadFormatError(EDIException):
    message = u"Field has a bad format."
