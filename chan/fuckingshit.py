#!/usr/bin/env

from cookielib import CookieJar

from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent, CookieAgent

class HTTPProtocol(Protocol):

    def __init__(self):
        self.body = ""

    def dataReceived(self, bytes):
        print "Received data: %s" % bytes
        self.body += bytes

    def connectionLost(self,reason):
        return self.body


def main():

    agent = CookieAgent(Agent(reactor), CookieJar())

    d = agent.request("GET", "http://google.com")
    d.addCallback(success_callback)

    reactor.run()

def success_callback(response):

    print response.deliverBody(HTTPProtocol())
    reactor.stop()

if __name__ == "__main__":
    main()
