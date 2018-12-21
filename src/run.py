import numpy as np
import csv

def main():
    init = np.matrix('0;0;1')
    # fb = np.array([0,0,1,0,0,0])
    srm = np.matrix('0 1 1; 1 0 0; 0 1 0')
    n_of_bits = 300

    for i1 in range (1,n_of_bits):
        q_pow = proceed_ssrg_np_pow(i1, init, srm)
        q_rec = proceed_ssrg_recursion(i1, init, srm)
        write_csv(q_pow, q_rec, "../data/test_data.csv", i1)


def write_csv(m1, m2, filename, iter):
    if iter == 1:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(('iteration', 'm_power', 'recursion'))
            writer.writerow((iter, m1.T, m2.T))
    else:
        with open (filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow((iter, m1.T, m2.T))


def proceed_ssrg_recursion(n,x,srm):
    if n == 1 :
        return srm*x %2
    else:
        return srm * proceed_ssrg_recursion(n-1,x,srm) %2


def proceed_ssrg_np_pow(n,x,srm):
    a = srm**n
    return (a * x)%2


if __name__ == '__main__':
    main()
