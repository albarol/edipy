# coding: utf-8

from edipy import fields, exceptions


def parse(model, data):
    data = "".join(data.splitlines())
    model_fields = model._fields
    instance = model()
    for (name, fixed_type) in model_fields:

        if isinstance(fixed_type, fields.Register):
            els, parsed = _parse_register(fixed_type, data)
            setattr(instance, name, els)
        elif isinstance(fixed_type, fields.CompositeField):
            els, parsed = _parse_composite(fixed_type, data)
            setattr(instance, name, els)
        else:
            parsed = fixed_type.size
            setattr(instance, name, fixed_type.encode(data[0:parsed]))
        data = data[parsed:]
    return instance


def _parse_composite(fixed_type, value):
    if fixed_type.occurrences == 1:
        return (parse(*fixed_type.encode(value)), fixed_type.size)

    els = []
    parsed = 0
    while len(els) < fixed_type.occurrences:
        els.append(parse(*fixed_type.encode(value)))
        parsed += fixed_type.size
        value = value[fixed_type.size:]
    return (els, parsed)


def _parse_register(fixed_type, value):
    identifier = fixed_type.model._fields[0][1].identifier

    if fixed_type.max_occurrences == 1:
        if not value.startswith(identifier):
            if fixed_type.min_occurrences > 0:
                raise exceptions.RequiredFieldError()
            return (None, 0)
        return (parse(*fixed_type.encode(value)), fixed_type.size)

    els = []
    parsed = 0
    while len(els) < fixed_type.max_occurrences:
        if not value.startswith(identifier):
            if not len(els) >= fixed_type.min_occurrences:
                raise exceptions.RequiredFieldError()
            break
        els.append(parse(*fixed_type.encode(value)))
        parsed += fixed_type.size
        value = value[fixed_type.size:]
    return (els, parsed)
