#!/usr/bin/env python

import csv

def write_csv(m1, filename, iter):
    if iter == 1:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(('iteration', 'ssrg_state'))
            writer.writerow((iter, m1.T))
    else:
        with open (filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow((iter, m1.T))
