"""
INPUTs
args: 
    M_i
    d_im
    P_prec
    num_r, R_r, U_imr
    num_nr, R_nr, U_imnr: default None
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
        11:[12],}
        # 12:[12]}


"""Parameters"""
# fBest = 
# sBest = 
runMax = 100
tMax = 25

numI = 10                       # num of activities
I = [2,3,4,5,6,7,8,9,10,11]      # activities
# i = 1,2,...,11,11+1                # including start and end dummy nodes
A = [1,2,3,4,5,6,7,8,9,10,11,12] # the set of nodes
