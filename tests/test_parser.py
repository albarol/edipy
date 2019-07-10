# coding: utf-8

import os
from datetime import datetime
from decimal import Decimal

import pytest

from edipy import fields, parser, exceptions

FIXTURES_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')

#######################
# Test simple fields
#######################

class Example(fields.EDIModel):
    identifier = fields.Identifier("352")
    name = fields.String(10)
    date = fields.DateTime(8, "%d%m%Y")
    value = fields.Decimal(8, 2)
    bank_identifier = fields.Integer(3)
    bank_name = fields.String(18)


def test_parse_example():
    line = '352NEDI      230220120000007194001BANCO EDI         '
    example = parser.parse(Example, line)
    assert example.identifier == "352"
    assert example.name == "NEDI      "
    assert example.date == datetime(2012, 2, 23)
    assert example.value == Decimal("71.94")
    assert example.bank_identifier == 1
    assert example.bank_name == "BANCO EDI         "


@pytest.mark.parametrize('data', [
    ('352NEDI      230220120000007194001BANCO EDI'),
    ('352'),
])
def test_parse_example_with_wrong_layout(data):
    with pytest.raises(exceptions.ValidationError):
        example = parser.parse(Example, data)


def test_parse_example_with_identifier():
    class ExampleIdentifier(fields.EDIModel):
        identifier = fields.Identifier("352")

    example = parser.parse(ExampleIdentifier, "352")
    assert example.identifier == "352"

    with pytest.raises(exceptions.ValidationError):
        parser.parse(ExampleIdentifier, "353")



#######################
# Test complex fields
#######################


class Group(fields.EDIModel):
    example1 = fields.Register(Example)
    example2 = fields.CompositeField(Example)

def test_parse_group():
    with open(FIXTURES_PATH + '/group.edi') as fd:
        group = parser.parse(Group, fd.read())

    example1 = group.example1
    assert example1.identifier == "352"
    assert example1.name == "NEDI      "
    assert example1.date == datetime(2012, 2, 23)
    assert example1.value == Decimal("71.94")
    assert example1.bank_identifier == 1
    assert example1.bank_name == "BANCO EDI         "

    example2 = group.example2
    assert example2.identifier == "352"
    assert example2.name == "VEDI      "
    assert example2.date == datetime(2018, 12, 23)
    assert example2.value == Decimal("881.94")
    assert example2.bank_identifier == 1
    assert example2.bank_name == "BANCOVEDI         "

#########################
# Test repeatable fields
#########################

class Repeatable(fields.EDIModel):
    example = fields.CompositeField(Example, occurrences=2)

def test_parse_repeatable():
    with open(FIXTURES_PATH + '/group.edi') as fd:
        group = parser.parse(Repeatable, fd.read())

    example1 = group.example[0]
    assert example1.identifier == '352'
    assert example1.name == "NEDI      "
    assert example1.date == datetime(2012, 2, 23)
    assert example1.value == Decimal("71.94")
    assert example1.bank_identifier == 1
    assert example1.bank_name == "BANCO EDI         "

    example2 = group.example[1]
    assert example2.identifier == '352'
    assert example2.name == "VEDI      "
    assert example2.date == datetime(2018, 12, 23)
    assert example2.value == Decimal("881.94")
    assert example2.bank_identifier == 1
    assert example2.bank_name == "BANCOVEDI         "
