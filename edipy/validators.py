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


class MaxValue(Validator):
    """Validate if a value is greater than the limit"""

    def __init__(self, max_value):
        self.max_value = max_value

    def validate(self, value):
        if not value <= self.max_value:
            raise exceptions.ValidationError(u"Value {0} is greater than max value.".format(value))
        return True


class MinValue(Validator):
    """Validate if a value is lesser than then limit"""

    def __init__(self, min_value):
        self.min_value = min_value

    def validate(self, value):
        if not value <= self.min_value:
            raise exceptions.ValidationError(u"Value {0} is lesser than min value.".format(value))
        return True


class Regex(Validator):
    """Validates if a value matches the expression"""

    def __init__(self, pattern):
        try:
            self.pattern = re.compile(r'{0}'.format(pattern))
        except:
            raise ValueError("{0} is not a valid regex pattern.")

    def validate(self, value):
        if not self.pattern.match(value):
            raise exceptions.ValidationError(u"Value {0} has not matched with regex.".format(value))
        return True


class Email(Validator):
    """Validates if value is a valid email"""
    expression = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    def validate(self, value):
        if not self.expression.search(value):
            raise exceptions.ValidationError(u"Value {0} is not a valid email.".format(value))
        return True

