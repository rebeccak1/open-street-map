#!/usr/bin/env python
import xml.etree.ElementTree as ET

"""
Process the map file with iterative parsing to find what kinds of 
tags there are and how many. Outputs a dictionary where the keys
are the tag names and the values are how many times the tag is in
the map.
"""

def count_tags(filename):
    tag_count = {}
    for _, element in ET.iterparse(filename, events=("start",)):
        add_tag(element.tag, tag_count)
    return tag_count

def add_tag(tag, tag_count):
    if tag in tag_count:
        tag_count[tag] += 1
    else:
        tag_count[tag] = 1