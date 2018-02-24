# coding: utf-8

import re


class Validator(object):

    def validate(self, value):
        return True


class Required(Validator):

    def validate(self, value):
        return True if value else False


class Range(Validator):

    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        return self.min_value <= value <= self.max_value


class Email(Validator):
    expression = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    def validate(self, value):
        return True if self.expression.search(value) else False


class Cep(Validator):
    expression = re.compile(r"^[0-9]{8}\b")

    def validate(self, value):
        return True if self.expression.search(value) else False
