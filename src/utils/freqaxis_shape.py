import numpy as np

def freq_fr_time(t):
    """
    Forms a frequency axis to plot a frequency spectrum of the signal. Assumes spectrum to be computed by *fft* function

    :param t: time axis
    :return: frequency axis
    """
    t_range = np.max(t) - np.min(t)
    t_step = (t_range / (np.size(t) - 1));
    fa = np.arange(0, 0.5 / t_step + 0.5 / t_range, 1 / t_range)
    fb = np.arange(-0.5 / t_step - 1 / t_range, 0 - 1 / t_range, 1 / t_range)
    f = np.concatenate((fa, fb))
    return f


def corr_fr_time(t):
    """
    Forms a time axis to plot a correlation function results. Folds an original time axis into negative

    :param t: time axis
    :return: time axis which is symmetrical with respect to the time origin
    """
    tmax = np.max(t)
    tmin = np.min(t)
    t_range = tmax - tmin
    t_step = (t_range / (np.size(t) - 1));
    tb = np.arange(2 * tmin - tmax, tmin, t_step)
    tc = np.concatenate((tb, t))
    return tc


def corr_fr_halftime(t):
    """
    Forms a time axis to plot a correlation function results. Folds an original time axis into negative

    :param t: time axis
    :return: time axis which is symmetrical with respect to the time origin
    """
    tmax = np.max(t)
    tmin = np.min(t)
    t_range = tmax - tmin
    t_step = (t_range / (np.size(t) - 1));
    tb = np.arange(2 * tmin - tmax, tmin, t_step)
    tc = np.concatenate((tb, t))
    return tc[::2]
