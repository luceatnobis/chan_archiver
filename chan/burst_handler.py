#!/usr/bin/env python


class BurstHandler(object):

    def __init__(self, ContentSet, DeferredSemaphore):
        """
        This is an object that:

            a) instantiates the Content object
            b) keeps track of the number of downloaded Content and
               Thumbnail objects
        """
        self.contents = ContentSet

        self.num_content = 0
        self.num_thumbnails = 0
        self.num_elements = len(self.contents)
