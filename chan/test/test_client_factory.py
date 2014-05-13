#!/usr/bin/env python
# coding=utf-8


import re
import unittest

from twisted.internet import reactor

from treq.content import content
from chan.client_factory import ClientFactory


class TestClientFactory(unittest.TestCase):

    '''
    def test_instantiate_raw(self):
        """
        This will return an HTTPClient object without any additional
        capabilities; its being fed a standard Agent.
        """
        c = ClientFactory()
        self.assertIsNotNone(c)

    def test_instantiate_cookie(self):
        This will instantiate an HTTPClient capable of retrieving cookies
        from HTTP headers. The assertion will function on the existence of the
        _extractCookies method which is intrinsic to CookieAgents.
        c = ClientFactory(cookies=True)
        self.assertTrue(hasattr(c._agent, "_extractCookies"))

    def test_instantiate_tor(self):
        c = ClientFactory(tor=True)
        self.assertTrue(hasattr(c._agent, "proxyEndpoint"))

    def test_instantiate_socks(self):
        socks_host = "127.0.0.1"
        socks_port = 1234
        c = ClientFactory(socks=True, host=socks_host, port=socks_port)
        self.assertEqual(c._agent.proxyEndpoint._host, socks_host)
        self.assertEqual(c._agent.proxyEndpoint._port, socks_port)

    '''

    def test_test_all(self):
        """
        Here we will check the precedence of tor over socks, the cookie
        functionality and the ClientFactory in general.

        Basically, we will receive an object that is capsuled and wrapped
        multiple times around the original Agent created. This is why we need
        to many rounds of ._agent for the retrieval of truth values. For the
        moment, everything that matters is that c can be used like requests
        would be used.
        """

        c = ClientFactory(cookies=True, socks=True, host="192.168.1.4",
                          port=1234, tor=True)

        cookies = hasattr(c._agent, "_extractCookies")
        tor = hasattr(c._agent._agent, "proxyEndpoint")

        self.assertTrue(all((cookies, tor)))
