#!/usr/bin/env python

import mock

import pkgutil
import unittest

from chan.post_producer import PostProducer

class TestBodyProducer(unittest.TestCase):

    def setUp(self):
        self.json_str = pkgutil.get_data("chan.test.files", "json_old_dump")

    def test_all_posts(self):
        num_of_posts = 190
        self.p = PostProducer(self.json_str)
        calculated_posts = sum(1 for x in self.p.all_posts())

        self.assertEqual(num_of_posts, calculated_posts)

    def test_image_posts(self):
        num_of_posts = 74
        self.p = PostProducer(self.json_str)
        calculated_posts = sum(1 for x in self.p.posts_with_images())

        self.assertEqual(num_of_posts, calculated_posts)

    def test_init_exception(self):
        self.json_str = "This is not decodable."
        with self.assertRaises(Exception):
            PostProducer(self.json_str)
