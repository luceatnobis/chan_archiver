#!/usr/bin/env python
# coding=utf-8


import re
import unittest

from twisted.internet import reactor

from treq.content import content
from chan.client_factory import ClientFactory


class TestClientFactory(unittest.TestCase):

    def setUp(self):
        
        self.socks_port = 1234
        self.socks_host = "127.0.0.1"
        
        self.tor_port = 9050
        self.tor_host = "127.0.0.1"

    def test_instantiate_raw(self):
        """
        This will return an HTTPClient object without any additional
        capabilities; its being fed a standard Agent.
        """
        c = ClientFactory()
        self.assertIsNotNone(c)

    def test_instantiate_cookie(self):
        """
        This will instantiate an HTTPClient capable of retrieving cookies
        from HTTP headers. The assertion will function on the existence of the
        _extractCookies method which is intrinsic to CookieAgents.
        """

        c = ClientFactory(cookies=True)
        self.assertTrue(hasattr(c._agent, "_extractCookies"))

    def test_instantiate_no_cookie(self):
        """
        This will check whether an Agent capable of SOCKS5 handling cookies.
        During coding there was a lot of trouble with this, just don't ask.
        """

        c = ClientFactory(tor=True)
        
        # Check if it has another _agent in it
        self.assertFalse(hasattr(self, "_agent"))

        # Check if the client has the proxyEndpoint property
        self.assertTrue(hasattr(c._agent, "proxyEndpoint"))

        # Check if it has the _extractCookies method
        self.assertFalse(hasattr(c._agent, "_extractCookies"))

    def test_instantiate_tor(self):
        c = ClientFactory(tor=True)
        self.assertTrue(hasattr(c._agent, "proxyEndpoint"))

    def test_instantiate_socks(self):
        """
        This tests whether the instantiation of the socks agent with custom
        parameters functions correctly.
        """
        c = ClientFactory(socks=True, host=self.socks_host, port=self.socks_port)
        self.assertEqual(c._agent.proxyEndpoint._host, self.socks_host)
        self.assertEqual(c._agent.proxyEndpoint._port, self.socks_port)


    def test_test_all(self):
        """
        Here we will check the precedence of tor over socks, the cookie
        functionality and the ClientFactory in general.

        Basically, we will receive an object that is capsuled and wrapped
        multiple times around the original Agent created. This is why we need
        to many rounds of ._agent for the retrieval of truth values. For the
        moment, everything that matters is that c can be used like requests
        object would be used.
        """

        c = ClientFactory(cookies=True, socks=True, host=self.socks_host,
                          port=self.socks_port, tor=True)

        cookies = hasattr(c._agent, "_extractCookies")
        tor = hasattr(c._agent._agent, "proxyEndpoint")

        # the agents do have all the necessary attributes
        self.assertTrue(all((cookies, tor)))

        # we check that the passed "host" and "port" values are not used
        # and the precedence of tor and its values works
        self.assertEqual(c._agent._agent.proxyEndpoint._port, self.tor_port)
        self.assertEqual(c._agent._agent.proxyEndpoint._host, self.tor_host)
