#!/usr/bin/env python

import os

from treq.client import HTTPClient
from twisted.internet import reactor

from twisted.web.client import Agent


class Content(object):
    """
    Content is a class that, as you may have guessed, does something with
    content. Content is every media uploaded to 4chan, images, gifs, webm.

    Content is being downloaded with the deferred Semaphore passed in the
    constructor. Each piece of content is also responsible for grabbing the
    associated thumbnail
    """

    def __init__(self, ImagePost, semaphore, httpclient=None):

        assert 'thread_dir' in ImagePost
        for k, v in ImagePost.iteritems():
            setattr(self, k, v)

        if httpclient is None:
            self.client = HTTPClient(Agent(reactor))
        else:
            self.client = httpclient # not callable, instantiated object ref!

        self.semaphore = semaphore
        self._for_abstraction()

    def _for_abstraction(self):
        self.subfolder = "content"
        self.url = self._build_url()

    def _build_url(self):
        url = "%s://i.4cdn.org/%s/%s%s" % (
            self.protocol, self.board, self.tim, self.ext)
        return str(url)

    def start(self):
        self._download()

    def _download(self):
        #d = self.semaphore.run(self.client.get, self.url)
        d = self.client.get(self.url)
        d.addCallback(self._download_success)
        d.addErrback(self._download_failure)

    def _download_success(self, headers):
        print "Download success"

    def _download_failure(self, error):
        print dir(error.value)
        print error.value.reasons
        """
        if error.value.status == '404':
            print "Sorry, URL 404'd"
        """

class Thumbnail(Content):

    def _for_abstraction(self):
        self.subfolder = "thumbs"

    def _build_url(self):
        """
        Return the url to the actual content to be fetched. The 
        """
        return "%s://t.4cdn.org/%s/i%s.jpg" % (
            self.protocol, self.board, self.tim)
