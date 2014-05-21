#!/usr/bin/env python

import json

from chan.post import Post, ImagePost


class PostProducer(object):

    def __init__(self, json_string, **kwargs):
        """
        This is a class that gives you access to certain sorts of classes,
        those in particular being:

            a)  all posts, dicts
            b)  all posts, wrapped in chan.post.Post
            c)  image posts, dicts
            d)  image_posts, wrapped in chan.post.ImagePost
        """
        self.decoded_json = json.loads(json_string)['posts']

        for post in self.decoded_json:
            post.update(kwargs)

    def all_posts(self):
        for post in self.decoded_json:
            yield post

    def n_posts(self, n):
        for i in xrange(n):
            yield self.all_posts()

    def all_posts_wrapped(self):
        for post in self.all_posts():
            yield Post(**post)

    def n_posts_wrapped(self, n):
        for i in xrange(n):
            yield self.all_posts_wrapped()

    def all_image_posts(self):
        for post in self.all_posts():
            if 'tim' not in post:
                continue
            yield post

    def n_image_posts(self, n):
        for i in xrange(n):
            yield self.all_image_posts()

    def all_image_posts_wrapped(self):
        for post in self.all_image_posts():
            yield ImagePost(**post)

    def n_image_posts_wrapped(self, n):
        for i in xrange(n):
            yield self.all_image_posts_wrapped()
