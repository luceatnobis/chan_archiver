#!/usr/bin/env python
# test_content.py

import json
import pkgutil
import unittest

from chan.post import ImagePost
from chan.post_producer import PostProducer

json_str = pkgutil.get_data("chan.test.files", "json_old_dump")
json_new_str = pkgutil.get_data("chan.test.files", "json_new_dump")


class ImagePostTest(unittest.TestCase):

    def setUp(self):
        url = "https://boards.4chan.org/b/thread/544128809"
        self.element_count_old = 74
        self.element_count_new = 86

        self.set = set()
        self.json_old = json.loads(json_str)
        self.json_new_obj = json.loads(json_new_str)

        self.p = PostProducer(json_str)
        self.gen = self.p.all_image_posts()

    def test_decoding_success(self):
        self.assertIsInstance(self.json_old, dict)
        
    def test_settable(self):
        """
        This test tests (duh) whether we can make a set from ImagePost
        objects. We take the generator and create one object from it.
        """
        gen = iter(self.gen)
        jc = ImagePost(**next(gen))

        self.set.update([jc])
        self.assertEquals(str(next(iter(self.set))), "1398643849442.png")
        
    def test_set_of_posts(self):

        for json_post in self.gen:
            jc = ImagePost(**json_post)
            self.set.update([jc])

        self.assertEquals(len(self.set), self.element_count_old)

    def test_create_difference(self):

        len_of_difference = 12

        new_producer = PostProducer(json_new_str)
        old_set = set(self.p.all_image_posts_wrapped())
        new_set = set(new_producer.all_image_posts_wrapped())

        difference = new_set - old_set
        self.assertEqual(len(difference), len_of_difference)

    def test_create_difference_to_nullset(self):

        empty_set = set()
        self.set = set(self.p.all_image_posts_wrapped())

        diff = self.set - empty_set
        self.assertEqual(len(diff), len(self.set))

def main():
    unittest.main()

if __name__ == "__main__":
    main()
