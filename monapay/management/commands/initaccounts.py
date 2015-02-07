# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from monapay.rpc import make_rpc_connection

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        conn = make_rpc_connection()
        accounts = conn.listaccounts(as_dict=True)
        account_names = [
            settings.PAYMENT_WALLET_ACCOUNT_NAME,
            settings.PAYMENT_FEE_ACCOUNT_NAME
        ]
        for account_name in account_names:
            if not account_name in accounts:
                address = conn.getnewaddress(account=account_name)
                print("create a new account '{0}'. address: {1}".format(
                    account_name, address))
