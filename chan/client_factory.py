#!/usr/bin/env python

from treq.client import HTTPClient

from twisted.internet import reactor
from twisted.web.client import Agent


class ClientFactory(object):

    # __new__ because its a factory, __init__ returns None """
    def __new__(self, agent=None, endpoint=None):
        """
        Returns a treq.client.HTTPClient object, I am not quite sure yet what
        exactly I need.
        """
        if agent is None:
            self.agent = Agent(reactor)
        else:
            self.agent = agent(reactor)  # must be callable

        self.client = HTTPClient(self.agent)
        return self.client
