import os
import unittest
from datetime import date, timedelta, datetime
try:
    from urllib import HTTPError
except ImportError:
    from urllib2 import HTTPError


from poloniex import Poloniex


import httplib
httplib.debuglevel = 1
httplib.HTTPConnection.debuglevel = 1


import pdb


class TestPoloniexPrivate(unittest.TestCase):

    def setUp(self):
        apiKey = os.environ.get('API_KEY', False)
        apiSecret = os.environ.get('API_SECRET', False)

        if not apiKey or not apiSecret:
            self.skipTest('private keys not provided')

        self.poloniex = Poloniex(apiKey, apiSecret)

    def test_balances(self):
        res = self.poloniex.returnBalances()

        assert 'BTC' in res
        assert 'ETH' in res

        
class TestPoloniexPrivateWithoutToken(unittest.TestCase):

    def setUp(self):
        self.poloniex = Poloniex('', '')

    def test_exception(self):
        with self.assertRaises(HTTPError):
            self.poloniex.returnBalances()
