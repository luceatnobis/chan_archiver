#!/usr/bin/env python

import itertools

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from chan.chanthread import thread

"""
ThreadContainer is a class that keeps track of all threads, whether registered
or not. The relationship between ThreadContainer and a Thread can be compared
to parents and their kids that have moved out. The Parent starts the Kids life
and after moving out, the kid could never be heard from again. The Thread will
only register if its not dead, 404'd, at the time of check. If its dead, it
will never be heard from again.

Likewise, a kid that moved out can only call its parents when it didn't die
in the gutter.
"""


class ThreadContainer(object):

    def __init__(self):
        self.restart_delay = 3
        self.loopingcalls = dict()
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
        """
        This is only until I figured out why sometimes an emptry response
        is received.
        """
        reactor.callLater(self.restart_delay, thread_ref.start)
"""
def threadcontainer():
    return ThreadContainer()
"""
