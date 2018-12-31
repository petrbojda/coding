"""
Functions of the module **Constallation Mapper** produce baseband signals
according to required passband modulations and shape of the pulse.

At this moment available choices are BPSK or QPSK modulations and three
different pulses - rectangular, sinus cardinale or raised cosine.

Returned *baseband* signals are numpy arrays of the same size as the time axis *t*.
"""
# import sys
# sys.path.append("../../srcpy")

import numpy as np
from siggens import train_pulse as gen

def rect_bpsk_map(t, data, b_rate, **args):
    """
    Generates a baseband signal for a BPSK modulation with rectangular pulses

    :param t: time axis
    :param data: binary sequence which is going to be mapped
    :param b_rate: bit rate of the transmitted bit-stream
    :param args: optional arguments, see the table.

    +----------+-------------+-----------+---------------------------------------------------+
    | Key word | Possible    | Default   | Description                                       |
    |          | values      |           |                                                   |
    +==========+=============+===========+===================================================+
    | tp       | positive    |           |  pulse width of a single symbol                   |
    |          | float       | 1/b_rate  |                                                   |
    +----------+-------------+-----------+---------------------------------------------------+
    | td       | positive    |           |  delay of the signal with reference to the origin |
    |          | float       |   0       |  of the time axis                                 |
    +----------+-------------+-----------+---------------------------------------------------+
    | ts       | positive    |   0       |  the space between pulses in a stream             |
    |          | float       |           |                                                   |
    +----------+-------------+-----------+---------------------------------------------------+

    :return: Baseband signal
    """
    if 'tp' in args:
        tp = args['tp']
    else:
        tp = 1 / b_rate  # pulse width of a single symbol

    if 'td' in args:
        td = args['td']
    else:
        td = 0  # signal starts at time td = 0s

    if 'ts' in args:
        ts = args['ts']
    else:
        ts = 0  # the space between pulses in a stream is ts = 0s

    # Baseband signal generator
    i_bb = 2 * gen.rect_tr(t, tp, ts, td, data) - 1
    q_bb = np.zeros(np.size(t))
    bb = i_bb + q_bb * 1j

    return (bb)


def rect_qpsk_map(t, data, s_rate, **args):
    """
    Generates a baseband signal to modulate with QPSK and rectangular pulses

    :param t: time axis
    :param data: binary sequence which is going to be mapped
    :param s_rate: symbol rate of the transmitted baseband signal
    :param args: optional arguments, see the table.

    +----------+-------------+-----------+---------------------------------------------------+
    | Key word | Possible    | Default   | Description                                       |
    |          | values      |           |                                                   |
    +==========+=============+===========+===================================================+
    | tp       | positive    |           |  pulse width of a single symbol                   |
    |          | float       | 1/b_rate  |                                                   |
    +----------+-------------+-----------+---------------------------------------------------+
    | td       | positive    |           |  delay of the signal with reference to the origin |
    |          | float       |   0       |  of the time axis                                 |
    +----------+-------------+-----------+---------------------------------------------------+
    | ts       | positive    |   0       |  the space between pulses in a stream             |
    |          | float       |           |                                                   |
    +----------+-------------+-----------+---------------------------------------------------+

    :return: Baseband signal
    """
    tup = 2  # number of bits in one tuple
    n_d = tup - (np.size(data) % tup)
    data = np.append(data, np.zeros(n_d))  # appends zero to get odd number of bits
    data_2s = data.reshape(-1, tup)  # reshaping the data vector into matrix
    data_2s = data_2s > 0

    ## Baseband signal parameters
    if 'tp' in args:
        tp = args['tp']
    else:
        tp = 1 / s_rate  # pulse width of a single symbol

    if 'td' in args:
        td = args['td']
    else:
        td = 0  # signal starts at time td = 0s

    if 'ts' in args:
        ts = args['ts']
    else:
        ts = 0  # the space between pulses in a stream is ts = 0s

    # Baseband signal generator
    i_bb = 2 * gen.rect_tr(t, tp, ts, td, data_2s[:, 0]) - 1
    q_bb = 2 * gen.rect_tr(t, tp, ts, td, data_2s[:, 1]) - 1
    bb = i_bb + q_bb * 1j

    return (bb)

# BPSK mapper 
def sinc_bpsk_map(t, data, b_rate, **args):
    """
    Generates a baseband signal to modulate with BPSK and sinc pulses

    :param t: time axis
    :param data: binary sequence which is going to be mapped
    :param b_rate: bit rate of the transmitted bit-stream
    :param args: optional arguments, see the table.

    +----------+-------------+-----------+---------------------------------------------------+
    | Key word | Possible    | Default   | Description                                       |
    |          | values      |           |                                                   |
    +==========+=============+===========+===================================================+
    | tp       | positive    |           |  pulse width of a single symbol                   |
    |          | float       | 1/b_rate  |                                                   |
    +----------+-------------+-----------+---------------------------------------------------+
    | td       | positive    |           |  delay of the signal with reference to the origin |
    |          | float       |   0       |  of the time axis                                 |
    +----------+-------------+-----------+---------------------------------------------------+
    | pw       | positive    | 1/b_rate  |  pulse width of the sinc - main lobe              |
    |          | float       |           |                                                   |
    +----------+-------------+-----------+---------------------------------------------------+

    :return: Baseband signal
    """
    if 'tp' in args:
        tp = args['tp']
    else:
        tp = 1 / b_rate  # pulse width of a single symbol

    if 'td' in args:
        td = args['td']
    else:
        td = 0  # signal starts at time td = 0s

    if 'pw' in args:
        pw = args['pw']
    else:
        pw = 1 / b_rate  # pulse width of the sinc - main lobe

    # Baseband signal generator
    i_bb = 2 * gen.sinc_tr(t, tp, td, data, pw) - 1
    q_bb = np.zeros(np.size(t))
    bb = i_bb + q_bb * 1j

    return (bb)

def sinc_qpsk_map(t, data, s_rate, **args):
    """
    Generates a baseband signal to modulate with QPSK and sinc pulses

    :param t: time axis
    :param data: binary sequence which is going to be mapped
    :param s_rate: symbol rate of the transmitted baseband signal
    :param args: optional arguments, see the table.

    +----------+-------------+-----------+---------------------------------------------------+
    | Key word | Possible    | Default   | Description                                       |
    |          | values      |           |                                                   |
    +==========+=============+===========+===================================================+
    | tp       | positive    |           |  pulse width of a single symbol                   |
    |          | float       | 1/b_rate  |                                                   |
    +----------+-------------+-----------+---------------------------------------------------+
    | td       | positive    |           |  delay of the signal with reference to the origin |
    |          | float       |   0       |  of the time axis                                 |
    +----------+-------------+-----------+---------------------------------------------------+
    | pw       | positive    | 1/b_rate  |  pulse width of the sinc - main lobe              |
    |          | float       |           |                                                   |
    +----------+-------------+-----------+---------------------------------------------------+

    :return: Baseband signal
    """
    tup = 2  # number of bits in one tuple
    n_d = tup - (np.size(data) % tup)
    data = np.append(data, np.zeros(n_d))  # appends zeros to get the proper shape
    data_2s = data.reshape(-1, tup)  # reshaping the data vector into matrix
    data_2s = data_2s > 0

    ## Baseband signal parameters
    if 'tp' in args:
        tp = args['tp']
    else:
        tp = 1 / s_rate  # pulse width of a single symbol

    if 'td' in args:
        td = args['td']
    else:
        td = 0  # signal starts at time td = 0s

    if 'pw' in args:
        pw = args['pw']
    else:
        pw = 1 / s_rate  # pulse width of the sinc - main lobe

    # Baseband signal generator
    i_bb = 2 * gen.sinc_tr(t, tp, td, data_2s[:, 0], pw) - 1
    q_bb = 2 * gen.sinc_tr(t, tp, td, data_2s[:, 1], pw) - 1
    bb = i_bb + q_bb * 1j

    return (bb)

def rcos_bpsk_map(t, data, b_rate, **args):
    """
    Generates a baseband signal to modulate with BPSK and raised cosine pulses

    :param t: time axis
    :param data: binary sequence which is going to be mapped
    :param b_rate: bit rate of the transmitted bit-stream
    :param args: optional arguments, see the table.

    +----------+-------------+-----------+---------------------------------------------------+
    | Key word | Possible    | Default   | Description                                       |
    |          | values      |           |                                                   |
    +==========+=============+===========+===================================================+
    | tp       | positive    |           |  pulse width of a single symbol                   |
    |          | float       | 1/b_rate  |                                                   |
    +----------+-------------+-----------+---------------------------------------------------+
    | td       | positive    |           |  delay of the signal with reference to the origin |
    |          | float       |   0       |  of the time axis                                 |
    +----------+-------------+-----------+---------------------------------------------------+
    | pw       | positive    | 1/b_rate  |  pulse width of the sinc - main lobe              |
    |          | float       |           |                                                   |
    +----------+-------------+-----------+---------------------------------------------------+
    | alpha    | positive    |   0.8     |  roll-off factor                                  |
    |          | float       |           |                                                   |
    +----------+-------------+-----------+---------------------------------------------------+

    :return: Baseband signal
    """
    if 'tp' in args:
        tp = args['tp']
    else:
        tp = 1 / b_rate  # pulse width of a single symbol

    if 'td' in args:
        td = args['td']
    else:
        td = 0  # signal starts at time td = 0s

    if 'pw' in args:
        pw = args['pw']
    else:
        pw = 1 / b_rate  # pulse width of the sinc - main lobe

    if 'alpha' in args:
        alpha = args['alpha']
    else:
        alpha = .8  # roll-off factor

    # Baseband signal generator
    i_bb = 2 * gen.rcos_tr(t, tp, td, data, pw, alpha) - 1
    q_bb = np.zeros(np.size(t))
    bb = i_bb + q_bb * 1j

    return (bb)

def rcos_qpsk_map(t, data, s_rate, **args):
    """
    Generates a baseband signal to modulate with QPSK and raised cosine pulses

    :param t: time axis
    :param data: binary sequence which is going to be mapped
    :param s_rate: symbol rate of the transmitted baseband signal
    :param args: optional arguments, see the table.

    +----------+-------------+-----------+---------------------------------------------------+
    | Key word | Possible    | Default   | Description                                       |
    |          | values      |           |                                                   |
    +==========+=============+===========+===================================================+
    | tp       | positive    |           |  pulse width of a single symbol                   |
    |          | float       | 1/b_rate  |                                                   |
    +----------+-------------+-----------+---------------------------------------------------+
    | td       | positive    |           |  delay of the signal with reference to the origin |
    |          | float       |   0       |  of the time axis                                 |
    +----------+-------------+-----------+---------------------------------------------------+
    | pw       | positive    | 1/b_rate  |  pulse width of the sinc - main lobe              |
    |          | float       |           |                                                   |
    +----------+-------------+-----------+---------------------------------------------------+
    | alpha    | positive    |   0.8     |  roll-off factor                                  |
    |          | float       |           |                                                   |
    +----------+-------------+-----------+---------------------------------------------------+

    :return: Baseband signal
    """
    tup = 2  # number of bits in one tuple
    n_d = tup - (np.size(data) % tup)
    data = np.append(data, np.zeros(n_d))  # appends zeros to get the proper shape
    data_2s = data.reshape(-1, tup)  # reshaping the data vector into matrix
    data_2s = data_2s > 0

    ## Baseband signal parameters
    if 'tp' in args:
        tp = args['tp']
    else:
        tp = 1 / s_rate  # pulse width of a single symbol

    if 'td' in args:
        td = args['td']
    else:
        td = 0  # signal starts at time td = 0s

    if 'pw' in args:
        pw = args['pw']
    else:
        pw = 1 / s_rate  # pulse width of the sinc - main lobe

    if 'alpha' in args:
        alpha = args['alpha']
    else:
        alpha = .8  # roll-off factor

    # Baseband signal generator
    i_bb = 2 * gen.rcos_tr(t, tp, td, data_2s[:, 0], pw, alpha) - 1
    q_bb = 2 * gen.rcos_tr(t, tp, td, data_2s[:, 1], pw, alpha) - 1
    bb = i_bb + q_bb * 1j

    return (bb)
