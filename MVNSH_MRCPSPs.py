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
    # makespan = 0
    start = time.time()
    while run <= runMax:
        s,f,order = initial_schedule2(d_im,P_prec,num_r,R_r,U_imr)
        makespan = max(f.flatten())
        if makespan == fBest:
            break
        else:
            ord_list = [o[0] for o in list(order.values())]
            feas_uni = swap([ord_list])

            u_s,u_f,u_makespan = modified_makespan(feas_uni[0],d_im,P_prec,num_r,R_r,U_imr)

            if u_makespan == fBest:
                break
            else:
                makespan = min(makespan, u_makespan)
                run += 1
    end = time.time()
    tspan = end-start
    return makespan, tspan
