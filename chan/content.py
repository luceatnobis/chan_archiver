#!/usr/bin/env python

import os

from random import choice as choose
from twisted.internet import reactor

"""
A few words about the eventual layout of the files on the drive, as this
decision is bound to be made here. I have decided for a layout that looks like
this:

There will be a root_dir, its ~ per default. In root_dir there will be a
dump_dir, which serves to limit the entire dumping process in one
folder. The default for dump_dir is 4chan/. In this dump_dir there will be
olders for each board. If a board folder is not present when a thread from
the board is to be dumped, it will be created. We shall call this folder
board_dir, for example ~/4chan/wg.

A thread will be dumped into board_dir with a folder name of the respective
threads number. This will be the thread_dir, ~/4chan/wg/5764713.

Now, there are a few things that need to be stored here:

    a) the actual images
    b) the thumbnails
    c) the html
    d) the stylesheet
    e) the "top image" for style.

In thread_dir there will be an html/ folder, containing the html document, a
folder content/ for the image content, a folder thumbs/ for the thumbnails to
said content and a misc/ folder for everything else I can't think of at
the moment. The google javascript stuff will not be saved as there is
no purpose for it.

However, for conveniences sake, there will be symlinks from
thread_dir/html/content to thread_dir, so that content from a thread can be
accessed without much hassle and the program stays true to its archival idea.

root_dir and dump_dir can be specified in the 4chan.conf file at the
DirectorySettings section.

"""


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


"""
def content(protocol, board, filename, semaphore):
    return Content(protocol, board, filename, semaphore)
"""
