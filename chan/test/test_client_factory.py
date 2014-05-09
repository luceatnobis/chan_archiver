#!/usr/bin/env python

import mock
import unittest

from treq.client import HTTPClient

from twisted.internet import reactor
from twisted.web.client import Agent

from chan.client_factory import ClientFactory


class TestClientFactoryInstantiate(unittest.TestCase):

    def test_raw(self):
        client = ClientFactory()

    def test_agent(self):
        client = ClientFactory(agent=Agent)
        d = client.get("http://google.com")
        d.addCallback(self._reactor_stop)
        #reactor.run()

    def _reactor_stop(self, result):
        reactor.stop()
