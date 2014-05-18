#!/usr/bin/env python

import pkgutil
import unittest

from chan.burst_handler import BurstHandler
from chan.post_producer import PostProducer

json_str = pkgutil.get_data("chan.test.files", "json_old_dump")


class TestBurstHandler(unittest.TestCase):

    def setUp(self):

        post = {
            'board': 'g',
            'protocol': 'https',
            'thread_dir': '/home/maddinw/4chan/'
        }
        self.p = PostProducer(json_str, **post)
