#!/usr/bin/env python


from cookielib import CookieJar

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.web.client import Agent, CookieAgent

from treq.client import HTTPClient
from txsocksx.http import SOCKS5Agent


class ClientFactory(object):


    def __new__(self, cookies=None, socks=None, tor=None,
                host="127.0.0.1", port=9050):
        """
        Here we will check for some flags to be set. The calling instance can
        decide what sort of HTTPClient object it wants to have returned by
        specifying the capabilities that are required. For each set flag the
        according wrapper will be applied to the standard agent.
        """
        # TODO: add section to read tor configuration from config file

        tor_ip = "127.0.0.1"
        tor_port = 9050

        if tor or socks:

            if tor:
                tor_endpoint = TCP4ClientEndpoint(reactor, tor_ip, tor_port)
            else:
                tor_endpoint = TCP4ClientEndpoint(reactor, host, port)
            self.agent = SOCKS5Agent(reactor, proxyEndpoint=tor_endpoint)

        else:
            self.agent = Agent(reactor)
        self.agent = CookieAgent(self.agent, CookieJar())

        return HTTPClient(self.agent)
