# coding: utf-8

from datetime import datetime
from decimal import Decimal as DecimalType
import itertools

from edipy import exceptions


class FixedType(object):
    """
    Due python 2.7 does not respect the order of
    class declaration, here we have to set a counter
    which will emulate the order.
    """
    __counter = itertools.count()
    size = 0

    def __init__(self, required=False, validators=None):
        self.__order__ = self.__counter.next()
        self.validators = validators if validators else []
        self.required = required

    def _has_value(self, value):
        return value and not value.isspace()

    def encode(self, value):
        if self.required and not self._has_value(value):
            raise exceptions.ValidationError(u"Field is required.")

        if not self.required and not self._has_value(value):
            return None

        value = self._to_python(value)
        for validator in self.validators:
            if not validator.validate(value):
                raise exceptions.ValidationError()
        return value

    def _to_python(self, value):
        return str(value)

    def decode(self, value):
        return self._to_edi(value)

    def _to_edi(self, value):
        return value


class Integer(FixedType):
    zfill = False

    def __init__(self, size, zfill=False, required=False, validators=None):
        super(Integer, self).__init__(validators=validators, required=required)
        self.size = size
        self.zfill = zfill

    def _to_python(self, value):
        return int(value[-self.size:])

    def decode(self, value):
        return str(value)


class String(FixedType):

    def __init__(self, size, required=False, validators=None):
        super(String, self).__init__(validators=validators, required=required)
        self.size = size

    def _to_python(self, value):
        return value[:self.size]

    def decode(self, value):
        return value


class Identifier(FixedType):

    def __init__(self, identifier, required=False, validators=None):
        super(Identifier, self).__init__(validators=validators, required=required)
        self.size = len(identifier)
        self.identifier = identifier


    def _to_python(self, value):
        if value != self.identifier:
            raise exceptions.ValidationError()
        return self.identifier


class Decimal(FixedType):

    def __init__(self, size, digits=0, required=False, validators=None):
        super(Decimal, self).__init__(validators=validators, required=required)
        self.size = size + digits
        self.denominator = size
        self.digits = digits

    def _to_python(self, value):
        if self.digits:
            denominator, digits = value[:-self.digits], value[-self.digits:]
            denominator = denominator[-self.denominator:]
        else:
            denominator, digits = value[-self.denominator:], ""
        return DecimalType("{}.{}".format(denominator, digits))


class DateTime(FixedType):

    def __init__(self, size, date_format, required=False, validators=None):
        super(DateTime, self).__init__(validators=validators, required=required)
        self.size = size
        self.date_format = date_format

    def _to_python(self, value):
        return datetime.strptime(value, self.date_format)


class Register(FixedType):

    def __init__(self, cls, required=False, validators=None):
        super(Register, self).__init__(validators=validators, required=required)
        if not issubclass(cls, EDIModel):
            raise exceptions.BadFormatError(message=u"Field is not subclass of EDIModel.")

        if not cls._fields or not isinstance(cls._fields[0][1], Identifier):
            raise exceptions.BadFormatError(message=u"First argument must be an Identifier.")

        self.size = cls._size
        self.model = cls

    def _to_python(self, value):
        return (self.model, value)


class Enum(FixedType):
    size = 1

    def __init__(self, values, required=False, validators=None):
        super(Enum, self).__init__(validators=validators, required=required)

        if not values or any([value for value in values if len(value) != 1]):
            raise exceptions.BadFormatError()
        self.values = set(values)

    def _to_python(self, value):
        if value not in self.values:
            raise exceptions.ValidationError()
        return value


class EDIMeta(type):

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        values = [(k, v, v.size) for k, v in attrs.iteritems() if isinstance(v, FixedType)]
        new_cls._fields = [(k, v) for (k, v, s) in sorted(values, key=lambda (k, v, s): v.__order__)]
        new_cls._size = sum([s for k, v, s in values])
        return new_cls


class EDIModel(object):
    __metaclass__ = EDIMeta
