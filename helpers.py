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
    get all predecessors of activities
    args:
        prec (dict): P_prec constant
    return:
        P_pre (dict)
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
