
import numpy as np

def quad_mod(bb, t, f0, p0, pE, jtr):
    """
    Quadrature modulator.

    :param bb: baseband signal, complex
    :param t: time axis vector
    :param f0: carrier frequecy of real signal
    :param p0: starting phase of the LO signal (phase disbalance)
    :param pE:  phase error between LO and LO+pi/2 signals
    :param jtr: sampling jitter (percent of sample period)
    :return: passband signal modulated
    """

    # trange = np.max(t)-np.min(t);
    # tstep = (trange/(np.size(t)-1));
    # t_jitter = jtr*tstep/100 * randn(size(t));
    # t_noisy = t + t_jitter;

    t_noisy = t

    s_I = np.cos(2 * np.pi * f0 * t_noisy + p0);
    s_Q = np.sin(2 * np.pi * f0 * t_noisy + p0 + pE);

    x = np.real(bb) * s_I + np.imag(bb) * s_Q

    return (x)
