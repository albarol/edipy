Validators
==========

A validator takes a value and raise ``ValidationError`` if it doesn`t meet some criteria.

Built-in validators
-------------------

.. autoclass:: edipy.validators.Range

.. autoclass:: edipy.validators.MaxValue

.. autoclass:: edipy.validators.MinValue

.. autoclass:: edipy.validators.Regex

.. autoclass:: edipy.validators.Email


How to extend
-------------

.. code-block:: python

    from edipy import validators, fields, exceptions, parser

    class MyValidator(validators.Validator):

        def validate(self, value):
            if value != "edi":
                raise exceptions.ValidationError(message=u"Value should be edi")
            return True


    class ValidatorExample(fields.EDIModel):
        data = fields.String(3, validators=[MyValidator()])

    try:
        data = 'aaa'
        example = parser.parse(ValidatorExample, data)
    except exceptions.ValidationError as e:
        print(e.message)
