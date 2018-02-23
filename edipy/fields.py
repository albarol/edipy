# coding: utf-8

from decimal import Decimal as DecimalType
from collections import OrderedDict
import itertools


class FixedType(object):
    """
    Due python 2.7 does not respect the order of
    class declaration, here we have to set a counter
    which will emulate the order.
    """
    __counter = itertools.count()
    size = 0

    def __init__(self):
        self.__order__ = self.__counter.next()

    def encode(self, value):
       return value

    def decode(self, value):
        return value


class Integer(FixedType):
    zfill = False

    def __init__(self, size, zfill=False):
        super(Integer, self).__init__()
        self.size = size
        self.zfill = zfill

    def encode(self, value):
        return int(value)

    def decode(self, value):
        return str(value)


class String(FixedType):

    def __init__(self, size):
        super(String, self).__init__()
        self.size = size

    def encode(self, value):
        return value

    def decode(self, value):
        return value


class DateTime(FixedType):

    def __init__(self, size, timezone=None):
        super(DateTime, self).__init__()
        self.size = size


class Decimal(FixedType):

    def __init__(self, size, digits=0):
        super(Decimal, self).__init__()
        self.size = size + digits
        self.value = size
        self.digits = digits

    def encode(self, value):
        if self.digits:
            denominator, digits = value[0:self.value], value[-self.digits:]
        else:
            denominator, digits = value, ""
        return DecimalType("{}.{}".format(denominator, digits))


class EDIMeta(type):

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        values = [(k, v, v.size) for k, v in attrs.iteritems() if isinstance(v, FixedType)]
        new_cls._fields = OrderedDict([(k, v) for (k, v, s) in sorted(values, key=lambda (k, v, s): v.__order__)])
        new_cls._size = sum([s for k, v, s in values])
        return new_cls


class EDIModel(object):
    __metaclass__ = EDIMeta
