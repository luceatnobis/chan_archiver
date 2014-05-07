#!/usr/bin/env python

import json

from chan import exceptions
from chan.post import Post, ImagePost

class PostProducer(object):
    """
    This is a class that gives you access to certain sorts of classes,
    those in particular being:

        a)  all posts
        b)  those with images

    To be continued...
    """

    def __init__(self, json_string, **kwargs):

        self.decoded_json = json.loads(json_string)['posts']

        for post in self.decoded_json:
            post.update(kwargs)

    def all_posts(self):
        for post in self.decoded_json:
            yield post

    def all_posts_wrapped(self):
        for post in self.all_posts():
            yield Post(**post)

    def posts_with_images(self):
        for post in self.all_posts():
            if 'tim' not in post:
                continue
            yield post

    def posts_with_images_wrapped(self):
        for post in self.posts_with_images():
            yield ImagePost(**post)
