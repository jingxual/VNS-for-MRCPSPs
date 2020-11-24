import re
import math
import copy
import time
import random
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

import pdb

import data
import helpers
import shake
import init_schedules
import updated_schedules

path = "/content/gdrive/My Drive/635project/"

runMax=30
fBest=15

"""Main: whole procedures"""
def MVNSH(runMax,fBest):
    run = 0
    bestknown = []

    start = time.time()
    while run <= runMax:
        ss = time.time()
        print("Initializing...")
        s,f,order = initial_schedule2(d_im,P_prec,num_r,R_r,U_imr)
        makespan = max(f.flatten())
        if makespan == fBest:
            bestknown.append(makespan)
            break
        else:
            print("Shaking...")
            ord_list = [o[0] for o in list(order.values())]
            feas_uni = swap([ord_list])

            print("Local searching...")
            idx = random.randint(0,len(feas_uni)-1)
            feas_uni = feas_uni[idx]
            print(feas_uni)
            u_s,u_f,u_makespan = modified_makespan(feas_uni,d_im,P_prec,num_r,R_r,U_imr)

            if u_makespan == fBest:
                bestknown.append(u_makespan)
                break
            else:
                if u_makespan > fBest:
                    bestknown.append(min(makespan, u_makespan))
                    run += 1
        ee = time.time()
        print("[run]: ", run)
        print("[time]: ", ee-ss)
        print("makespan = ", min(bestknown))

    end = time.time()
    tspan = end-start
    print("total run: ", run)
    print("makespan: ", min(bestknown))
    print("total time: ", tspan)

    return min(bestknown), tspan

if __name__ == "__main__":
    MVNSH(runMax,fBest)
