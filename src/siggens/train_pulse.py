"""
Module provides sed are functions to generate trains of pulses of various shapes and parameters.
Used are functions which generate single pulses.
"""
import sys
sys.path.append("../../srcpy")

import numpy as np
import logging
from siggens import one_pulse as pulse

def rect_tr(t, tp, ts, td, code):
    """
    Generates a train of rectangular pulses using the *one_pulse* function -> ''rect_p''

    :param t: time axis
    :param tp: pulse width
    :param ts: spaces in between pulses
    :param td: time delay, time between origin of the t axis and the first pulse rising edge
    :param code: binary sequence which will be coded
    :return: baseband signal
    """
    logger = logging.getLogger(__name__)
    n = np.size(code)
    x = np.zeros(np.shape(t)) > 1
    logger.debug("code length %s ", n)
    logger.debug("oversampled signal length %s ", x.size)
    for i1 in range(0, n):
        p = pulse.rect_p(t, td + i1 * (tp + ts), td + tp + i1 * (tp + ts))
        # x = (x | p & code[i1]) * 1
        x = np.maximum(x, p * code[i1])
    return x

def sinc_tr(t, ts, td, code, pw):
    """
    Generates a train of cardinal sin pulses using the *one_pulse* function -> ''sinc_p''

    :param t: time axis
    :param ts: spaces in between pulses
    :param td: time delay, time between origin of the t axis and the center of the first pulse
    :param code: binary sequence which will be coded
    :param pw: pulse width
    :return: baseband signal
    """
    n = np.size(code)
    x = np.zeros(np.shape(t))
    for i1 in range(0, n):
        p = pulse.sinc_p(t, td + i1 * (ts), pw)
        # x = (x + p * code[i1])
        x = np.maximum(x, p * code[i1])
    return x

def rcos_tr(t, ts, td, code, pw, alpha):
    """
    Generates a train of raised cosine pulses using the *one_pulse* function -> ''rcos_p''

    :param t: time axis
    :param ts: spaces in between pulses
    :param td: time delay, time between origin of the t axis and the center of the first pulse
    :param code: binary sequence which will be coded
    :param pw: pulse width
    :param alpha: roll-off factor
    :return: baseband signal
    """
    n = np.size(code)
    x = np.zeros(np.shape(t))
    for i1 in range(0, n):
        p = pulse.rcos_p(t, td + i1 * (ts), pw, alpha)
        # x = (x + p * code[i1])
        x = np.maximum(x, p * code[i1])
    return (x)
