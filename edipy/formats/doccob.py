# coding: utf-8

from edipy import fields, validators

class Interchange(fields.EDIModel):
    identifier = fields.Identifier("000")
    sender_identifier = fields.String(35, required=True, validators=[validators.Cnpj()])
    recipient_identifier = fields.String(35, required=True, validators=[validators.Cnpj()])
    date = fields.Date(6, "%d%m%y", required=True)
    time = fields.Time(4, "%H%M", required=True)
    interchange = fields.String(12, required=True)
    filler = fields.String(205, required=False)


#class Header(fields.EDIModel):



class Doccob(fields.EDIModel):
    interchange = fields.Register(Interchange)
