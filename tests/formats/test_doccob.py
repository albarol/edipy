# coding: utf-8

import os
from datetime import datetime, date, time

from edipy import parser
from edipy.formats.doccob import Doccob

FIXTURES_PATH = os.path.join(os.path.dirname(__file__), '../fixtures')


def test_parse_doccob_properly():
    with open(FIXTURES_PATH + '/doccob.edi') as f:
        doccob = parser.parse(Doccob, f.read())

    # assert interchange
    interchange = doccob.interchange
    assert interchange
    assert interchange.identifier == "000"
    assert interchange.sender_identifier == "12345678904321                     "
    assert interchange.recipient_identifier == "12345678901234                     "
    assert interchange.date == date(2016, 01, 27)
    assert interchange.time == time(15, 17)
    assert interchange.interchange == "COB270115170"
    assert not interchange.filler

    # assert document
    header = interchange.header[0]
    assert header
    assert header.identifier == "350"
    assert header.document_identifier == "COBRA270115170"
    assert not header.filler
