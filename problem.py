# -*- coding: utf-8 -*-
import os

def comment_cutter(s):
    t = s.find("#")
    if t < 0:
        return s
    else:
        return s[0:t].strip()

def show_variant(num, lines):
    print "Variant %s:" % num
    for l in file_pathes:
        print l
    print "------"

path_prefix = os.path.abspath(os.path.curdir)

#most simple approach
f = open("test.txt")
lines_stripped = map(lambda s: s.strip(), f)
lines_meaningful = filter(lambda s: len(s) > 0 and s[0:1] != "#", lines_stripped)
lines_clean = map(comment_cutter, lines_meaningful)
file_pathes = map(lambda s: os.path.join(path_prefix, s), lines_clean)
show_variant(1, file_pathes)

#list comprehensions + nested functions
file_pathes = map(lambda s: os.path.join(path_prefix, s),
                  map(comment_cutter,
                      filter(lambda s: len(s) > 0 and s[0:1] != "#",
                             [line.strip() for line in open("test.txt")])))
show_variant(2, file_pathes)

#lazy generator expressions
lines_stripped = (s.strip() for s in open("test.txt"))
lines_clean = (comment_cutter(s) for s in lines_stripped if len(s) > 0 and s[0:1] != "#")
file_pathes = (os.path.join(path_prefix, s) for s in lines_clean)
show_variant(3, file_pathes)

#functional composition
from composable import *
@composable
def empty_tester(x):
    return len(x) > 0 and x[0:1] != "#"

file_pathes = (c(open) >> c(str.strip).map >> c(comment_cutter).map >>
               empty_tester.filter >> c(os.path.join)[path_prefix, _].map)("test.txt")
show_variant(4, file_pathes)
