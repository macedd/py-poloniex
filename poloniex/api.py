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
import hmac, hashlib

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
            jsonRet = json.loads(ret.read().decode('utf-8'))

        if 'private' == type:
            post_data = bytes(urlencode(params), 'ascii')
            
            sign = hmac.new(bytes(self.Secret, 'ascii'), post_data, hashlib.sha512).hexdigest()
            headers ={
                'Sign': sign,
                'Key': self.APIKey
            }
            
            ret = urlopen(Request('https://poloniex.com/tradingApi', post_data, headers))
            jsonRet = json.loads(ret.read().decode('utf-8'))
            return self.post_process(jsonRet)
        
        if self.parseJson:
            return json.loads(ret.read().decode('utf-8'))
        else:
            return ret.read()

    def _private(self, command, params={}):
        params['command'] = command
        params['nonce'] = int(time.time())

        return self.api('private', params)

    def _public(self, command, params={}):
        params['command'] = command
        
        return self.api('public', params)

    def returnTicker(self):
        return self._public("returnTicker")
 
    def return24hVolume(self):
        return self._public("return24hVolume")
 
    def returnOrderBook (self, currencyPair="BTC_Dash"):
        return self._public("returnOrderBook", {'currencyPair': currencyPair})
 
    def returnTradeHistory (self, currencyPair='BTC_DASH', start=None, end=None):
        return self._public("returnTradeHistory", {
            'currencyPair': currencyPair,
            'start': createTimeStamp(start),
            'end': createTimeStamp(end)
        })
 
    def returnChartData (self, currencyPair='BTC_DASH', period=300, start=None, end=None):
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
    # success        1 or 0
    def cancel(self,currencyPair,orderNumber):
        return self._private('cancelOrder',{"currencyPair":currencyPair,"orderNumber":orderNumber})
 
    # Immediately places a withdrawal for a given currency, with no email confirmation. In order to use this method, the withdrawal privilege must be enabled for your API key. Required POST parameters are "currency", "amount", and "address". Sample output: {"response":"Withdrew 2398 NXT."}
    # Inputs:
    # currency      The currency to withdraw
    # amount        The amount of this coin to withdraw
    # address       The withdrawal address
    # Outputs:
    # response      Text containing message about the withdrawal
    def withdraw(self, currency, amount, address):
        return self._private('withdraw',{"currency":currency, "amount":amount, "address":address})
   
    ####################################
    # Margin Trading + Loan Management
    # Added by Luke Westfield

    # Returns current trading fees and trailing 30-day volume in BTC. Updated every 24 hours
    # Inputs:           None
    def returnFeeInfo(self):
        return self._private('returnFeeInfo')
        
    # Returns balances sorted by account. Balances in margin account may not be accessible if you have open margin positions or orders
    # Inputs:
    # account           Specific account to retrieve (optional, default=all)
    def returnAvailAccountBalances(self, account=None):
        return self._private('returnAvailableAccountBalances', {"account":account})
        
    # Returns your current tradable balances for each currency in each market for which margin trading is enabled
    # Inputs:           None
    def returnTradableBalances(self):
        return self._private('returnTradableBalances')
        
    # Transfers funds from account you specify to another (e.g. exchange account to margin account)
    # Required POST parameters: "currency", "amount", "fromAccount", "toAccount"
    # Inputs:
    # currency          Currency to transfer (e.g. BTC)
    # amount            Amount of currency to transfer (float)
    # fromAccount       Account moving currency from ("exchange", "margin", or "lending")
    # toAccount         Account moving currency to (same options as fromAccount)
    def transferBalance(self, currency, amount, fromAccount, toAccount):
        return self._private('transferBalance', {"currency": currency, "amount": amount, 
                                    "fromAccount": fromAccount, "toAccount":toAccount})
        
    # Returns a summary of entire margin account
    # Inputs:           None
    def returnMarginAccountSummary(self):
        return self._private('returnMarginAccountSummary')
    
    # Places margin buy order in a given market. Bitcoins spent(total) = rate of currencyPair * amount *(1+lendingRate)
    # Required POST parameters: "currencyPair", "rate", "amount", "lendingRate"
    # Inputs:
    # currencyPair      Specifies given market to enter margin position (e.g. BTC_XMR)
    # rate              Current rate of market (e.g. 0.03243)
    # amount            Amount to buy (in units of particular market currency))
    # lendingRate       Maximum lending rate (default=.02)
    def marginBuy(self, currencyPair, rate, amount, lendingRate=0.02):
        return self._private('marginSell', {"currencyPair": currencyPair, "rate":rate, "amount":amount, 
                                    "lendingRate":lendingRate})
    
    # Places margin sell order in a given market. Bitcoins spent(total) = rate of currencyPair * amount *(1+lendingRate)
    # Required POST parameters: "currencyPair", "rate", "amount", "lendingRate"
    # Inputs:
    # currencyPair      Specifies given market to sell margin position (e.g. BTC_XMR)
    # rate              Current price of market (e.g. 0.03243)
    # amount            Amount to sell (in BTC)
    # lendingRate       Maximum lending rate (default=.02)
    def marginSell(self, currencyPair, rate, amount, lendingRate=0.02):
        return self._private('marginSell', {"currencyPair": currencyPair, "rate":rate, "amount":amount, 
                                    "lendingRate":lendingRate})
    
    # Get margin position in a given market denoted by currencyPair. Required POST parameters: "currencyPair"
    # Inputs:
    # currencyPair      Specifies given market to get margin position (e.g. BTC_XMR) (default = all, returns all margin positions)
    def getMarginPosition(self,currencyPair='BTC_ETH'):
        return self._private('getMarginPosition',{"currencyPair" : currencyPair})

    # Closes margin position in a given market. Also returns success if you do not have an open position
    # Required POST parameters: "currencyPair"
    # Inputs:
    # currencyPair      Specifies given market to close margin position (e.g. BTC_XMR)
    def closeMarginPosition(self, currencyPair):
        return self._private('closeMarginPosition', {"currencyPair": currencyPair}) 
    
    # Creates a loan offer for a given currency. Required POST parameters: "currency", "amount", "duration", "lendingRate"
    # Inputs:
    # currency          Currency format of loan (e.g. BTC)
    # amount            Loan amount
    # duration          Number of days loan is active
    # autoRenew         Set to 1 if loan is to auto renew, 0 otherwise (default = 1)
    # lendingRate       Lending rate in decimal form (e.g. .02 for 2%)
    def createLoanOffer(self, currency, amount, duration, autoRenew=1, lendingRate=.02):
        return self._private('createLoanOffer', {"currency": currency, "amount":amount, "duration":duration,
                                    "autoRenew":autoRenew, "lendingRate":lendingRate})
        
    # Cancels a loan offer. Required POST parameter: "orderNumber"
    # Inputs: 
    # orderNumber       Order ID number of loan offer to cancel
    def cancelLoanOffer(self, orderNumber):
        return self._private('cancelLoanOffer', {"orderNumber": orderNumber})
    
    # Returns your open loan offers for each currency
    # Inputs            None
    def returnOpenLoanOffers(self):
        return self._private('returnOpenLoanOffers')
    
    # Return active loans for each currency
    # Inputs:           None
    def returnActiveLoans(self):
        return self._private('returnActiveLoans')
    
    # Returns lending history within a time specified. Required POST parameters: "start", "stop"
    # Inputs:
    # start             Start of time range of inquiry. UNIX timestamp format
    # stop              End of time range of inquiry. UNIX timestamp format
    # limit             Specified limit of rows to return (optional, default = 1)
    def returnLendingHistory(self, start=None, stop=None, limit=3):
        return self._private('returnLendingHistory', {"start": start, "stop": stop, "limit" : limit})   

    # Toggles the Auto Renew setting on an active loan. Required POST parameter: "orderNumber"
    # Inputs:
    # orderNumber       Order Number of Active Loan
    def toggleAutoRenew(self, orderNumber):
        return self._private('toggleAutoRenew', {"orderNumber": orderNumber})
    
    
    
    
    
    
    
    
    
