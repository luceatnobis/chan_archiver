#!/usr/bin/env python

import pkgutil
import cStringIO
import ConfigParser


"""
This is supposed to be a wrapper around the ConfigParser, which allows for
easier retrieval of config information.

"""


class ConfigReader(object):

    def __init__(self, config_files=None):
        self.config_parser = ConfigParser.ConfigParser()

        if config_files is None:
            self.config_files = ["4chan.conf"]  # , "shitnigga"]
        else:
            self.config_files = config_files

        self.config_dict = dict()
        self.config_contents = list()
        self.config_module = "chan.config"

        for f in self.config_files:
            try:
                conf = pkgutil.get_data(self.config_module, f)
            except IOError:
                # print "%s could not be found, skipping" % f
                continue

            self.config_contents.append(conf)

        if self.config_contents:
            self._parse()

    def _parse(self):
        for s in self.config_contents:
            io = cStringIO.StringIO(s)
            self.config_parser.readfp(io)

            for sec in self.config_parser.sections():
                self.config_dict[sec] = dict()
                self.config_dict[sec].update(self.config_parser.items(sec))

    def get_section_options(self, section):
        if section not in self.config_dict:
            return {}
        return self.config_dict[section]
