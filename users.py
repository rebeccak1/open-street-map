#!/usr/bin/env python
import xml.etree.ElementTree as ET

"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!
The function process_map should return a set of unique user IDs ("uid")
"""


def get_user(element):
    return

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if 'uid' in element.attrib:
            users.add(element.get('uid'))

    return users