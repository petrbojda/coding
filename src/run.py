#!/usr/bin/env python

import numpy as np
import csv
import setup
import logging
import logging.config

class NoLoggerConfiguration(Exception): pass

def main(setup_data):

    print("Coder configuration file", setup_data["cnf"])
    print("Logger configuration file", setup_data["logcnf"])
    print("Logger output file", setup_data["log"])
    print("Python files", setup_data["srcpy"])
    print("SSRG state output file", setup_data["data_state"])
    print("Coder PRN output file", setup_data["data_code"])

    setup.logger_setup(setup_data["logcnf"],setup_data["log"])
    logger = logging.getLogger(__name__)
    logger.info("Main function started now.")

    init = np.matrix('1;0;0;0')
    # fb = np.array([0,0,1,0,0,0])
    srm = np.matrix('1 0 0 1; 1 0 0 0; 0 1 0 0; 0 0 1 0')
    n_of_bits = 190

    for i1 in range (1,n_of_bits):
        q_pow = proceed_ssrg_np_pow(i1, init, srm)
        q_rec = proceed_ssrg_recursion(i1, init, srm)
        write_csv(q_pow, q_rec, setup_data["data_state"], i1)


def write_csv(m1, m2, filename, iter):
    if iter == 1:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(('iteration', 'm_power', 'recursion'))
            writer.writerow((iter, m1.T, m2.T))
    else:
        with open (filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow((iter, m1.T, m2.T))


def proceed_ssrg_recursion(n,x,srm):
    if n == 0 :
        return x %2
    elif n == 1 :
        return srm*x %2
    else:
        return srm * proceed_ssrg_recursion(n-1,x,srm) %2


def proceed_ssrg_np_pow(n,x,srm):
    a = srm**n
    return (a * x)%2




if __name__ == '__main__':
    setup_file = setup.parse_CMDLine()
    print (setup_file)
    setup_data = setup.setup_file_parser(setup_file)
    main(setup_data)
