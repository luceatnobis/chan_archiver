#!/usr/bin/env python

import os
import json
import mock
import shutil
import pkgutil
import unittest
from itertools import count

from chan import chanthread
from chan import threadcontainer

from twisted.trial.unittest import TestCase

json_str = pkgutil.get_data("chan.test.files", "json_old_dump")
url = "https://boards.4chan.org/b/thread/544035281"


class TestChanthread(TestCase):

    def setUp(self):
        thread_pool_nr = next(count())

        self.thread_container = threadcontainer.ThreadContainer()
        self.thread = chanthread.Thread(url, thread_pool_nr,
                                        self.thread_container, interval=30)

    def test_filter_url(self):
        self.thread._parse_thread_url(url)

        self.assertEquals(self.thread.protocol, "https")
        self.assertEquals(self.thread.board, "b")
        self.assertEquals(self.thread.chan_thread_id, "544035281")

    def test_build_json_url(self):
        target_str = "https://a.4cdn.org/b/thread/544035281.json"

        self.thread._parse_thread_url(url)
        result_json_url = self.thread._build_json_url()
        self.assertEquals(target_str, result_json_url)


class TestBuildFolderTree(unittest.TestCase):

    def setUp(self):
        """ Sets up the objects for the folder tree test """
        self.get_data_backup = pkgutil.get_data
        self.conf_str = (
            "[DirectorySettings]\n"
            "root_dir = ~\n"
            "dump_dir = 4chan_test"
            )

        self.root_dir_expanded = os.path.expanduser('~')
        m = mock.Mock(return_value=self.conf_str)
        pkgutil.get_data = m

        thread_pool_nr = next(count())

        self.thread_container = threadcontainer.ThreadContainer()
        self.thread = chanthread.Thread(url, thread_pool_nr,
                                        self.thread_container, interval=30)

    def tearDown(self):
        """
        Tears it all down
        """
        pkgutil.get_data = self.get_data_backup
        if os.path.exists(self.thread.effective_dump_dir):
            shutil.rmtree(self.thread.effective_dump_dir)

    def test_set_folders(self):
        """
        Here we test if _set_folders() sets the right folders for:

            a) root_dir
            b) dump_dir
            c) board_dir
            d) thread_dir
        """
        self.thread._set_folders()
        exp_str = self.root_dir_expanded + os.sep \
            + "/".join(("4chan_test", "b", "544035281"))

        self.assertEqual(self.thread.dump_dir, "4chan_test")
        self.assertEqual(self.thread.thread_dir, exp_str)

    def test_build_folder_tree(self):
        self.thread._set_folders()
        self.thread._build_folder_tree()

        for subfolders in self.thread.subfolders:
            full_path = self.thread.thread_dir + subfolders
            self.assertTrue(os.path.exists(full_path))
