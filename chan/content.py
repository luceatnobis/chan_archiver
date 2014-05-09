#!/usr/bin/env python

import os

from twisted.internet import reactor


class Content(object):
    """
    Content is a class that, as you may have guessed, does something with
    content. Content is every media uploaded to 4chan, images, gifs, webm.

    Content is being downloaded with the deferred Semaphore passed in the
    constructor. Each piece of content is also responsible for grabbing the
    associated thumbnail
    """

    def __init__(self, ImagePost, semaphore):

        assert 'thread_dir' in ImagePost
        for k, v in ImagePost.iteritems():
            setattr(self, k, v)

        self.semaphore = semaphore

    def _build_url(self):
        return "%s://i.4cdn.org/%s/%s%s" % (
            self.protocol, self.board, self.tim, self.ext)


class Thumbnail(Content):

    def _build_url(self):
        """
        Return the url to the actual content to be fetched. The 
        """
        return "%s://t.4cdn.org/%s/i%s.jpg" % (
            self.protocol, self.board, self.tim)
