
import numpy as np
import numpy.fft as npfft
import scipy.signal as signal
import logging


def corr_td_single (x1,x2):
    c_12 = np.dot(x1,x2)
    return c_12


def corr_fd(x1,x2):
    logger = logging.getLogger(__name__)
    logger.debug("Numpy based correlation function called, using fft and ifft from numpy.fft")
    x1_f = npfft.fft(x1)
    x2_f = npfft.fft(x2)
    logger.debug("operand x1: %s, %s, %s", np.shape(x1_f), type(x1_f), np.max(x1_f))
    logger.debug("operand x2: %s, %s, %s", np.shape(x2_f), type(x2_f), np.max(x2_f))
    c_f = x1_f * np.conjugate(x2_f)
    logger.debug("result in freq-domain: %s, %s, %s", np.shape(c_f), type(c_f), np.max(c_f))
    c = npfft.ifft(c_f)
    logger.debug("result in time-domain after ifft: %s, %s, %s", np.shape(c), type(c), np.max(c))
    return c


def corr_CORR(x1,x2):
    c = signal.correlate(x1,x2,'full')
    return c
