# coding: utf-8

from collections import OrderedDict

from edipy import fields, exceptions


def parse(model, data):
    data = "".join(data.splitlines())
    model_fields = model._fields
    instance = model()
    for (name, fixed_type) in model_fields:
        value = data[0:fixed_type.size]

        if len(value) != fixed_type.size:
            raise exceptions.WrongLayoutError('Layout is different from data.')

        if isinstance(fixed_type, fields.Register):
            setattr(instance, name, parse(*fixed_type.encode(value)))
        else:
            setattr(instance, name, fixed_type.encode(value))
        data = data[fixed_type.size:]
    return instance
