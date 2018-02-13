# coding: utf-8

from edipy import fields
from edipy.parser import parse


class Doccob(fields.EDIModel):
    identifier = fields.String(3)
    remetente = fields.String(35)
    destinatario = fields.String(35)
    data = fields.Integer(6, zfill=True)
    hora = fields.Integer(4, zfill=True)
    exchange_identification = fields.String(12)
    #filler = fields.String(75)


def test_parse_line():
    line = '000L4B LOGISTICA LTDA                 Luxottica                          2812161618COB281216180'
    tree = parse(Doccob, line)
    assert 1 == 1

