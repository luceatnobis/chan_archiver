#!/usr/bin/env python

import os
import base64
import hashlib

from treq.content import content
from twisted.internet import threads

from chan.client_factory import ClientFactory


class Content(object):
    """
    Content is a class that, as you may have guessed, does something with
    content. Content is every media uploaded to 4chan, images, gifs, webm.

    This class, in particular, deals with downloading and storing content on
    the hard drive.

    Content is being downloaded with the Semaphore passed in the
    constructor. Each piece of content is also responsible for grabbing the
    associated thumbnail
    """

    def __init__(self, ImagePost, Semaphore, httpclient=None):

        # assert 'thread_dir' in ImagePost
        for k, v in ImagePost.iteritems():
            setattr(self, k, v)

        self.semaphore = Semaphore

        if httpclient is None:
            self.client = ClientFactory()
        else:
            self.client = httpclient

        self._for_abstraction()

    def _for_abstraction(self):
        self.subdir = "content"
        self.url = self._build_url()

        self.orig_filename = self._return_original_filename()
        self.time_filename = self._return_timestamp_filename()

    def _build_url(self):
        url = "%s://i.4cdn.org/%s/%s%s" % (
            self.protocol, self.board, self.tim, self.ext)
        return str(url)

    def _return_timestamp_filename(self):
        return str(self.tim) + self.ext

    def _return_original_filename(self):
        return self.filename + self.ext

    def download(self):
        """
        Here we will start the callback chain which downloads and stores the
        content.
        """
        d = self.semaphore.run(self.client.get, self.url)
        d.addCallback(self._retrieve_headers)
        d.addCallback(self._store_content)

    def _retrieve_headers(self, resp):
        """
        The body has received, putting us finally in control of what happens
        to a piece of 4chan content. Ideas for now involve storing the content
        in the self.subdir of thread_dir under the original filename, symlinked
        prinl self.thread_dir

        to thread_dir in the timestamp.ext and telling the BurstHandler that
        we're done with our one piece of content.
        """
        if resp.code == 404:
            """
            Here we will need to do something clever with the BurstHandler
            passed to this object in case we have had a bad day.
            """

        d = content(resp)
        return d
       
    def _store_content(self, body):
        if not self._return_md5_match(body):
            """
            Do something smart with BurstHandler
            """
            return
        
        #return threads.deferToThread(self.

    def _return_md5_match(self, body):
        """
        This function verifies that the md5sum from JsonContent matches the
        passed set of bytes.
        """
        assert hasattr(self, "md5")
        h = hashlib.md5(body)
        b64 = base64.b64decode(self.md5)

        return b64 == h.digest()

    def _create_symlinks(self):
        """
        This function creates the symlinks to thread_dir. However, this is not
        what we want to do with thumbnails.
        """

    def _write_to_disk(self, body):
        pass

    def _return_full_path_tim(self):
        return os.sep.join([
            self.thread_dir,
            self._return_timestamp_filename()])

    # def _return_full_path

    def __repr__(self):
        return "<Content: %s>" % self.url


class Thumbnail(Content):

    def _for_abstraction(self):
        self.subdir = "thumbs"

    def _build_url(self):
        """
        Return the url to the actual content to be fetched.
        """
        return "%s://t.4cdn.org/%s/i%s.jpg" % (
            self.protocol, self.board, self.tim)
