def initial_schedule(d_im,P_prec,r,R_r,U_imr,nr=None,R_nr=None,U_imnr=None):
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
