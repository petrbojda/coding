"""
Module contains a set of functions which produce binary sequences either pseudo-random
or deterministic. Algorithms are developed based on the book *Spread Spectrum Systems for
GNSS and Wireless Communications* by Jack K. Holmes.

Returned binary sequences are numpy arrays of the type *bool*.
"""
import numpy as np
import logging

def build_srm(fb_vector):
    logger = logging.getLogger(__name__)
    logger.debug("build_srm function started.")
    srm = np.matrix(np.identity(fb_vector.size - 1))
    logger.debug("srm matrix , step 1 %s", srm)
    z = np.matrix(np.zeros(fb_vector.size -1))
    z = z.astype(int)
    logger.debug("srm matrix , step 2, append vector %s", z.T)
    srm = np.append(srm,z.T,axis=1)
    srm = np.append(fb_vector,srm,axis=0)
    return srm

# def proceed_ssrg_recursion(n,x,srm):
#     if n == 0 :
#         return int(x %2)
#     elif n == 1 :
#         return int(srm*x %2)
#     else:
#         return int(srm * proceed_ssrg_recursion(n-1,x,srm) %2)

def proceed_ssrg_np_pow(n,x,srm):
    a = ((srm**n) * x)%2
    return a.astype(int)

def proceed_ssrg_onestep(x,srm):
    out = (srm * x)%2
    return out.astype(int)


def ssrg(init_reg, fb_reg, **args):
    if 'n_bits' in args:
        n_bits = int(args['n_bits'])
    else:
        n_bits = 7

    if 'verbosity' in args:
        verbosity = bool(args['verbosity'])
    else:
        verbosity = False

    #  Output register
    x=np.zeros([n_bits])
    #  Shift register
    shft_reg = init_reg
    nob = len(shft_reg)
    #  Feedback registers - bit '1' means -> FB is connected
    #  defined as an input argument fb_reg
    for i1 in range (0,n_bits-1):
        in1 = int(np.dot(shft_reg,fb_reg)%2)
        x[i1] = shft_reg[nob-1]
        shft_reg = np.roll(shft_reg,1)
        shft_reg[0] = in1
        if verbosity:
            print('For i=',i1,'shift register:',shft_reg,'output:',x)
    return (x.astype(bool))

def gold_seq(x1, x2, **args):
    if 'verbosity' in args:
        verbosity = bool(args['verbosity'])
    else:
        verbosity = False

    if 'no_bits' in args:
        no_bits = int(args['no_bits'])
    else:
        no_bits = 1023

    if 'no_periods' in args:
        no_periods = int(args['no_periods'])
    else:
        no_periods = 1

    # Output register
    x = np.zeros([no_periods * no_bits])
    # Maximum-length sequence generators:
    #  Shift registers
    shft_reg_1 = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    shft_reg_2 = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    #  Feedback registers - bit '1' means -> FB is connected
    fbck_reg_1 = np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 1])
    fbck_reg_2 = np.array([0, 1, 1, 0, 0, 1, 0, 1, 1, 1])

    if verbosity == 1:
        print('G1: ', shft_reg_1, 'G2: ', shft_reg_2)

    for i1 in range(0, no_periods * no_bits):
        g1 = shft_reg_1[9]
        g2 = (shft_reg_2[x1 - 1] + shft_reg_2[x2 - 1]) % 2
        x[i1] = (g1 + g2) % 2

        in1 = np.dot(shft_reg_1, fbck_reg_1) % 2
        in2 = np.dot(shft_reg_2, fbck_reg_2) % 2

        shft_reg_1 = np.roll(shft_reg_1, 1)
        shft_reg_1[0] = in1

        shft_reg_2 = np.roll(shft_reg_2, 1)
        shft_reg_2[0] = in2

        # g1  = shft_reg_1 [9]
        # g2  = ( shft_reg_2[x1] + shft_reg_2[x2] ) % 2
        # x[i1] = ( g1 + g2 ) % 2

        if verbosity == 1:
            print('G1:', shft_reg_1, 'G2:', shft_reg_2, 'g2a:', shft_reg_2[x1], 'g2b:', shft_reg_2[x2], 'g2out:', g2,
                  'g1out:', g1, 'out:', x[i1])

    return (x.astype(bool))
