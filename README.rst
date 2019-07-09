edipy
=====

**edipy** gives you a fancy way to read positional files by using declarative classes.

Examples
--------

```py
from edipy import fields, parser


class Example(fields.EDIModel):
    identifier = fields.Identifier("352")
    name = fields.String(10)
    date = fields.DateTime(8, "%d%m%Y")
    value = fields.Decimal(8, 2)
    bank_identifier = fields.Integer(3)
    bank_name = fields.String(18)


data = '352NEDI      230220120000007194001BANCO EDI         '
example = parser.parse(Example, data)

print(example.identifier) # "352"
print(example.name) # "NEDI      "
print(example.date) # datetime(2012, 02, 23)
print(example.value) # Decimal("71.94")
print(example.bank_identifier) # 1
print(example.bank_name) # "BANCO EDI         "
```
