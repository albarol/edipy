# coding: utf-8

from datetime import datetime
from decimal import Decimal as DecimalType
from collections import OrderedDict
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

    def __init__(self, required=True, validators=None):
        self.__order__ = self.__counter.next()
        self.validators = validators if validators else []
        self.required = required

    def _has_value(self, value):
        return value and not value.isspace() 

    def encode(self, value):
        if self.required and (not self._has_value(value) or len(value) != self.size):
            raise exceptions.RequiredFieldError()

        if not self.required and (not value or value.isspace()):
            return None

        value = self._to_python(value)
        for validator in self.validators:
            validator.validate(value)
        return value

    def _to_python(self, value):
        return str(value)

    def decode(self, value):
        return self._to_edi(value)

    def _to_edi(self, value):
        return value


class Integer(FixedType):
    zfill = False

    def __init__(self, size, zfill=False, required=True, validators=None):
        super(Integer, self).__init__(validators=validators, required=required)
        self.size = size
        self.zfill = zfill

    def _to_python(self, value):
        return int(value[-self.size:])

    def decode(self, value):
        return str(value)


class String(FixedType):

    def __init__(self, size, required=True, validators=None):
        super(String, self).__init__(validators=validators, required=required)
        self.size = size

    def _to_python(self, value):
        return value[:self.size]

    def decode(self, value):
        return value


class Identifier(FixedType):

    def __init__(self, identifier, required=True, validators=None):
        super(Identifier, self).__init__(validators=validators, required=required)
        self.size = len(identifier)
        self.identifier = identifier


    def _to_python(self, value):
        if value != self.identifier:
            raise exceptions.ValidationError()
        return self.identifier


class Decimal(FixedType):

    def __init__(self, size, digits=0, required=True, validators=None):
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

    def __init__(self, size, date_format, required=True, validators=None):
        super(DateTime, self).__init__(validators=validators, required=required)
        self.size = size
        self.date_format = date_format

    def _to_python(self, value):
        try:
            return datetime.strptime(value, self.date_format)
        except ValueError as e:
            if not self.required:
                return None
            raise e


class Date(DateTime):

    def _to_python(self, value):
        ret = super(Date, self)._to_python(value)
        if ret:
            return ret.date()
        return ret


class Time(DateTime):

    def _to_python(self, value):
        ret = super(Time, self)._to_python(value)
        if ret:
            return ret.time()
        return ret


class CompositeField(FixedType):

    def __init__(self, cls, occurrences=1, required=True):
        super(CompositeField, self).__init__(validators=None, required=required)
        if not issubclass(cls, EDIModel):
            raise exceptions.BadFormatError(message=u"Field is not subclass of EDIModel.")


        self.occurrences = occurrences        
	self.size = cls._size
        self.model = cls

    def encode(self, value):
        return self._to_python(value)

    def _to_python(self, value):
        return (self.model, value)


class Register(CompositeField):

    def __init__(self, cls, occurrences=1, required=True):
        super(Register, self).__init__(cls, occurrences=occurrences, required=required)

        if not cls._fields or not isinstance(cls._fields[0][1], Identifier):
            raise exceptions.BadFormatError(message=u"First argument must be an Identifier.")

        if isinstance(occurrences, int):
            occurrences = (1, occurrences)
        self.occurrences = occurrences

    @property
    def min_occurrences(self):
        return self.occurrences[0]

    @property
    def max_occurrences(self):
        return self.occurrences[1]


class Enum(FixedType):

    def __init__(self, values, required=True, validators=None):
        super(Enum, self).__init__(validators=validators, required=required)

        if not values:
            raise exceptions.BadFormatError(u"Empty value is not a valid value.")

        self.values = map(str, values)
        self.size = len(self.values[0])

        if not all([len(v) == self.size for v in self.values]):
            raise exceptions.BadFormatError(u"All values must have the same size.")

    def _to_python(self, value):
        if value not in self.values:
            raise exceptions.ValidationError(u"Value {} is not a valid value.")
        return value


class EDIMeta(type):

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        values = [(k, v, v.size) for (k, v) in attrs.iteritems() if isinstance(v, FixedType)]
        new_cls._fields = [(k, v) for (k, v, s) in sorted(values, key=lambda (k, v, s): v.__order__)]
        new_cls._size = sum([s for k, v, s in values])
        return new_cls


class EDIModel(object):
    __metaclass__ = EDIMeta
