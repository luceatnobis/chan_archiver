#!/usr/bin/env python

import itertools

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from chan.chanthread import thread


class ThreadContainer(object):

    def __init__(self):
        self.loopingcalls = dict()
        self.restart_delay = 3
        self.count = itertools.count()

    def add_thread(self, thread_url, interval):
        thread_pool_nr = str(next(self.count))
        t = thread(thread_url, thread_pool_nr, self, interval=interval)
        t.start()

    def add_loopingcall(self, thread_ref):
        lc = LoopingCall(thread_ref.start)
        lc.start(thread_ref.interval, now=False)
        self.loopingcalls[thread_ref.thread_pool_nr] = lc

    def remove_loopingcall(self, thread_ref):
        if thread_ref.thread_pool_nr in self.loopingcalls:
            self.loopingcalls[thread_ref.thread_pool_nr].stop()
        if not any(lc.running for lc in self.loopingcalls.values()):
            reactor.stop()

    def restart_delayed(self, thread_ref):
        reactor.callLater(self.restart_delay, thread_ref.start)

def threadcontainer():
    return ThreadContainer()
