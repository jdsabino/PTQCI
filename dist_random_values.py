def dist_random_values(nvals, vals, probs):

    import numpy as np

    if len(vals) != len(probs):
        print("List of values and probabilities must have the same size!")

        return ValueError
    
    if sum(probs) != 1:
        print("Probabilities must sum to 1!")

        return ValueError
    
    val_array = np.random.uniform(size=nvals)

    idx_ordered = np.argsort(probs)
    porder = probs[idx_ordered]
    vorder = vals[idx_ordered]


    for idx, val in enumerate(vorder):
        if idx == 0:
            indexes = np.where(val_array <= porder[idx])[0]
            val_array[indexes] = val
            continue
        
        indexes = np.where(np.logical_and(val_array > porder[idx-1], val_array <= porder[idx] + porder[idx-1]))[0]
        val_array[indexes] = val
    
    return val_array