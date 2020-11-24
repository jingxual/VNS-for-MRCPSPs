import re
import math
import copy
import time
import random
import numpy as np
import matplotlib.pyplot as plt

import pdb


"""
INPUTs
args: 
    M_i
    d_im
    P_prec
    r, R_r, U_imr
    nr, R_nr, U_imnr: default None
"""
# multi-mode
M_i = [1,2,3]

# renewable and nonrenewable resource type
num_r = [1,2]  # R1, R2
num_nr = None

# renewable and nonrenewable resource availability
# R_r = {0:9, 1:4}
R_r = [9,4]
R_nr = None

# renewable and nonrenewable resource requirement of activity i in mode m, either R1 or R2
U_imr ={1:{1:[0,0],2:[0,0],3:[0,0]},
        2:{1:[6,0],2:[5,0],3:[0,6]},
        3:{1:[0,4],2:[7,0],3:[0,2]},
        4:{1:[7,0],2:[6,0],3:[5,0]},
        5:{1:[0,9],2:[2,0],3:[0,5]},
        6:{1:[4,0],2:[0,8],3:[2,0]},
        7:{1:[5,0],2:[0,7],3:[4,0]},
        8:{1:[6,0],2:[3,0],3:[4,0]},
        9:{1:[4,0],2:[2,0],3:[1,0]},
        10:{1:[4,0],2:[0,2],3:[1,0]},
        11:{1:[0,2],2:[0,1],3:[0,1]},
        12:{1:[0,0],2:[0,0],3:[0,0]},}
U_imnr = None

# duration of activity i in mode m
d_im={1:{1:0,2:0,3:0},
      2:{1:3,2:9,3:10},
      3:{1:1,2:1,3:5},
      4:{1:3,2:5,3:8},
      5:{1:4,2:6,3:10},
      6:{1:2,2:4,3:6},
      7:{1:3,2:6,3:8},
      8:{1:4,2:10,3:9},
      9:{1:2,2:7,3:10},
      10:{1:1,2:1,3:9},
      11:{1:6,2:9,3:9},
      12:{1:0,2:0,3:0},}

# adjacent matrix: precedence relationships
# row for i, column for j, i happens before j
P_prec={1:[2,3,4],
        2:[5,6],
        3:[10,11],
        4:[9],
        5:[7,8],
        6:[11],
        7:[9,10],
        8:[9],
        9:[12],
        10:[12],
        11:[12],
        12:[12]}


"""Params"""
# sBest = 
fBest = 15
runMax = 30
tMax = 25

numI = 10                       # num of activities
I = [2,3,4,5,6,7,8,9,10,11]      # activities
# i = 1,2,...,11,11+1                # including start and end dummy nodes
A = [1,2,3,4,5,6,7,8,9,10,11,12] # the set of nodes


"""helpers"""
# mode selection rule: shortest possible way, if tie, choose smaller order
def mode_selection(dict_dim,dict_Uimr):
    """
    mode selection rule
    SFM: shortest possible way, if d tie, calculate RU; if RU also tie, choose smaller order
    """
    sort_m = sorted(dict_dim.values())

    # d tie, calculate RU
    if sort_m[0] in sort_m[1:]:
        m = 0
        d = 0
        ru = np.sum(R_r)
        for i,di in enumerate(dict_dim.values()):
            if di==sort_m[0]:
                mi = i+1
                rui = np.sum(dict_Uimr[mi])
                if rui<ru:
                    m=mi
                    d=di
                    ru=rui
        return m, d

    else:
        # min_d = sort_m[0]
        for d in sort_m:
            m = list(dict_dim.keys())[list(dict_dim.values()).index(d)]
            if ((np.array(R_r) - np.array(dict_Uimr[m]))>=0).all():
                return m, d


# priority rule: random selection
def priority_rule(SE):
    """priority rule: random selection"""
    return random.choice(SE)

# find type of renewable resource R, either R1 or R2
def typeR(U_im):
    """U_im (list)"""
    r_id = 0
    r = 0
    # print(U_im,type(U_im))
    for i in range(len(U_im)):
        if U_im[i] != 0:
            r_id = i
            r = U_im[i]
    return r_id,r

# union of 2 sets
def uni(s1, s2):
    s = list(set(s1).union(set(s2)))
    return s

# difference of 2 sets
def diff(s1, s2):
    s = list(set(s1) - set(s2))
    return s


"""Pre-process"""
def data_process(A, d_im, U_imr):
    D_i = {}
    U_i = {}
    U_im = {}
    for i in A:
        m_i,d_i = mode_selection(d_im[i], U_imr[i])
        r_im = U_imr[i][m_i]
        r_id, r = typeR(r_im)
        D_i[i] = d_i
        U_i[i] = {r_id: r}
        U_im[i] = r_im
    return D_i, U_i, U_im


def get_pred(prec):
    """
    prec (dict): P_prec
    """
    P_pre = {}

    for i in prec:
        succ = prec[i]
        for j in succ:
            if j not in P_pre:
                P_pre[j] = [i]
            else:
                P_pre[j].append(i)
    return P_pre


D_i, U_i, U_im = data_process(A,d_im,U_imr)
pr = get_pred(P_prec)
# print(D_i)
# print(U_i)
# print(U_im)
# print(pr)


"""algorithm (a): generation of initial schedules"""
def initial_schedule2(d_im,P_prec,r,R_r,U_imr,nr=None,R_nr=None,U_imnr=None):
    """
    return:
        s (list): start time
        f (list): end time
        order (dict): activity sequence
    """
    
    g, t = 0,0
    C_g = []   # already scheduled and completed
    E_g = []   # predecessors Predj have been completed 
    A_g = [1]  # active 
    SE_g = [1] # a subset of E_g, will start at time t_g
    
    s = np.zeros((len(num_r),len(A)))
    f = np.zeros((len(num_r),len(A)))
    order = {}

    D_i, U_i, U_im = data_process(A,d_im,U_imr)
    Prec_i = get_pred(P_prec)

    # for run in range(runMax):
        
    # while len(uni(C_g, A_g)) <= len(A):
    while len(C_g) <= len(A):

        g += 1
        t += 1

        t_g = tMax
        for i in A_g:
            r_id,_ = typeR(U_im[i])
            t_g = min(t_g, f[r_id][i-1])

        t_g_i = []
        A_g_new = []
        for i in A_g:
            r_id,_ = typeR(U_im[i])
            if f[r_id,i-1]<=t_g:
                t_g_i.append(i)
            else: A_g_new.append(i)
        
        C_g = uni(C_g, t_g_i)
        A_g = A_g_new
        order[g] = t_g_i

        C_g_succ = []
        for i in C_g:
            C_g_succ += P_prec[i]
        C_g_succ = list(set(C_g_succ))

        C_g_succ_new = []
        for i_c in C_g_succ:
            isvalid = True
            for i_c_prec in Prec_i[i_c]:
                if i_c_prec not in C_g and isvalid:
                    isvalid = False
            if isvalid: C_g_succ_new.append(i_c)

        E_g = diff(C_g_succ_new, uni(C_g, A_g))
        SE_g = []

        Rr_g = []
        for i in A_g:
            u_i = U_im[i]
            Rr_g.append(u_i)
        Rr_g = R_r - np.sum(Rr_g,axis=0)
        # Rnr_g = 

        # print("iter: ",g)
        # print("Complete: ",C_g)
        # print("Activate: ",A_g)
        # print("Eligible: ",E_g)
        # print("SubE: ",SE_g)
        # print("\n")

        while E_g:
            i_next = priority_rule(E_g)
            u_i_next = U_im[i_next]
            E_g = diff(E_g, [i_next])

            if ((Rr_g-u_i_next)>=0).all():
                # if Rnr_g- 

                r_id,r = typeR(u_i_next)

                SE_g = uni(SE_g, [i_next])
                A_g = uni(A_g, [i_next])
                Rr_g -= u_i_next
                s[r_id][i_next-1] = t_g
            else:
                SE_g = SE_g
                A_g = A_g

        for i in SE_g:
            r_id,_ = typeR(U_im[i])
            f[r_id][i-1] = s[r_id][i-1] + D_i[i]

        if len(C_g) == len(A)-1:
            # print("end: ",C_g)
            break
    return s,f,order



"""Plot"""
def plottask(start,finish,order):
    """
    start (np.array)
    finish (np.array)
    order (dict)
    """
    numRow = len(num_r)
    numCol = 1

    s = start
    f = finish
    w = f-s
    h = np.zeros((len(num_r),len(A)))
    for i in range(len(A)):
        r_id,r = typeR(U_im[i+1])
        h[r_id][i] = r

    tag = np.zeros((numRow, tMax))
    rtag = np.zeros((numRow, tMax))
    yltag = np.zeros((len(num_r),len(A)))

    plt.figure(figsize=(10,10))
    for t,i in enumerate(order.values()):
        i = i[0]   # activity
        idx = i-1  # index
        r_id,r = typeR(U_im[i])
        si = int(s[r_id][idx])
        hi = int(h[r_id][idx])
        wi = int(w[r_id][idx])
        
        for t in range(si,si+wi):
            if tag[r_id][t] == 0:
                tag[r_id][t] = i
                rtag[r_id][t] = r

        if tag[r_id][si] != i:
            print("here: ", i, tag[r_id][si])

            yli = yltag[r_id][int(tag[r_id][si])-1]
            if hi <= yli:
                yl = 0
            else:
                yl = rtag[r_id][si]
        else: yl = 0
        yltag[r_id][idx]=yl
        print(i,si, yl, hi, wi)

        # if i != 1:
        # subplot(numRows, numCols, plotNum)
        plt.subplot(numRow,numCol,r_id+1)
        plt.axhline(y=R_r[r_id], ls="--", c="r")
        plt.bar(si, hi, wi, bottom=yl, align="edge", label="{}".format(i))
        plt.legend(loc="upper right")
        plt.xlabel('Time')
        plt.ylabel('Resource use')
        plt.xlim([0,tMax])
        plt.title('Renewable reaource R{}'.format(r_id+1))
        plt.grid(linestyle='-.')
    # plt.savefig(path + 'Initial Schedules.png', format='png')


"""algorithm (b) Shaking phase: swap/move"""
run = 1000

"""extensive experiment: generate several intial schedules and select the one with best makespan"""
def generate_init(run):
    orders = []
    ord_dic = {}
    for k in range(run):
        sk,fk,ok = initial_schedule2(d_im,P_prec,num_r,R_r,U_imr)
        f = max(fk.flatten())
        ord = [o[0] for o in list(ok.values())]
        if ord not in orders:
            orders.append(ord)
            if f not in ord_dic:
                ord_dic[f] = [ord]
            else: ord_dic[f].append(ord)
    return orders,ord_dic


def ifswap(id,i,cs):
    """
    Apply precedence and resource constraints
    args:
        id: current activity 
        i:  swap activity
        cs: current schedules
    return:
        ifswap (bool): if id and i can swap
    """
    i_pred = get_pred(P_prec)

    isvalid = False
    if i not in P_prec[id]:
        if set(i_pred[i]) <= set(cs[:id]):  # < if a include b; <= if b is subset of a
            isvalid = True
      
    return isvalid


def check_unique(feas_uni):
    """
    args:
        feas_uni (list): all feasible unique schedules after swapping
    return:
        isunique (bool) 
    """
    isunique = True
    for i,f in enumerate(feas_uni):
        ff = feas_uni[:i]+feas_uni[i+1:]
        if f in ff:
            ii = ff.index(f)
            print(i, ":", f, "same", ii)
            isunique = False
    return isunique


def swap(BS_uni):
    """
    Enhanced activity swapping strategy
    args:
        BS_uni (2d-list): a set of unique feasible schedules with best makespan generated by algorithm (a)
    return:
        AS (2d-list): feasible unique schedules    
    """
    AS = []
    cnt = 0
    for p in range(len(BS_uni)):       # p: num of unique best schedules
        CS = BS_uni[p]
        for k in range(1,len(A)-1):    # k: activities available in project, excluding dummy end nodes, start from activity 1
            activity = CS[k]
            print("\n", k,":", activity, BS_uni[p])

            # forward swap
            CS_copy_f = copy.deepcopy(CS)
            for i in range(len(A)-1-k):
                id1 = CS_copy_f.index(activity)
                if ifswap(CS_copy_f[id1],CS_copy_f[k+i],CS_copy_f):   # apply constraints
                    CS_copy_f[id1],CS_copy_f[k+i] = CS_copy_f[k+i],CS_copy_f[id1]
                    print(p,k,i,CS_copy_f)
                    if CS_copy_f not in AS:   # if unique
                        cnt += 1
                        print(cnt, "Forward PICK: ", CS_copy_f)
                        find = copy.deepcopy(CS_copy_f)
                        AS.append(find)

            # backward swap
            CS_copy_b = copy.deepcopy(CS)
            for j in range(k-1):
                id2 = CS_copy_b.index(activity)
                if ifswap(CS_copy_b[k-j-1],CS_copy_b[id2],CS_copy_b):  # apply constraints
                    CS_copy_b[id2],CS_copy_b[k-j-1] = CS_copy_b[k-j-1],CS_copy_b[id2]
                    print(p,k,j,CS_copy_b)
                    if CS_copy_b not in AS:   # if unique
                        cnt += 1
                        print(cnt, "Backward PICK: ", CS_copy_b)
                        find = copy.deepcopy(CS_copy_b)
                        AS.append(find)
    
    if check_unique(AS):
        print("All feasible schedules are uniqe. GOOD LUCK.")
        return AS
    else:
        print("Please double check SWAP algorithm !!! ")



"""algorithm (c) Obtain modified makespan: calculate new finish time"""
def modified_makespan(feas, d_im,P_prec,r,R_r,U_imr,nr=None,R_nr=None,U_imnr=None):
    """
    Calculate new finish time of new-generated precedence feasible schedules
    args:
        feas (list): schedules order generated by swapping/moving
    return:
        s (ndarray) 
        f (ndarray)
        modified_f (scalar): modified makespan
    """

    g, t = 0,0
    NS_g = 0
    C_g = []   # already scheduled and completed
    # E_g = []   # predecessors Predj have been completed 
    A_g = [1]  # active 
    SE_g = [1] # a subset of E_g, will start at time t_g
    
    s = np.zeros((len(num_r),len(A)))
    f = np.zeros((len(num_r),len(A)))

    D_i, U_i, U_im = data_process(A,d_im,U_imr)
    Prec_i = get_pred(P_prec)

    # for run in range(runMax):
        
    # while len(uni(C_g, A_g)) <= len(A):
    while len(C_g) <= len(A):

        g += 1
        t += 1

        t_g = tMax
        for i in A_g:
            r_id,_ = typeR(U_im[i])
            t_g = min(t_g, f[r_id][i-1])

        t_g_i = []
        A_g_new = []
        for i in A_g:
            r_id,_ = typeR(U_im[i])
            if f[r_id,i-1]<=t_g:
                t_g_i.append(i)
            else: A_g_new.append(i)
        
        C_g = uni(C_g, t_g_i)
        A_g = A_g_new

        SE_g = []

        Rr_g = []
        for i in A_g:
            u_i = U_im[i]
            Rr_g.append(u_i)
        Rr_g = R_r - np.sum(Rr_g,axis=0)
        # Rnr_g = 

        print("iter: ",g)
        print("Complete: ",C_g)
        print("Activate: ",A_g)
        # print("Eligible: ",E_g)
        print("SubE: ",SE_g)
        print("\n")

        if len(C_g) == len(A)-1:
            print("end: ",C_g)
            break

        for k in range(NS_g,len(feas)):
            i_next = feas[k]
            print("k: ", k)
            print("i: ", i_next)
            print("Rr_g: ", Rr_g)
            # i_next = priority_rule(E_g)
            u_i_next = U_im[i_next]

            if ((Rr_g-u_i_next)>=0).all():
                # if Rnr_g- 

                r_id,r = typeR(u_i_next)

                SE_g = uni(SE_g, [i_next])
                A_g = uni(A_g, [i_next])
                Rr_g -= u_i_next
                print("i: ",i_next, t_g)
                s[r_id][i_next-1] = t_g
            else:
                SE_g = SE_g
                A_g = A_g
                NS_g = k
                break

        for i in SE_g:
            r_id,_ = typeR(U_im[i])
            f[r_id][i-1] = s[r_id][i-1] + D_i[i]

    modified_f = max(f.flatten())
    return s,f,modified_f


"""Main: whole procedures"""
def MVNSH(runMax,fBest):
    run = 0
    start = time.time()
    
    while run <= runMax:
        print("1")
        s,f,order = initial_schedule2(d_im,P_prec,num_r,R_r,U_imr)
        makespan = max(f.flatten())
        if makespan == fBest:
            print("2")
            break
        else:
            ord_list = [o[0] for o in list(order.values())]
            feas_uni = swap([ord_list])

            u_s,u_f,u_makespan = modified_makespan(feas_uni[0],d_im,P_prec,num_r,R_r,U_imr)

            if u_makespan == fBest:
                makespan = u_makespan
                print("3")
                break
            else:
                makespan = min(makespan, u_makespan)
                run += 1
    
    end = time.time()
    tspan = end-start

    print("run: ", run)
    print("makespan: ", makespan)
    print("time: ", tspan)

    return makespan, tspan

if __name__ == "__main__":
    MVNSH(runMax,fBest)
