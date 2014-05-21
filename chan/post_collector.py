#!/usr/bin/env python

"""
PostCollector is a class that simply collects posts. Its being used to record
all posts of a thread, regardless if a post was deleted or not. It only takes
a generator or a list of chan.post.Post objects to make things less finnicky.

It also needs to return an ordered list of the posts. For now I have settled
on a dictionary keeping track of the posts with the post number being the key
and the chan.post.Post object being the value. This has the advantage that I
can switch easily between ordered and unordered access.
"""


class PostCollector(object):

    def __init__(self):
        self.posts = dict()

    def add_to_collection(self, *args):
        """
        This takes a list of chan.post.Post objects and stores them in a
        dict to later enable sorting over the dict keys.
        """
        for i in args:
            assert hasattr(i, "no")
            if i.no in self.posts:
                continue
            self.posts[i.no] = i

    def return_ordered(self):
        """
        This is the result of quite a bit of thinking and brain twisting, but
        when coded out it will seem quite simple. Hopefully.
        """
        s_func = lambda (k, v): int(k)  # PEP 8 and stuff
        for k, v in sorted(self.posts.iteritems(), key=s_func):
            yield v
