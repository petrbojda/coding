import numpy as np
import csv

def main():
    init = np.array([1,1,1,0,0,1])
    fb = np.array([0,0,1,0,0,0])
    n_of_bits = 40

    write_csv(init,6,"../data/test_data.csv")

def write_csv(arr,nob,filename):
    with open (filename,'w',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('iteration','input_of_reg','output_of_reg'))
        for i1 in range (0,nob):
            writer.writerow((i1,1,arr[int(i1/2)]))
            writer.writerow((i1,0,arr[int(i1/2)]))


if __name__ == '__main__':
    main()
