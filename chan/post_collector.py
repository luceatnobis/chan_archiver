#!/usr/bin/env python

class PostCollector(object):

    def __init__(self):
        self.posts = dict()

    def add_to_collection(self, *args):
        """
        This takes a list of chan.post.Post objects and stores them in a
        dict to enable later sorting over the dict keys.
        """
        for i in args:
            if i.no in self.posts:
                continue
            self.posts[i.no] = i       

    def return_ordered(self):
        """
        This is the result of quite a bit of thinking and brain twisting, but
        when coded out it will seem quite simple. Hopefully.
        """
        sf = lambda (k, v): int(k)
        for k, v in sorted(self.posts.iteritems(), key=sf):
            print v
