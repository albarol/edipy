# coding: utf-8

import pytest

from edipy import fields, validators, exceptions


@pytest.mark.parametrize('fixed_type, data', [
    (fields.Integer(1, validators=[validators.Range(1, 5)]), '0'),
    (fields.Integer(1, validators=[validators.Range(1, 5)]), '6'),
])
def test_validate_range(fixed_type, data):
    with pytest.raises(exceptions.ValidationError):
        fixed_type.encode(data)


@pytest.mark.parametrize('fixed_type, data', [
    (fields.Integer(1, validators=[validators.MaxValue(1)]), '2'),
    (fields.Integer(1, validators=[validators.MaxValue(5)]), '6'),
])
def test_validate_max_value(fixed_type, data):
    with pytest.raises(exceptions.ValidationError):
        fixed_type.encode(data)


@pytest.mark.parametrize('fixed_type, data', [
    (fields.Integer(1, validators=[validators.MinValue(1)]), '2'),
    (fields.Integer(1, validators=[validators.MinValue(5)]), '6'),
])
def test_validate_min_value(fixed_type, data):
    with pytest.raises(exceptions.ValidationError):
        fixed_type.encode(data)


@pytest.mark.parametrize('fixed_type, data', [
    (fields.String(5, validators=[validators.Regex("[0-9]+")]), 'a123f'),
    (fields.String(5, validators=[validators.Regex("\d+")]), 'abcde'),
    (fields.String(5, validators=[validators.Regex("[A-Z]{6}")]), 'ABCDE'),
])
def test_validate_regex(fixed_type, data):
    with pytest.raises(exceptions.ValidationError):
        fixed_type.encode(data)


def test_throws_exception_when_regex_is_invalid():
    with pytest.raises(ValueError):
        field = fields.String(5, validators=[validators.Regex(")")])


@pytest.mark.parametrize('fixed_type, data', [
    (fields.String(30, validators=[validators.Email()]), 'edimail.com'),
    (fields.String(30, validators=[validators.Email()]), 'edi@mailcom'),
])
def test_validate_email(fixed_type, data):
    with pytest.raises(exceptions.ValidationError):
        fixed_type.encode(data)


