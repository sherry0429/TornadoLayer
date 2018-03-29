# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
import ConfigParser


class ParseConf(object):

    @staticmethod
    def parse_for_all(conf_path):
        conf = ConfigParser.ConfigParser()
        conf.read(conf_path)
        sections = conf.sections()
        conf_dict = dict()
        for section in sections:
            conf_dict[section] = dict()
            options = conf.options(section)
            for option in options:
                val = conf.get(section, option)
                v= val.strip()
                if v == "True":
                    v = True
                elif v == "False":
                    v = False
                conf_dict[section][option] = v
        return conf_dict