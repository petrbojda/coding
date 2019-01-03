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
from utils import analytic_plots as aplt
from siggens import train_pulse as gen
from siggens import PRN_bitstreams as prn
from dsp import corrNumpy as ncorr


# class NoLoggerConfiguration(Exception): pass

def main(setup_data):

    stp.logger_setup(setup_data["setup"])
    logger = logging.getLogger(__name__)
    logger.info("Main function started.")

    logger.debug("Coder analysis configuration file %s", setup_data["cnf"])
    logger.debug("Setup configuration file %s", setup_data["setup"])
    logger.debug("Plotting configuration file %s",setup_data["plt"])
    logger.debug("Logger output file %s", setup_data["log"])
    logger.debug("Python files %s", setup_data["srcpy"])
    logger.debug("SSRG state output file %s", setup_data["data_state"])
    logger.debug("Coder PRN output file %s", setup_data["data_code"])


    ##################### code generator ###############################
    analysis_setup = stp.analysis_cnf_file_parser(setup_data["cnf"])
    logger.debug("%s file read to setup analysis", setup_data["cnf"])
    ssrg_init = analysis_setup["ssrg_init"]
    logger.debug("initial state of the ssrg, ssrg_init =  %s ", ssrg_init)
    ssrg_fb = analysis_setup["ssrg_fb"]
    logger.debug("feedback vector of the ssrg, ssrg_fb =  %s ", ssrg_fb)
    srm = prn.build_srm(ssrg_fb)
    logger.debug("srm matrix created, srm =  %s ", srm)
    logger.debug("Number of bits in one period of the code N = %s bits ", analysis_setup["code_period"])
    logger.debug("Number of periods being generated %s ", analysis_setup["n_o_periods"])
    n_of_bits = analysis_setup["code_period"] * analysis_setup["n_o_periods"]
    logger.debug("code generator setup - number of generated bits %s ", n_of_bits)

    x = ssrg_init.T
    code = np.zeros(1)
    for i1 in range (1,n_of_bits):
        x = prn.proceed_ssrg_onestep(x, srm)
        csvi.write_csv(x, setup_data["data_state"], i1)
        csvi.write_csv(x[-1], setup_data["data_code"], i1)
        code = np.append(code,x[-1])
    logger.debug("coder run - binary sequence generated, number of bits %s ", code.size)

    #################### time related simulation ######################
    f_sampl = analysis_setup["chip_rate"] * analysis_setup["oversampling_factor"]
    logger.debug("sampling rate is %s kHz", f_sampl)
    logger.debug("sampling period is %s ms", 1/f_sampl)
    logger.debug("chiprate is %s kHz", analysis_setup["chip_rate"])
    Ts = 1/analysis_setup["chip_rate"] # transmitted symbol interval or a chip length
    logger.debug("chip length is %s ms", Ts)
    logger.debug("code period is %s ms", analysis_setup["code_period"] / analysis_setup["chip_rate"])
    T_int = analysis_setup["n_o_samples"] / f_sampl
    logger.debug("time axis  length  is %s ms", T_int)
    t = np.arange(0, T_int, 1 / f_sampl)  # time axis
    logger.debug("time axis created, length  %s samples", t.size)

    f = ut.freq_fr_time(t)				# frequency axis
    logger.debug("frequency axis for spectral analysis, length  %s", f.size)
    tc = ut.corr_fr_time(t)  # correlation time axis
    logger.debug("time axis correlation created, length  %s samples", tc.size)
    tc_h = ut.corr_fr_halftime(t)  # correlation time axis
    logger.debug("half time axis correlation created, length  %s samples", tc_h.size)

    tau = analysis_setup["time_accelerating_factor"]  # time acceleration factor
    logger.debug("time acceleration factor is %s", tau)
    Tstr = Ts * tau  # Nyquist's symbol interval
    logger.debug("Transmitted (accelerated) chip length is %s ms", Tstr)
    td = analysis_setup["time_offset"]  # initial delay of the sequence (time offset)
    logger.debug("Time offset (delay) of transmitted baseband signal is %s ms", td)

    # Time Domain Signals
    # a1 = gen.rcos_tr(t, Tstr, td + Tstr / 2, x, Ts, 1.0)
    # a2 = gen.rcos_tr(t, Tstr, td + Tstr / 2, x, Ts, 0.5)
    # a3 = gen.rcos_tr(t, Tstr, td + Tstr / 2, x, Ts, 0.0)
    c = gen.rect_tr(t, Tstr, 0, td, code)
    logger.debug("Oversampled signal with rectangular pulse shape created, number of samples %s", c.size)

    # Correlate processor
    c_con = np.concatenate((c,c))
    A1_c = ncorr.corr_fd(c, c, )
    # A1_c = signal.correlate(c, c_con, 'full', 'fft')
    # A1_c = signal.convolve(c, c, 'full')
    # A1_c = signal.fftconvolve(c, c, 'full')
    # A1_c = np.real(np.fft.ifft( np.fft.fft(c)*np.fft.fft(c) ))
    logger.debug("Autocorrelation function calculated, number of samples %s", A1_c.size)

    ##################### Plots ###########################
    plotting_setup = stp.plotting_cnf_file_parser(setup_data["plt"])
    logger.debug("%s file read to setup plotting results", setup_data["plt"])

    if plotting_setup["plotting"]:
        #  Time domain
        f1 = plt.figure(1, figsize=(10, 7), dpi=300)
        f1ax1 = f1.add_subplot(211)
        texts = {"y_legend": "$h_{rect}(t), \\beta = 1.0$",
                 "title": "Pulse-shaped time-domain baseband signal",
                 "y_label": "$prn(t)$",
                 "x_label": "time [ms]"}
        # figure_axes = [-0.25, 0.25, -100, 253000]
        aplt.timedomain_plot(f1ax1,t,c,texts=texts)

        #  Autocorrelated
        # f2 = plt.figure(2, figsize=(10, 7), dpi=300)
        # f2ax1 = f2.add_subplot(212)
        f1ax2 = f1.add_subplot(212)
        texts = {
                 # "y_legend": "$h_{rect}(t), \\beta = 1.0$",
                 # "title":"Pulse-shaped Autocorrelated",
                 "y_label":"$C_{xx}(\\tau)$",
                 "x_label":"time [ms]"}
        # figure_axes = [-0.25, 0.25, -100, 253000]
        tc_con = np.concatenate((tc,t))
        aplt.timedomain_plot(f1ax2, f, A1_c, texts=texts)

        if plotting_setup["show_plots"]:
            # f1.show()
            # f2.show()
            plt.show()

        if plotting_setup["save_plots"]:
            ssrg_time = setup_data["data_path"] + 'ssrgout_timedomain.' + plotting_setup["plot_saving_format"]
            ssrg_corr = setup_data["data_path"] + 'ssrgout_autocorr.' + plotting_setup["plot_saving_format"]
            f1.savefig(ssrg_time, format=plotting_setup["plot_saving_format"])
            # f2.savefig(ssrg_corr, format=plotting_setup["plot_saving_format"])


if __name__ == '__main__':
    setup_file = stp.parse_CMDLine()
    print (setup_file)
    setup_data = stp.setup_cnf_file_parser(setup_file)
    main(setup_data)
