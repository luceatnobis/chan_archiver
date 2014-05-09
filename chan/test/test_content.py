#!/usr/bin/env python

import pkgutil
import unittest

from twisted.internet.defer import DeferredSemaphore

from chan.post_producer import PostProducer
from chan.content import Content, Thumbnail

url = "https://boards.4chan.org/g/thread/544035281"
conf_str = pkgutil.get_data("chan.config", "4chan.conf")
json_str = pkgutil.get_data("chan.test.files", "json_old_dump")


class TestContent(unittest.TestCase):

    def setUp(self):
        """
        We need to get a content object, so we use the Post Producer which
        comes in handy for exactly this situation
        """
        self.p = PostProducer(json_str)

        post_gen = iter(self.p.all_posts())
        example_post = next(post_gen)

        example_post['board'] = "g"
        example_post['protocol'] = "https"
        example_post['thread_dir'] = ""

        self.content = Content(example_post, DeferredSemaphore(2))

    def test_build_url(self):
        # print self.content._build_url()
        target_url = "https://i.4cdn.org/g/1398643849442.png"
        self.assertEqual(target_url, self.content._build_url())

class TestThumbnail(unittest.TestCase):

    def setUp(self):
        self.p = PostProducer(json_str)
        example_post = next(iter(self.p.all_posts()))

        example_post['board'] = "g"
        example_post['protocol'] = "https"
        example_post['thread_dir'] = ""

        self.thumb = Thumbnail(example_post, DeferredSemaphore(2))

    def test_build_url(self):
        url = "https://t.4dcn.org/1398643849442s.jpg"
        built_url = self.thumb._build_url()
