#!/usr/bin/env python

import mock
import pkgutil
import unittest

from chan import config_reader

test_data = ("[ArbitrarySection]\n"
             "this = is\n"
             "a = test\n"
             "[OtherArbitrarySection]\n"
             "again = another\n"
             "simple = test\n")

fail_dict = {}
success_dict = {'again': 'another', 'simple': 'test'}

class ConfigTestExistentFile(unittest.TestCase):

    def setUp(self):
        self.get_data = pkgutil.get_data
        get_data_mock = mock.Mock(return_value=test_data)
        pkgutil.get_data = get_data_mock
        self.config = config_reader.ConfigReader()

    def tearDown(self):
        pkgutil.get_data = self.get_data

    def test_read_test_config(self):
        res_dict = self.config.get_section_options('OtherArbitrarySection')
        self.assertDictEqual(res_dict, success_dict)

    def test_read_config_non_existent_section(self):
        res_dict = self.config.get_section_options('NoSuchSection')
        self.assertDictEqual(fail_dict, res_dict)

class ConfigTestNonExistentFile(unittest.TestCase):

    def setUp(self):
        self.config = config_reader.ConfigReader(config_files=["None"])

    def test_config_content(self):
        self.assertDictEqual(self.config.config_dict, {})
