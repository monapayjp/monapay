# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from monapay.rpc import make_rpc_connection

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        from_account = args[0]
        to_account = args[1]
        amount = float(args[2])
        conn = make_rpc_connection()
        conn.move(from_account, to_account, amount)
