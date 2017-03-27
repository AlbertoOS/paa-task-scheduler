#!/usr/bin/python
# -*- encoding: utf-8 -*-
import random

def generate_activities(entries):
    activities = []
    for i in range(entries):
        begin = random.randint(0, entries - 1)
        end = random.randint(begin + 1, entries)
        activities.append((begin, end))

    filename = 'input' + str(entries) + '.txt'
    with open(filename, 'w') as f:
        for begin, end in activities:
            f.write('%s %s\n' % (begin, end))


entries_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
for entries in entries_list:
    generate_activities(entries)
