# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from monapay.rpc import make_rpc_connection

info_str = \
"""monacoind information:
    connections = {0}
    errors = {1}
    blocks = {2}
    paytxfee = {3}
    keypoololdest = {4}
    walletversion = {5}
    difficulty = {6}
    testnet = {7}
    version = {8}
    proxy = {9}
    protocolversion = {10}
    timeoffset = {11}
    balance = {12}
    mininput = {13}
    keypoolsize = {14}"""

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        conn = make_rpc_connection()
        info = conn.getinfo()
        print(info_str.format(
            info.connections,
            info.errors,
            info.blocks,
            info.paytxfee,
            info.keypoololdest,
            info.walletversion,
            info.difficulty,
            info.testnet,
            info.version,
            info.proxy,
            info.protocolversion,
            info.timeoffset,
            info.balance,
            info.mininput,
            info.keypoolsize))
