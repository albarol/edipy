# coding: utf-8

from edipy import fields, validators


class NotaFiscal(fields.EDIModel):
    registro_identificador = fields.Identifier("354")
    serie = fields.String(3, required=False)
    numero = fields.String(9)
    data_emissao = fields.Date(8, "%d%m%Y")
    peso = fields.Decimal(5, 2)
    valor = fields.Decimal(13, 2)
    cnpj_emissor = fields.String(14, validators=[validators.Cnpj()])
    filler = fields.String(241, required=False)


class Cte(fields.EDIModel):
    registro_identificador = fields.Identifier("353")
    filial_emissora = fields.String(14, validators=[validators.Cnpj()])
    serie_conhecimento = fields.String(3)
    numero_conhecimento = fields.String(9)
    valor_frete = fields.Decimal(13, 2)
    data_emissao = fields.Date(8, "%d%m%Y")
    cnpj_remetente = fields.String(14, required=False, validators=[validators.Cnpj()])
    cnpj_destinatario = fields.String(14, required=False, validators=[validators.Cnpj()])
    cnpj_emissor = fields.String(14, required=False, validators=[validators.Cnpj()])
    chave_acesso = fields.String(44)
    dominio = fields.String(50)
    chave_embarque = fields.String(50)
    icms = fields.Decimal(13, 2)
    filler = fields.String(47, required=False)
    notas_fiscais = fields.Register(NotaFiscal, occurrences=(0, 40))


class Cobranca(fields.EDIModel):
    registro_identificador = fields.Identifier("352")
    filial_emissora = fields.String(14, validators=[validators.Cnpj()])
    tipo_documento_cobranca = fields.Enum(['0','1'])
    serie_cobranca = fields.String(3)
    numero_documento = fields.String(10)
    data_emissao = fields.Date(8, "%d%m%Y")
    data_vencimento = fields.Date(8, "%d%m%Y")
    valor = fields.Decimal(13, 2)
    tipo_cobranca = fields.String(3)
    valor_icms = fields.Decimal(13, 2)
    valor_juros = fields.Decimal(13, 2, required=False)
    data_limite_pagamento = fields.Date(8, "%d%m%Y", required=False)
    valor_desconto = fields.Decimal(13, 2, required=False)
    agente_cobranca = fields.String(35, required=False)
    agencia_numero = fields.String(4, required=False)
    agencia_digito_verificador = fields.String(1, required=False)
    conta_corrente_numero = fields.String(10, required=False)
    conta_corrente_digito_verificador = fields.String(2, required=False)
    acao_documento = fields.Enum(['I'])
    identificador = fields.String(50, required=False)
    tipo_desconto = fields.Enum(['A', 'D'], required=False)
    filler = fields.String(78, required=False)
    ctes = fields.Register(Cte, occurrences=(1, 100))


class Transportadora(fields.EDIModel):
    registro_identificador = fields.Identifier("351")
    cnpj = fields.String(14, validators=[validators.Cnpj()])
    razao_social = fields.String(40)
    filler = fields.String(243, required=False)
    cobranca = fields.Register(Cobranca)


class Fatura(fields.EDIModel):
    registro_identificador = fields.Identifier("355")
    quantidade_docs_cobranca = fields.Integer(4)
    valor_total_docs_cobranca = fields.Decimal(13, 2)
    filler = fields.String(278, required=False)


class Cabecalho(fields.EDIModel):
    registro_identificador = fields.Identifier("350")
    identificacao_documento = fields.String(14)
    filler = fields.String(283, required=False)
    transportadora = fields.Register(Transportadora)
    fatura = fields.Register(Fatura)


class Intercambio(fields.EDIModel):
    registro_identificador = fields.Identifier("000")
    remetente = fields.String(35, validators=[validators.Cnpj()])
    destinatario = fields.String(35, validators=[validators.Cnpj()])
    data = fields.Date(6, "%d%m%y")
    hora = fields.Time(4, "%H%M")
    identificacao_intercambio = fields.String(12)
    filler = fields.String(205, required=False)
    cabecalhos = fields.Register(Cabecalho, occurrences=(1, 200))


class Doccob(fields.EDIModel):
    intercambio = fields.Register(Intercambio)
