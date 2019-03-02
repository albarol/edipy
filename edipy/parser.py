# coding: utf-8

from collections import OrderedDict

from edipy import fields, exceptions


def parse(model, data):
    data = "".join(data.splitlines())
    model_fields = model._fields
    instance = model()
    for (name, fixed_type) in model_fields:
        value = data[0:fixed_type.length]

        if len(value) != fixed_type.length:
            raise exceptions.WrongLayoutError('Layout is different from data.')

        if isinstance(fixed_type, fields.CompositeField):
            values = _parse_composite(fixed_type, value)
            setattr(instance, name, values)
        else:
            setattr(instance, name, fixed_type.encode(value))
        data = data[fixed_type.length:]
    return instance

def _parse_composite(fixed_type, value):
    if fixed_type.occurrences == 1:
        return parse(*fixed_type.encode(value))

    els = []
    for n in range(fixed_type.occurrences):
        els.append(parse(*fixed_type.encode(value)))
        value = value[fixed_type.size:]
    return els

