Introduction
============

**edipy** came to help you to parse positional data easily. Just with a class declaration you can read texts and files.

Basic usage
-----------

With **edipy** you just need declare a class using `fields`_

.. code-block:: python

    from datetime import date
    from edipy import fields, parser

    class Example(fields.EDIModel):
        name = fields.String(5)
        date = fields.Date(8, '%Y%m%d')
        description = fields.String(7)
        likes = fields.Integer(4)

    data = 'EDIPY20190719AWESOME9999'
    example = parser.parse(Example, data)

    assert example.name == 'EDIPY'
    assert example.date ==  date(2019, 7, 19)
    assert example.description == 'AWESOME'
    assert example.likes == 9999


Installation
------------

You just need to install ``edipy`` library:

.. code-block:: sh

    pip install edipy


Complex models
--------------

If you need to read data according an specific format, such as `ANSI X12`_, you can create composed types.

.. code-block:: python

    from edipy import fields, parser

    class ISASegment(fields.EDIModel):
        identifier = fields.Identifier("ISA")
        content = fields.String(5)

    class GSSegment(fields.EDIModel):
        identifier = fields.Identifier("GS")
        content = fields.String(5)

    class ANSIX12(fields.EDIModel):
        isa = fields.Register(ISASegment, occurrences=1)
        gs = fields.Register(GSSegment, occurrences=2)

    data = 'ISA*100*\r\nGS*200*GS*300*'
    ansi = parser.parse(ANSIX12, data)

    assert ansi.isa.identifier == 'ISA'
    assert ansi.isa.content == '*100*'

    assert len(ansi.gs) == 2
    assert ansi.gs[0].identifier == 'GS'
    assert ansi.gs[0].content == '*200*'
    assert ansi.gs[1].content == '*300*'


Validators
----------

There are basic `validators`_ that you can use or extend to check if data is correct.

.. code-block:: python

    from edipy import fields, parser, validators, exceptions

    class User(fields.EDIModel):
        name = fields.String(10)
        age = fields.Integer(2, required=False, validators=[validators.MinValue(18)])
        email = fields.String(20, required=False, validators=[validators.Email()])

    try:
        data = 'Someone   17someone@net.com  '
        invalid_age = parser.parse(User, data)
    except exceptions.ValidationError as e:
        print("MinValue: {}".format(e.message))

    try:
        data = 'Someone   19someoneanet.com  '
        invalid_email = parser.parse(User, data)
    except exceptions.ValidationError as e:
        print("Email: {}".format(e.message))



.. _`fields`: fields.rst
.. _`validators`: validators.rst
.. _`ANSI X12`: https://en.wikipedia.org/wiki/ASC_X12
