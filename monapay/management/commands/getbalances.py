# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from monapay.rpc import make_rpc_connection

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        conn = make_rpc_connection()
        balance = conn.listaccounts(as_dict=True)
        for key, value in balance.items():
            name = u"{empty}" if key == u"" else key
            print("{0}: {1}".format(name, value))
