# coding: utf-8

from edipy import fields, validators

#doccob.interchange.header[0].shipping_company.charge_document.ctes[0].info
#doccob.interchange.header[0].invoice

class Header(fields.EDIModel):
    identifier = fields.Identifier("350")
    document_identifier = fields.String(14)
    filler = fields.String(283, required=False)


class Interchange(fields.EDIModel):
    identifier = fields.Identifier("000")
    sender_identifier = fields.String(35, validators=[validators.Cnpj()])
    recipient_identifier = fields.String(35, validators=[validators.Cnpj()])
    date = fields.Date(6, "%d%m%y")
    time = fields.Time(4, "%H%M")
    interchange = fields.String(12)
    filler = fields.String(205, required=False)
    header = fields.Register(Header, occurrences=2)


class ShippingCompany(fields.EDIModel):
    identifier = fields.Identifier("351")




class Doccob(fields.EDIModel):
    interchange = fields.Register(Interchange)
    #header = fields.Register(Header)
