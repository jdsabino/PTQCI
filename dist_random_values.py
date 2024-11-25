def dist_random_values(nvals, vals, probs):

    import numpy as np

    tol = 1e-6
    #trick_value = tol*tol#np.float64(10) # dirty trick

    if len(vals) != len(probs):
        print("List of values and probabilities must have the same size!")

        return ValueError
    
    if abs(1 - sum(probs)) > tol:
        print("Probabilities must sum to 1!")

        return ValueError
    
    val_array = np.random.uniform(size=nvals)
    val_array_store = np.zeros(nvals)

    # print("SHAPES")
    # print(val_array.shape)
    # print(val_array_store.shape)

    idx_ordered = np.argsort(probs, stable=True)
    porder = probs[idx_ordered.astype(int)]
    vorder = vals[idx_ordered.astype(int)]

    #index_prev = None
    for idx, val in enumerate(vorder):

        #print("IDX: " + str(idx))
        
        if idx == 0:
            upper = porder[idx]
            indexes = np.where(val_array <= upper)[0]
            # index_prev = indexes
            val_array_store[indexes] = val #+ trick_value # dirty trick
            continue


        lower = upper
        upper = porder[idx] + porder[:idx].sum()
        #print("Lower: " + str(lower) + " Uper: " +str(upper))
        aaa = np.logical_and(val_array > lower, val_array <= upper)
        #print("val_array: ")
        #print(val_array)
        #print("And op: ")
        #print(aaa)
        indexes = np.where(np.logical_and(val_array > lower, val_array <= upper))[0]
        # print(np.intersect1d(indexes, index_prev).shape)
        # print("Indexes len: " +str(indexes.shape))
        # print("Val: " + str(val))
        # print("Check 1: "+str(val_array[val_array==(val)].shape))
        val_array_store[indexes] = val# +  trick_value # trick to avoid wrong replacement. Needs a better implementation
        #print("Check 2: "+str(val_array[val_array==(val)].shape))
        # index_prev = indexes


    # [print(val_array[val_array==vvv].shape[0]/val_array.shape[0]) for vvv in vorder]
    return val_array_store# - trick_value

# Test if it works without trick value (why is val_cnt==0?
