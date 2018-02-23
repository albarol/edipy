# coding: utf-8

from collections import OrderedDict

from edipy import fields, exceptions


def parse(model, data):
    fields = model._fields.iteritems()
    instance = model()
    for (name, fixed_type) in fields:
        value = data[0:fixed_type.size]
        setattr(instance, name, fixed_type.encode(value))
        data = data[fixed_type.size:]

    if data:
        raise exceptions.LayoutException(':moises:')

    return instance

