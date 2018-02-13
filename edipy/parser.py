# coding: utf-8

from collections import OrderedDict

from edipy import fields
from lark import Lark


def _token_to_int(ftype):
    return r'/[0-9]{{{size}}}/'.format(size=ftype.size)


def _token_to_string(ftype):
    return r'/[a-zA-Z0-9 ]{{{size}}}/'.format(size=ftype.size)

def _types_to_symbol(ftype):
    ftypes = {
        fields.String.__name__: _token_to_string,
        fields.Integer.__name__: _token_to_int,
        #fields.Decimal, r'/[0-9]{size}[0-9]{digits}/',
    }
    return ftypes[ftype.__class__.__name__](ftype)


def _build_grammar(model):
    model_name = model.__name__.lower()

    inner_fields = OrderedDict()
    for (name, ftype) in model._fields.iteritems():
        name = name.upper()
        inner_fields[name] = '{name} : {symbol}'.format(name=name.upper(), symbol=_types_to_symbol(ftype))

    grammar = ['{model} : {fields}'.format(model=model_name, fields=' '.join(inner_fields.keys()))]
    return (model_name, '\n'.join(grammar + [v for (k, v) in inner_fields.iteritems()]))



def parse(model, data):
    start, grammar = _build_grammar(model)
    lparser = Lark(grammar, start=start)
    return lparser.parse(data)
