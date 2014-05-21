#!/usr/bin/env python

import os
import pkgutil
import tempfile
import unittest

from twisted.internet import reactor
from twisted.internet.defer import DeferredSemaphore

from chan.post_producer import PostProducer
from chan.content import Content, Thumbnail

url = "https://boards.4chan.org/g/thread/546800873"
conf_str = pkgutil.get_data("chan.config", "4chan.conf")

b64_json = pkgutil.get_data("chan.test.files", "b64_json")
#json_str = pkgutil.get_data("chan.test.files", "json_old_dump")


class TestContent(unittest.TestCase):

    def setUp(self):
        """
        We need to get a content object, so we use the Post Producer which
        comes in handy for exactly this situation
        """
        self.p = PostProducer(b64_json)
        self.semaphore = DeferredSemaphore(2)
        
        self.tmpdir = tempfile.gettempdir()

        post_gen = iter(self.p.all_posts())
        self.example_post = next(post_gen)

        board_dir = "4chan_test/g/546800873"
        self.example_post['board'] = "g"
        self.example_post['protocol'] = "https"
        self.example_post['thread_dir'] = os.sep.join([
            self.tmpdir, board_dir])

        self.content = Content(self.example_post, self.semaphore)

    def test_build_url(self):
        target_url = "https://i.4cdn.org/g/1400320404136.jpg"
        self.assertEqual(target_url, self.content._build_url())

    def test_return_timestamp_filename(self):
        timestamp_filename = "1400320404136.jpg"
        self.assertEqual(
            self.content._return_timestamp_filename(), timestamp_filename)

    def test_return_original_filename(self):
        original_filename = "death grip.jpg"
        self.assertEqual(
            self.content._return_original_filename(), original_filename)
    
    def test_md5_match(self):
        body = pkgutil.get_data("chan.test.files", "1400320404136.jpg")
        self.assertTrue(self.content._return_md5_match(body))

    def test_return_full_path_tim(self):
        tim_path = self.content._return_full_path_tim()
        expected_path = os.sep.join(
            [self.tmpdir, "4chan_test/g/546800873/1400320404136.jpg"])

        self.assertEqual(tim_path, expected_path)

    # def test_return_full_path_

    def test_write_to_disk(self):
        pass

    '''
    def test_large_file(self):
        """
        This is so going to be deleted.
        """

        post  = self.example_post
        post['thread_dir'] = '/home/maddinw/4chan'

        c = Content(post, self.semaphore)

        # c.url = "http://96.8.113.201/c" # just a test file
        c.url = "https://i.4cdn.org/b/1400320404136.jpg"
        c.download()
        reactor.run()
    '''

class TestThumbnail(unittest.TestCase):

    def setUp(self):
        self.p = PostProducer(b64_json)
        self.example_post = next(iter(self.p.all_posts()))

        self.example_post['board'] = "g"
        self.example_post['protocol'] = "https"
        self.example_post['thread_dir'] = "test"

        self.thumb = Thumbnail(self.example_post, DeferredSemaphore(2))

    def test_build_url(self):
        url = "https://t.4dcn.org/1400320404136.jpg"
        built_url = self.thumb._build_url()
