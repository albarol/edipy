# coding: utf-8

import pytest

from edipy import fields, validators, exceptions


@pytest.mark.parametrize('fixed_type, data', [
    (fields.Integer(1, validators=[validators.Range(1, 5)]), '1'),
    (fields.Integer(1, validators=[validators.MaxValue(3)]), '2'),
    (fields.Integer(1, validators=[validators.MinValue(1)]), '5'),
    (fields.String(5, validators=[validators.Regex(r"[0-9]+")]), '12345'),
    (fields.String(12, validators=[validators.Email()]), 'abc@mail.com'),
])
def test_using_validators(fixed_type, data):
    try:
        fixed_type.encode(data)
    except exceptions.ValidationError:
        pytest.fail(u"ValidationError should not be thrown")



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
    (fields.Integer(1, validators=[validators.MinValue(1)]), '0'),
    (fields.Integer(1, validators=[validators.MinValue(5)]), '4'),
])
def test_validate_min_value(fixed_type, data):
    with pytest.raises(exceptions.ValidationError):
        fixed_type.encode(data)


@pytest.mark.parametrize('fixed_type, data', [
    (fields.String(5, validators=[validators.Regex(r"[0-9]+")]), 'a123f'),
    (fields.String(5, validators=[validators.Regex(r"\d")]), 'abcde'),
    (fields.String(5, validators=[validators.Regex(r"[A-Z]{6}")]), 'ABCDE'),
])
def test_validate_regex(fixed_type, data):
    with pytest.raises(exceptions.ValidationError):
        fixed_type.encode(data)


def test_throws_exception_when_regex_is_invalid():
    with pytest.raises(ValueError):
        field = fields.String(5, validators=[validators.Regex(")")])


@pytest.mark.parametrize('fixed_type, data', [
    (fields.String(11, validators=[validators.Email()]), 'edimail.com'),
    (fields.String(11, validators=[validators.Email()]), 'edi@mailcom'),
])
def test_validate_email(fixed_type, data):
    with pytest.raises(exceptions.ValidationError):
        fixed_type.encode(data)


