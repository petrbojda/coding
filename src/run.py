#!/usr/bin/env python

import sys
sys.path.append("../src")

import numpy as np
import scipy.signal as signal
import logging
import logging.config
import matplotlib.pyplot as plt

from utils import freqaxis_shape as ut
from utils import csv_interfaces as csvi
from utils import setup as stp
from siggens import train_pulse as gen
from siggens import PRN_bitstreams as prn


# class NoLoggerConfiguration(Exception): pass

def main(setup_data):

    stp.logger_setup(setup_data["setup"])
    logger = logging.getLogger(__name__)
    logger.info("Main function started.")

    logger.debug("Coder configuration file %s", setup_data["cnf"])
    logger.debug("Setup configuration file %s", setup_data["setup"])
    logger.debug("Logger output file %s", setup_data["log"])
    logger.debug("Python files %s", setup_data["srcpy"])
    logger.debug("SSRG state output file %s", setup_data["data_state"])
    logger.debug("Coder PRN output file %s", setup_data["data_code"])

    analysis_setup_date = stp.analysis_cnf_file_parser(setup_data["cnf"])
    logger.debug("%s file read to setup analysis", setup_data["cnf"])




    ##################### code generator ###############################
    ssrg_init = analysis_setup_date["ssrg_init"]
    logger.debug("initial state of the ssrg, ssrg_init =  %s ", ssrg_init)
    ssrg_fb = analysis_setup_date["ssrg_fb"]
    logger.debug("feedback vector of the ssrg, ssrg_fb =  %s ", ssrg_fb)
    srm = prn.build_srm(ssrg_fb)
    logger.debug("srm matrix created, srm =  %s ", srm)

    n_of_bits = analysis_setup_date["code_period"] * analysis_setup_date["n_o_periods"]
    logger.debug("coder setup - binary sequence generator, number of generated bits %s ", n_of_bits)
    x = ssrg_init.T
    code = np.zeros(1)
    for i1 in range (1,n_of_bits):
        x = prn.proceed_ssrg_onestep(x, srm)
        csvi.write_csv(x, setup_data["data_state"], i1)
        csvi.write_csv(x[-1], setup_data["data_code"], i1)
        code = np.append(code,x[-1])
    logger.debug("coder run - binary sequence generated, number of bits %s ", code.size)

    #################### time related simulation ######################
    # t = np.arange(0, T_int, 1 / f_sampl)  # time axis
    # logger.debug("time axis created, length  %s samples", t.size)

    # f = ut.freq_fr_time (t)				# frequency axis
    tc = ut.corr_fr_time(t)  # correlation time axis
    # cd = prn.gold_seq(2, 6, 1)  # code

    tau = 1  # time acceleration factor
    Ts = 10e-3  # transmitted symbol interval
    Tstr = Ts * tau  # Nyquist's symbol interval
    td = 0  # initial delay of the sequence (time offset)

    # Time Domain
    # a1 = gen.rcos_tr(t, Tstr, td + Tstr / 2, x, Ts, 1.0)
    # a2 = gen.rcos_tr(t, Tstr, td + Tstr / 2, x, Ts, 0.5)
    # a3 = gen.rcos_tr(t, Tstr, td + Tstr / 2, x, Ts, 0.0)
    c = gen.rect_tr(t, Tstr, 0, td, x)

    # Correlate processor
    A1_c = signal.correlate(c, c, 'full')

    ##################### Plots ###########################
    f1 = plt.figure(1, figsize=(10, 15), dpi=300)

    #  Time domain
    f1ax1 = f1.add_subplot(311)
    f1ax1.plot(t, x, '-g', label='$h_{rcos}(t), \\beta = 1.0$')
    # f1ax1.plot(t, a2, '-b', label='$h_{rcos}(t), \\beta = 0.5$')
    # f1ax1.plot(t, a3, '-r', label='$h_{rcos}(t), \\beta = 0.0$')
    # f1ax1.plot(t, c, '-k', label='$h_{rect}(t)$')
    f1ax1.grid(True)
    lgd = f1ax1.legend(loc='upper right', bbox_to_anchor=(1.12, 1.35))
    plt.title('Pulse-shaped baseband signal, $\\tau_A = 1.0$, $\\tau_B = 0.6$, $\\tau_C = 0.3$', loc='left')
    f1ax1.set_ylabel('Baseband - voltage')
    f1ax1.axis([0, 0.15, -0.3, 1.3])

    f2 = plt.figure(2, figsize=(10, 15), dpi=300)

    #  Autocorrelated
    f2ax1 = f2.add_subplot(311)
    f2ax1.plot(tc, A1_c, '-g', label='$h_{rcos}(t), \\beta = 1.0$')
    # f2ax1.plot(tc, A2_c, '-b', label='$h_{rcos}(t), \\beta = 0.5$')
    # f2ax1.plot(tc, A3_c, '-r', label='$h_{rcos}(t), \\beta = 0.0$')
    # f2ax1.plot(tc, CC_c, '-k', label='$h_{rect}(t)$')
    f2ax1.grid(True)
    lgd = f2ax1.legend(loc='upper right', bbox_to_anchor=(1.05, 1.15))
    plt.title('Pulse-shaped Autocorrelated, $\\tau_A = 1.0$, $\\tau_B = 0.6$, $\\tau_C = 0.3$', loc='left')
    f2ax1.set_ylabel('Baseband - voltage')
    f2ax1.axis([-0.25, 0.25, -100, 253000])

    f1.savefig('gold_accelerated.eps', format='eps')
    f2.savefig('gold_accelerated_autocorr.eps', format='eps')
    # f3.savefig('gold_accelerated_crosscorr.eps', format='eps')
    # f4.savefig('gold_accelerated_fft.eps', format='eps')
    plt.show()






if __name__ == '__main__':
    setup_file = stp.parse_CMDLine()
    print (setup_file)
    setup_data = stp.setup_cnf_file_parser(setup_file)
    main(setup_data)
