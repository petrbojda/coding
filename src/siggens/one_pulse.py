"""
Module provides functions to generate single pulses of various shapes and parameters. Functions accept a time
axis as an input argument. It suppose to be a NumPy array containing a row of time values defining moments
of sampling. Returned is a baseband signal which is a NumPy array of the same length as the time axis
containing samples of the signal.
"""
import numpy as np


def rect_p(t, t_start, t_end):
    """
    Generates a single rectangular pulse

    :param t: time axis
    :param t_start: time of the leading edge of the pulse
    :param t_end: time of the trailing edge of the pulse
    :return: baseband signal

    **Example:**

    A single rectangular pulse which starts at the time 0.1 sec and stops at 0.3 sec.
    The sampling rate is 1 kHz :

    >>> import one_pulse as op
    >>> import numpy as np
    >>> Tsampl = 0.001
    >>> t = np.arange(0,1,Tsampl)
    >>> out_seq = op.rect_p(t,0.1,0.3)
    """

    p = ((t > t_start) & (t < t_end)) * 1
    return p


def sinc_p(t, t0, Tb):
    """
    Generates a single cardinal sin pulse

    :param t: time axis
    :param t0: center point of the pulse
    :param Tb: pulse width in term of inverted frequency bandwidth
    :return: baseband signal

    **Example:**

    A single sinc pulse with its maximum at the time 0.5 sec. Pulse width is 0.2 sec.
    The sampling rate is 1 kHz :

    >>> import one_pulse as op
    >>> import numpy as np
    >>> Tsampl = 0.001
    >>> t = np.arange(0,1,Tsampl)
    >>> out_seq = op.sinc_p(t,0.5,0.2)
    """

    p = np.sinc(np.pi * (t - t0) / Tb)
    return (p)


def rcos_p(t, t0, Tb, alpha):
    """
    Generates a single raised cosine pulse

    :param t: time axis
    :param t0: center point of the pulse
    :param Tb: pulse width in term of inverted frequency bandwidth
    :param alpha: roll-off factor, float values in between 0 and 1.
    :return: baseband signal

    **Example:**

    A single raised-cosine pulse with its maximum at the time 0.5 sec. Pulse width is 0.2 sec,
    roll-off factor 0.8. The sampling rate is 1 kHz :

    >>> import one_pulse as op
    >>> import numpy as np
    >>> Tsampl = 0.001
    >>> t = np.arange(0,1,Tsampl)
    >>> out_seq = op.sinc_p(t,0.5,0.2,0.8)
    """

    beta = alpha / Tb
    damp = np.cos(np.pi * beta * (t - t0)) / (1 - 4 * (beta * (t - t0)) ** 2)
    p = np.sinc(np.pi * (t - t0) / Tb) * damp
    return (p)
