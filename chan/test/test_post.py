#!/usr/bin/env python

import unittest
from itertools import izip

from chan.post import Post


class PostTest(unittest.TestCase):

    def setUp(self):
        self.base = {'no': '123'}
        self.match = {'no': '123'}
        self.different = {'no': '12'}
        self.auxiliary1 = {'no': '45'}
        self.auxiliary2 = {'no': '834'}

        self.base_post = Post(**self.base)

    def test_equality(self):
        new_post = Post(**self.match)

        self.assertEqual(self.base_post, new_post)

    def test_inequality(self):
        new_post = Post(**self.different)

        self.assertNotEqual(self.base_post, new_post)

    def test_unmatching_object(self):
        self.assertNotEqual(self.base_post, 42)

    def test_set(self):
        s = set((Post(**self.base), Post(**self.match),
                Post(**self.different)))

        self.assertEqual(sum(1 for x in s), 2)
