#!/usr/bin/env python

import pkgutil
import unittest

from twisted.internet.defer import DeferredSemaphore

from chan.content import Content
from chan.post_producer import PostProducer

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

        example_post['protocol'] = "https"
        example_post['board'] = "g"

        self.content = Content(example_post, DeferredSemaphore(2))

    def test_build_url(self):
        target_url = "https://i.4cdn.org/g/1398643849442.png"
        self.assertEqual(target_url, self.content._build_url())
