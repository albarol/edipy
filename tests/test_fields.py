# coding: utf-8

from decimal import Decimal

import pytest

from edipy import fields


@pytest.mark.parametrize('fixed_type, value, expected', [
    (fields.String(1), 'ENCODE  ', 'E'),
    (fields.String(3), 'ENCODE  ', 'ENC'),
    (fields.String(8), 'ENCODE  ', 'ENCODE  '),
    (fields.String(8), '', None),

    (fields.Integer(1), '721', 1),
    (fields.Integer(2), '721', 21),
    (fields.Integer(3), '721', 721),
    (fields.Integer(1), '', None),

    (fields.Decimal(1), '721', Decimal('1.')),
    (fields.Decimal(2), '721', Decimal('21.')),
    (fields.Decimal(3), '721', Decimal('721.')),
    (fields.Decimal(1, 1), '7211', Decimal('1.1')),
    (fields.Decimal(2, 1), '7211', Decimal('21.1')),
    (fields.Decimal(3, 1), '7211', Decimal('721.1')),
    (fields.Decimal(1, 1), '7211', Decimal('1.1')),
    (fields.Decimal(1, 2), '7211', Decimal('2.11')),
    (fields.Decimal(1, 3), '7211', Decimal('7.211')),
    (fields.Decimal(1, 3), '', None),
])
def test_encode_data(fixed_type, value, expected):
    assert fixed_type.encode(value) == expected
