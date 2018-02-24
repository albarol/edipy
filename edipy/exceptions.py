# coding: utf-8


class EDIException(Exception):
    pass


class WrongLayoutError(EDIException):
    pass


class ValidationError(EDIException):
    pass


class FieldNotSupportedError(EDIException):
    pass
