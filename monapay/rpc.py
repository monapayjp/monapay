# -*- coding: utf-8 -*-

from decimal import Decimal
from django.conf import settings
import bitcoinrpc

def make_rpc_connection():
    return bitcoinrpc.connect_to_remote(
        settings.MONACOIND_ADMIN_USER,
        settings.MONACOIND_ADMIN_PASSWORD,
        settings.MONACOIND_HOST,
        settings.MONACOIND_PORT)

def get_minconf(x):
    if x <= Decimal("10.0"):
        return 2
    elif x <= Decimal("50.0"):
        return 3
    elif x <= Decimal("100.0"):
        return 4
    elif x <= Decimal("200.0"):
        return 5
    else:
        return 6
