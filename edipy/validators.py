# coding: utf-8

import re

from edipy import exceptions


class Validator(object):

    def validate(self, value):
        return True


class Range(Validator):
    """Validates if a value is comprise in two values"""

    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        if not self.min_value <= value <= self.max_value:
            raise exceptions.ValidationError(u"Value {0} is out of range.".format(value))
        return True


class Email(Validator):
    """Validates if value is a valid email"""
    expression = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    def validate(self, value):
        if not self.expression.search(value):
            raise exceptions.ValidationError(u"Value {0} is not a valid email.".format(value))
        return True


class Cep(Validator):
    """Validates if value is a valid cep"""
    expression = re.compile(r"^[0-9]{8}\b")

    def validate(self, value):
        if not self.expression.search(value):
            raise exceptions.ValidationError(u"Value {0} is not a valid cep.".format(value))
        return True

class Cnpj(Validator):
    """Validates if value is a valid cnpj"""
    expression = re.compile(r"^[0-9]{8}\b")

    def validate(self, value):
        return True
