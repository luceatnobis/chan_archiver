#!/usr/bin/env python

import unittest

from treq.client import HTTPClient

from twisted.internet import reactor
from twisted.internet.defer import Deferred, succeed
from twisted.internet.protocol import Protocol

from twisted.web import http_headers
from twisted.web.client import Agent

from twisted.test.proto_helpers import MemoryReactorClock


class StubHTTPProtocol(Protocol):
    """
    A protocol like L{HTTP11ClientProtocol} but which does not actually know
    HTTP/1.1 and only collects requests in a list.

    @ivar requests: A C{list} of two-tuples.  Each time a request is made, a
        tuple consisting of the request and the L{Deferred} returned from the
        request method is appended to this list.
    """
    def __init__(self):
        self.requests = []
        self.state = 'QUIESCENT'


    def request(self, request):
        """
        Capture the given request for later inspection.

        @return: A L{Deferred} which this code will never fire.
        """
        result = Deferred()
        self.requests.append((request, result))
        return result


class FakeReactorAndConnectMixin:
    """
    A test mixin providing a testable C{Reactor} class and a dummy C{connect}
    method which allows instances to pretend to be endpoints.
    """
    Reactor = MemoryReactorClock

    class StubEndpoint(object):
        """
        Endpoint that wraps existing endpoint, substitutes StubHTTPProtocol, and
        resulting protocol instances are attached to the given test case.
        """

        def __init__(self, endpoint, testCase):
            self.endpoint = endpoint
            self.testCase = testCase
            self.factory = _HTTP11ClientFactory(lambda p: None)
            self.protocol = StubHTTPProtocol()
            self.factory.buildProtocol = lambda addr: self.protocol

        def connect(self, ignoredFactory):
            self.testCase.protocol = self.protocol
            self.endpoint.connect(self.factory)
            return succeed(self.protocol)


    def buildAgentForWrapperTest(self, reactor):
        """
        Return an Agent suitable for use in tests that wrap the Agent and want
        both a fake reactor and StubHTTPProtocol.
        """
        agent = client.Agent(reactor)
        _oldGetEndpoint = agent._getEndpoint
        agent._getEndpoint = lambda *args: (
            self.StubEndpoint(_oldGetEndpoint(*args), self))
        return agent


    def connect(self, factory):
        """
        Fake implementation of an endpoint which synchronously
        succeeds with an instance of L{StubHTTPProtocol} for ease of
        testing.
        """
        protocol = StubHTTPProtocol()
        protocol.makeConnection(None)
        self.protocol = protocol
        return succeed(protocol)


    def buildAgentForWrapperTest(self, reactor):
        """
        Return an Agent suitable for use in tests that wrap the Agent and want
        both a fake reactor and StubHTTPProtocol.
        """
        agent = client.Agent(reactor)
        _oldGetEndpoint = agent._getEndpoint
        agent._getEndpoint = lambda *args: (
            self.StubEndpoint(_oldGetEndpoint(*args), self))
        return agent


class TestAgent(unittest.TestCase, FakeReactorAndConnectMixin):

    def test_agent(self):

        h = http_headers.Headers({'foo': ['bar']})

        agent = Agent(reactor)
        agent._getEndpoint = lambda *args: self

        agent.request("GET", "http://google.com",h , object())
