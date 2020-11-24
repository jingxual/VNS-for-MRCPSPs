import re
import math
import copy
import random
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

import pdb

import 
path = "/content/gdrive/My Drive/635project/"


runMax=30
fBest=15

def MVNSH(runMax,fBest):
    run = 0
    # makespan = 0
    while run <= runMax:
        s,f,order = initial_schedule2(d_im,P_prec,num_r,R_r,U_imr)
        makespan = max(f.flatten())
        if makespan == fBest:
            break
        else:
            feas_uni = swap([order])

            u_s,u_f,u_makespan = modified_makespan(feas_uni[0],d_im,P_prec,num_r,R_r,U_imr)

            if u_makespan == fBest:
                break
            else:
                makespan = min(makespan, u_makespan)
                run += 1

    return makespan
