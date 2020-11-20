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
    plt.savefig(path + 'Modified Schedules.png', format='png')
