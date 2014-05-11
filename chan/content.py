#!o/usr/bin/env python

import os

import treq
#from treq.client import HTTPClient
from twisted.internet import reactor

from twisted.web.client import Agent


class Content(object):
    """
    Content is a class that, as you may have guessed, does something with
    content. Content is every media uploaded to 4chan, images, gifs, webm.

    This class, in particular, deals with downloading and storing content on the
    hard drive.

    Content is being downloaded with the Semaphore passed in the
    constructor. Each piece of content is also responsible for grabbing the
    associated thumbnail
    """

    def __init__(self, ImagePost, semaphore, httpclient=None):

        assert 'thread_dir' in ImagePost
        for k, v in ImagePost.iteritems():
            setattr(self, k, v)

        self.semaphore = semaphore

        """
        if httpclient is None:
            self.client = HTTPClient(Agent(reactor))
        else:
            self.client = httpclient # not callable, instantiated object ref!
        """
        
        self._for_abstraction()

    def _for_abstraction(self):
        self.subfolder = "content"
        self.url = self._build_url()

    def _build_url(self):
        url = "%s://i.4cdn.org/%s/%s%s" % (
            self.protocol, self.board, self.tim, self.ext)
        return str(url)

    def _download(self):
        d = self.semaphore.run(treq.get, self.url)
        d.addCallback(self._retrieve_headers)

    def _retrieve_headers(self, resp):
        d = resp.content()
        d.addCallback(self._retrieve_body)
        d.addErrback(self._download_failure)

    def _retrieve_body(self, resp):
        """
        After we have downloaded the content we will store it. I might use
        non-blocking file descriptors for that but I'll have to see how the API
        is working and if its even supported.
        """

    def _download_failure(self, failure):
        print failure

class Thumbnail(Content):

    def _for_abstraction(self):
        self.subfolder = "thumbs"

    def _build_url(self):
        """
        Return the url to the actual content to be fetched. The 
        """
        return "%s://t.4cdn.org/%s/i%s.jpg" % (
            self.protocol, self.board, self.tim)
