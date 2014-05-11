#!/usr/bin/env python

from treq.client import HTTPClient

from twisted.internet import reactor, ssl
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet.endpoints import TCP4ClientEndpoint

from twisted.web.client import readBody

from txsocksx.http import SOCKS5Agent
from txsocksx.tls import TLSWrapClientEndpoint

def foo(body):

    print body

def main():

    url = "http://google.com"

    factory = ssl.ClientContextFactory()
    factory.protocol = LineReceiver

    tor_endpoint = TCP4ClientEndpoint(reactor, '127.0.0.1', 9050)
    tls_endpoint = TLSWrapClientEndpoint(tor_endpoint, factory)

    socks_agent = SOCKS5Agent(reactor, proxyEndpoint=tor_endpoint)
    socks_client = HTTPClient(socks_agent)

    d = socks_client.get("http://wtfismyip.com/text")
    d.addCallback(readBody)
    d.addCallback(foo)

    reactor.run()

if __name__ == "__main__":
    main()
