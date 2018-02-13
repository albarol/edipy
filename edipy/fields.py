# coding: utf-8

from collections import OrderedDict
import itertools
import inspect


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

class EDIMeta(type):

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        values = [(k, v) for k, v in attrs.iteritems() if isinstance(v, FixedType)]
        new_cls._fields = OrderedDict([(k, v) for k, v in sorted(values, key=lambda (k, v): v.__order__)])
        return new_cls

class EDIModel(object):
    __metaclass__ = EDIMeta
