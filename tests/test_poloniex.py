import unittest
from poloniex import Poloniex

from datetime import date, timedelta, datetime

class TestPoloniex(object):

    def setup(self):
        self.poloniex = Poloniex('', '')

    def test_ticker(self):
        res = self.poloniex.returnTicker()

        assert 'BTC_ETH' in res.keys()
        assert 'lowestAsk' in res['BTC_ETH'].keys()

    def test_volume(self):
        res = self.poloniex.return24hVolume()

        assert 'BTC_ETH' in res.keys()
        assert 'BTC' in res['BTC_ETH'].keys()

    def test_orderbook(self):
        res = self.poloniex.returnOrderBook('BTC_ETH')
        assert 'bids' in res.keys()
        assert 'asks' in res.keys()

    def test_tradehistory(self):
        start = datetime.now() - timedelta(hours=1)
        res = self.poloniex.returnTradeHistory('BTC_ETH', start)

        assert len(res)
        assert 'date' in res[0].keys()
        assert 'type' in res[0].keys()
        assert 'amount' in res[0].keys()
        assert 'rate' in res[0].keys()

    def test_chartdata(self):
        start = datetime.now() - timedelta(hours=1)
        res = self.poloniex.returnChartData('BTC_ETH', 300, start)

        assert len(res)
        assert 'date' in res[0].keys()
        assert 'volume' in res[0].keys()
        assert 'high' in res[0].keys()
        assert 'low' in res[0].keys()
        assert 'close' in res[0].keys()
