import numpy as np

def ssrg(init_reg, fb_reg,n_bits):

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
        shft_reg = np.roll(shft_reg,-1)
        shft_reg[0] = in1
        print('For i=',i1,'shift register:',shft_reg,'output:',x)
    return (x)
