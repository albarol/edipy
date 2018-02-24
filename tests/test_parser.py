# coding: utf-8

import os
from decimal import Decimal

import pytest

from edipy import fields, parser, exceptions

FIXTURES_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')

class Example(fields.EDIModel):
    identifier = fields.Integer(3)
    name = fields.String(10)
    date = fields.DateTime(8)
    value = fields.Decimal(8, 2)
    bank_identifier = fields.Integer(3)
    bank_name = fields.String(18)


class Group(fields.EDIModel):
    example1 = fields.Field(Example)
    example2 = fields.Field(Example)


def test_parse_example():
    line = '352NEDI      230220120000007194001BANCO EDI         '
    example = parser.parse(Example, line)
    assert example.identifier == 352
    assert example.name == "NEDI      "
    assert example.date == "23022012"
    assert example.value == Decimal("71.94")
    assert example.bank_identifier == 1
    assert example.bank_name == "BANCO EDI         "


@pytest.mark.parametrize('data', [
    ('352NEDI      230220120000007194001BANCO EDI'),
    ('352'),
])
def test_parse_example_with_wrong_layout(data):
    with pytest.raises(exceptions.WrongLayoutError):
        example = parser.parse(Example, data)


def test_parse_group():
    with open(FIXTURES_PATH + '/group.edi') as fd:
        group = parser.parse(Group, fd.read())

    example1 = group.example1
    assert example1.identifier == 352
    assert example1.name == "NEDI      "
    assert example1.date == "23022012"
    assert example1.value == Decimal("71.94")
    assert example1.bank_identifier == 1
    assert example1.bank_name == "BANCO EDI         "

    example2 = group.example2
    assert example2.identifier == 353
    assert example2.name == "VEDI      "
    assert example2.date == "23122018"
    assert example2.value == Decimal("881.94")
    assert example2.bank_identifier == 1
    assert example2.bank_name == "BANCOVEDI         "

