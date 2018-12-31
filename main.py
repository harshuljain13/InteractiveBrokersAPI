import argparse
import datetime
import collections
import inspect

import logging
import time
import os.path

from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper

# types
from ibapi.common import * # @UnusedWildImport
from ibapi.order_condition import * # @UnusedWildImport
from ibapi.contract import * # @UnusedWildImport
from ibapi.order import * # @UnusedWildImport
from ibapi.order_state import * # @UnusedWildImport
from ibapi.execution import Execution
from ibapi.execution import ExecutionFilter
from ibapi.commission_report import CommissionReport
from ibapi.ticktype import * # @UnusedWildImport
from ibapi.tag_value import TagValue

from ibapi.account_summary_tags import *

from ContractSamples import ContractSamples
from ibapi.scanner import ScanData


def printWhenExecuting(fn):
    def fn2(*args):
        print("   doing", fn.__name__)
        fn(*args)
        print("   done w/", fn.__name__)
    return fn2


class GeminiWrapper(wrapper.EWrapper):
    '''
    Wrapper class defines all methods used by TWS to communicate with the client.
    '''
    def __init__(self):
        wrapper.EWrapper.__init__(self)

class GeminiClient(EClient):
    '''
    client class contains all methods to communicate with IB.
    '''
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)


class GeminiApp(GeminiWrapper, GeminiClient):
    def __init__(self):
        GeminiWrapper.__init__(self)
        GeminiClient.__init__(self, wrapper=self)
        self.nKeybInt = 0
        self.started = False
        self.nextValidOrderId = None
        self.permId2ord = {}
        self.reqId2nErr = collections.defaultdict(int)
        self.globalCancelOnly = False
        self.simplePlaceOid = None

    @iswrapper
    def connectAck(self):
        if self.asynchronous:
            self.startApi()

    @iswrapper
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        logging.debug("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)
        self.start()

    def start(self):
        if self.started:
            return

        self.started = True

        if self.globalCancelOnly:
            print("Executing GlobalCancel only")
            self.reqGlobalCancel()
        else:
            self.tickDataOperations_req()

    @printWhenExecuting
    def tickDataOperations_req(self):
        self.reqMarketDataType(3)
        self.reqMktData(1000, ContractSamples.OptionAtBOX(), "", False, False, [])

    @iswrapper
    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float,
                  attrib: TickAttrib):
        super().tickPrice(reqId, tickType, price, attrib)
        print("TickPrice. TickerId:", reqId, "tickType:", tickType,
              "Price:", price, "CanAutoExecute:", attrib.canAutoExecute,
              "PastLimit:", attrib.pastLimit, end=' ')
        if tickType == TickTypeEnum.BID or tickType == TickTypeEnum.ASK:
            print("PreOpen:", attrib.preOpen)
        else:
            print()

    @printWhenExecuting
    def tickDataOperations_cancel(self):
        self.cancelMktData(1000)
    
    def keyboardInterrupt(self):
        self.nKeybInt += 1
        if self.nKeybInt == 1:
            self.stop()
        else:
            print("Finishing test")
            self.done = True

    def stop(self):
        self.tickDataOperations_cancel()

def main():
    app = GeminiApp()
    app.connect("127.0.0.1", 7497, clientId=0)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(), app.twsConnectionTime()))
    app.run()

if __name__ == '__main__':
    main()