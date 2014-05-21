#!/usr/bin/env python

import pkgutil
import unittest

from chan.post_producer import PostProducer


class TestBodyProducer(unittest.TestCase):

    def setUp(self):
        self.n = 4
        self.num_img_posts = 74
        self.num_all_posts = 190

        self.json_str = pkgutil.get_data("chan.test.files", "json_old_dump")
        self.p = PostProducer(self.json_str)

    def test_all_posts(self):
        calculated_posts = sum(1 for x in self.p.all_posts())
        self.assertEqual(self.num_all_posts, calculated_posts)

    def test_n_posts(self):
        returned_posts = sum(1 for x in self.p.n_posts(self.n))
        self.assertEqual(self.n, returned_posts)

    def test_all_posts_wrapped(self):
        returned_posts = sum(1 for x in self.p.all_posts_wrapped())
        self.assertEqual(self.num_all_posts, returned_posts)

    def test_n_posts_wrapped(self):
        returned_posts = sum(1 for x in self.p.n_posts_wrapped(self.n))
        self.assertEqual(returned_posts, self.n)

    def test_all_image_posts(self):
        calculated_posts = sum(1 for x in self.p.all_image_posts())
        self.assertEqual(self.num_img_posts, calculated_posts)

    def test_n_image_posts(self):
        calculated_posts = sum(1 for x in self.p.n_image_posts(self.n))
        self.assertEqual(self.n, calculated_posts)

    def test_all_image_posts_wrapped(self):
        calculated_posts = sum(1 for x in self.p.all_image_posts_wrapped())
        self.assertEqual(self.num_img_posts, calculated_posts)

    def test_n_image_posts_wrapped(self):
        calculated_posts = sum(1 for x in self.p.n_image_posts_wrapped(self.n))
        self.assertEqual(self.n, calculated_posts)

    def test_init_exception(self):
        self.json_str = "This is not decodable."
        with self.assertRaises(Exception):
            PostProducer(self.json_str)
