#!/usr/bin/python
import json


def load_file(filename):
    """ Generic Load Function """
    try:
        with open(filename) as json_data:
            data = json.load(json_data)
        return data
    except:
        return False


def dump_file(self, filename):
    """ Generic Dump to file functin """
    try:
        with open(filename, 'w') as outfile:
            json.dump(self, outfile)
    except:
        return False
