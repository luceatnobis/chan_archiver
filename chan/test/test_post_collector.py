#!/usr/bin/env python

import pkgutil
import unittest

from chan.post_producer import PostProducer
from chan.post_collector import PostCollector

json_old_dump = pkgutil.get_data("chan.test.files", "json_old_dump")
json_new_dump = pkgutil.get_data("chan.test.files", "json_new_dump")

json_missing_lower = pkgutil.get_data("chan.test.files", "json_missing_lower")
json_missing_upper = pkgutil.get_data("chan.test.files", "json_missing_upper")


class TestPostCollector(unittest.TestCase):

    def setUp(self):
        self.posts_nr_old_dump = 190
        self.posts_nr_new_dump = 231
        self.posts_nr_missing_dump_upper = 230  # duh

        self.producer_old = PostProducer(json_old_dump)
        self.producer_new = PostProducer(json_new_dump)
        self.producer_missing_upper = PostProducer(json_missing_upper)
        self.producer_missing_lower = PostProducer(json_missing_lower)

        self.old_gen = self.producer_old.all_posts_wrapped()
        self.new_gen = self.producer_new.all_posts_wrapped()
        self.missing_u_gen = self.producer_missing_upper.all_posts_wrapped()
        self.missing_l_gen = self.producer_missing_lower.all_posts_wrapped()

        self.collector = PostCollector()

    def test_simple_collection(self):
        self.collector.add_to_collection(*self.old_gen)

        nr_items = self._len_of_dict(self.collector.posts)
        self.assertEqual(self.posts_nr_old_dump, nr_items)

    def test_update_collection(self):
        self.collector.add_to_collection(*self.old_gen)
        self.collector.add_to_collection(*self.new_gen)

        nr_items = self._len_of_dict(self.collector.posts)
        self.assertEqual(self.posts_nr_new_dump, nr_items)

    def test_collection_deleted_missing_upper(self):
        self.collector.add_to_collection(*self.new_gen)
        self.collector.add_to_collection(*self.missing_u_gen)
    
        nr_items = self._len_of_dict(self.collector.posts)
        self.assertEqual(self.posts_nr_new_dump, nr_items)

    def test_collection_deleted_missing_lower(self):
        self.collector.add_to_collection(*self.old_gen)
        self.collector.add_to_collection(*self.missing_l_gen)

        nr_items = self._len_of_dict(self.collector.posts)
        self.assertEqual(self.posts_nr_new_dump, nr_items)

    def test_return_ordered(self):
        self.collector.add_to_collection(*self.new_gen)
        self.collector.return_ordered()

    def _len_of_dict(self, d):
        return len(d.keys())

