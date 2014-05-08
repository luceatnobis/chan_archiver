#!/usr/bin/env python

import os

from random import choice as choose
from twisted.internet import reactor


class Content(object):

    def __init__(self, ImagePost, semaphore):

        # For the time being...
        for k, v in ImagePost.iteritems():
            setattr(self, k, v)

        self.json_content = ImagePost
        self.semaphore = semaphore

    def _build_url(self):
        return "%s://i.4cdn.org/%s/%s%s" % (
            self.protocol, self.board,
            self.tim, self.ext)


class Thumbnail(Content):

    def _build_url(self):
        """
        Return the url to the actual content to be fetched
        thumbnail_server = str(choose(range(3)))
        """
