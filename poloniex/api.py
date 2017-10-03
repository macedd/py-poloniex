#
# Based on http://pastebin.com/8fBVpjaj
#

try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request
    from urllib import urlencode

import json
import time, datetime
from datetime import date, datetime
import calendar
import hmac,hashlib

def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    if type(datestr) in [date, datetime]:
        return calendar.timegm(datestr.timetuple())

    if datestr and type(datestr) is str:
        return time.mktime(time.strptime(datestr, format))

    return None

class Poloniex:
    def __init__(self, APIKey, Secret, parseJson=True):
        self.APIKey = APIKey
        self.Secret = Secret

        self.parseJson = parseJson

    def post_process(self, before):
        after = before

        # Add timestamps if there isnt one but is a datetime
        if('return' in after):
            if(isinstance(after['return'], list)):
                for x in xrange(0, len(after['return'])):
                    if(isinstance(after['return'][x], dict)):
                        if('datetime' in after['return'][x] and 'timestamp' not in after['return'][x]):
                            after['return'][x]['timestamp'] = float(createTimeStamp(after['return'][x]['datetime']))

        return after

    def api(self, type, params):
        try:
            params = dict((k,v) for k,v in params.iteritems() if v is not None)
        except AttributeError:
            params = dict((k,v) for k,v in params.items() if v is not None)

        if 'public' == type:
            uri = 'https://poloniex.com/public?' + urlencode(params)

            ret = urlopen(Request(uri))
            # jsonRet = json.loads(ret.read())

        if 'private' == type:
            post_data = urlencode(params)

            sign = hmac.new(self.Secret, post_data, hashlib.sha512).hexdigest()
            headers = {
                'Sign': sign,
                'Key': self.APIKey
            }

            ret = urlopen(Request('https://poloniex.com/tradingApi', post_data, headers))
            # jsonRet = json.loads(ret.read())
            # return self.post_process(jsonRet)

        if self.parseJson:
            return json.loads(ret.read().decode('utf-8'))
        else:
            return ret.read()

    def _private(self, command, params={}):
        params['command'] = command
        params['nonce'] = int(time.time()*1000)

        return self.api('private', params)

    def _public(self, command, params={}):
        params['command'] = command

        return self.api('public', params)

    def returnTicker(self):
        return self._public("returnTicker")

    def return24hVolume(self):
        return self._public("return24hVolume")

    def returnOrderBook (self, currencyPair):
        return self._public("returnOrderBook", {'currencyPair': currencyPair})

    def returnTradeHistory (self, currencyPair, start=None, end=None):
        return self._public("returnTradeHistory", {
            'currencyPair': currencyPair,
            'start': createTimeStamp(start),
            'end': createTimeStamp(end)
        })

    def returnChartData (self, currencyPair, period=300, start=None, end=None):
        return self._public("returnChartData", {
            'currencyPair': currencyPair,
            'start': createTimeStamp(start),
            'end': createTimeStamp(end),
            'period': period
        })


    # Returns all of your balances.
    # Outputs:
    # {"BTC":"0.59098578","LTC":"3.31117268", ... }
    def returnBalances(self):
        return self._private('returnBalances')

    # Returns your open orders for a given market, specified by the "currencyPair" POST parameter, e.g. "BTC_XCP"
    # Inputs:
    # currencyPair  The currency pair e.g. "BTC_XCP"
    # Outputs:
    # orderNumber   The order number
    # type          sell or buy
    # rate          Price the order is selling or buying at
    # Amount        Quantity of order
    # total         Total value of order (price * quantity)
    def returnOpenOrders(self,currencyPair):
        return self._private('returnOpenOrders',{"currencyPair":currencyPair})


    # Returns your trade history for a given market, specified by the "currencyPair" POST parameter
    # Inputs:
    # currencyPair  The currency pair e.g. "BTC_XCP"
    # Outputs:
    # date          Date in the form: "2014-02-19 03:44:59"
    # rate          Price the order is selling or buying at
    # amount        Quantity of order
    # total         Total value of order (price * quantity)
    # type          sell or buy
    def returnAccountTradeHistory(self,currencyPair):
        return self._private('returnTradeHistory',{"currencyPair":currencyPair})

    # Places a buy order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". If successful, the method will return the order number.
    # Inputs:
    # currencyPair  The curreny pair
    # rate          price the order is buying at
    # amount        Amount of coins to buy
    # Outputs:
    # orderNumber   The order number
    def buy(self,currencyPair,rate,amount):
        return self._private('buy',{"currencyPair":currencyPair,"rate":rate,"amount":amount})

    # Places a sell order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". If successful, the method will return the order number.
    # Inputs:
    # currencyPair  The curreny pair
    # rate          price the order is selling at
    # amount        Amount of coins to sell
    # Outputs:
    # orderNumber   The order number
    def sell(self,currencyPair,rate,amount):
        return self._private('sell',{"currencyPair":currencyPair,"rate":rate,"amount":amount})

    # Cancels an order you have placed in a given market. Required POST parameters are "currencyPair" and "orderNumber".
    # Inputs:
    # currencyPair  The curreny pair
    # orderNumber   The order number to cancel
    # Outputs:
    # succes        1 or 0
    def cancel(self, orderNumber):
        return self._private('cancelOrder', {"orderNumber":orderNumber})

    # Immediately places a withdrawal for a given currency, with no email confirmation. In order to use this method, the withdrawal privilege must be enabled for your API key. Required POST parameters are "currency", "amount", and "address". Sample output: {"response":"Withdrew 2398 NXT."}
    # Inputs:
    # currency      The currency to withdraw
    # amount        The amount of this coin to withdraw
    # address       The withdrawal address
    # Outputs:
    # response      Text containing message about the withdrawal
    def withdraw(self, currency, amount, address):
        return self._private('withdraw',{"currency":currency, "amount":amount, "address":address})
