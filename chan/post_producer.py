#!/usr/bin/env python

import json

from chan import exceptions
from chan.post import Post, ImagePost

"""
This is a class that gives you access to certain sorts of classes,
those in particular being:

a)  all posts, dicts
b)  all posts, wrapped in chan.post.Post
c)  image posts, dicts
d)  image_posts, wrapped in chan.post.ImagePost
"""


class PostProducer(object):

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
