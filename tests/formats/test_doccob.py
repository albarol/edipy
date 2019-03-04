# coding: utf-8

import os
from datetime import datetime, date, time
from decimal import Decimal

from edipy import parser
from edipy.formats.doccob import Doccob

FIXTURES_PATH = os.path.join(os.path.dirname(__file__), '../fixtures')


def test_parse_doccob_properly():
    with open(FIXTURES_PATH + '/doccob.edi') as f:
        doccob = parser.parse(Doccob, f.read())

    # assert interchange
    intercambio = doccob.intercambio
    assert intercambio
    assert intercambio.registro_identificador == "000"
    assert intercambio.remetente == "12345678904321                     "
    assert intercambio.destinatario == "12345678901234                     "
    assert intercambio.data == date(2016, 01, 27)
    assert intercambio.hora == time(15, 17)
    assert intercambio.identificacao_intercambio == "COB270115170"
    assert not intercambio.filler

    # assert document
    assert len(intercambio.cabecalhos) == 2
    cabecalho = intercambio.cabecalhos[0]
    assert cabecalho
    assert cabecalho.registro_identificador == "350"
    assert cabecalho.identificacao_documento == "COBRA270115170"
    assert not cabecalho.filler

    # assert shipping company
    transportadora = cabecalho.transportadora
    assert transportadora
    assert transportadora.registro_identificador == "351"
    assert transportadora.cnpj == "12345678901234"
    assert transportadora.razao_social == "Transportes Lages LTDA                  "

    # assert cobranca
    cobranca = transportadora.cobranca
    assert cobranca
    assert cobranca.registro_identificador == "352"
    assert cobranca.filial_emissora == "12345678901234"
    assert cobranca.tipo_documento_cobranca  == "0"
    assert cobranca.serie_cobranca  == "001"
    assert cobranca.numero_documento  == "1234567890"
    assert cobranca.data_emissao  == date(2016, 1, 27)
    assert cobranca.data_vencimento  == date(2016, 2, 7)
    assert cobranca.valor  == Decimal("0000000001000.10")
    assert cobranca.tipo_cobranca  == "B  "
    assert cobranca.acao_documento  == "I"

    # assert ctes
    assert len(cobranca.ctes) == 1
    cte = cobranca.ctes[0]
    assert cte
    assert cte.registro_identificador == "353"
    assert cte.chave_acesso == "31160112345678901234570010000003011000000008"
    assert cte.icms == Decimal('12.34')

    # assert nota
    assert len(cte.notas_fiscais) == 1
    nota_fiscal = cte.notas_fiscais[0]
    assert nota_fiscal
    assert nota_fiscal.data_emissao == date(2016, 2, 7)

    # assert fatura
    fatura = cabecalho.fatura
    assert fatura
    assert fatura.registro_identificador == "355"
    assert fatura.quantidade_docs_cobranca == 1
    assert fatura.valor_total_docs_cobranca == Decimal("1000.10")
