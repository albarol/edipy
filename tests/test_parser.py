# coding: utf-8

import pytest

from edipy import fields, parser, exceptions

class Example(fields.EDIModel):
    identifier = fields.Integer(3)
    name = fields.String(10)
    date = fields.DateTime(8)
    value = fields.Decimal(8, 2)
    bank_identifier = fields.Integer(3)
    bank_name = fields.String(18)


def test_parse_example():
    line = '352NEDI      230220120000007194001BANCO EDI        '
    example = parser.parse(Example, line)
    assert 1 == 1

def test_parse_example_with_wrong_layout():
    line = '352NEDI      230220120000007194001BANCO EDI               '
    with pytest.raises(exceptions.LayoutException):
        example = parser.parse(Example, line)
