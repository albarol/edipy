# coding: utf-8

import pytest

from edipy import fields, validators, exceptions


@pytest.mark.parametrize('fixed_type, data', [
    (fields.String(3, validators=[validators.Required()]), ''),
    (fields.Integer(2, validators=[validators.Required()]), ''),
])
def test_validate_required(fixed_type, data):
    with pytest.raises(exceptions.ValidationError):
        fixed_type.encode(data)


@pytest.mark.parametrize('fixed_type, data', [
    (fields.Integer(1, validators=[validators.Range(1, 5)]), '0'),
    (fields.Integer(1, validators=[validators.Range(1, 5)]), '6'),
])
def test_validate_range(fixed_type, data):
    with pytest.raises(exceptions.ValidationError):
        fixed_type.encode(data)


@pytest.mark.parametrize('fixed_type, data', [
    (fields.String(30, validators=[validators.Email()]), 'edimail.com'),
    (fields.String(30, validators=[validators.Email()]), 'edi@mailcom'),
])
def test_validate_email(fixed_type, data):
    with pytest.raises(exceptions.ValidationError):
        fixed_type.encode(data)


@pytest.mark.parametrize('fixed_type, data', [
    (fields.String(30, validators=[validators.Cep()]), '950100100'),
    (fields.String(30, validators=[validators.Cep()]), '95010A10'),
    (fields.String(30, validators=[validators.Cep()]), '95010 10'),
])
def test_validate_cep(fixed_type, data):
    with pytest.raises(exceptions.ValidationError):
        fixed_type.encode(data)
