def inefficiency_index_cluster(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0):
    import numpy as np
    import math
    from absolute_inefficiency import absolute_inefficiency
    
    #length of traces
    trace_length = len(trace)

    #distinct values of traces
    trace_distinct = list(set(trace))
    trace_distinct.sort()

    #create the activity order matrix
    matrix = np.empty([len(trace_distinct), trace_length], dtype=int)
    #replace values from activity order matrix
    for i in range(trace_length):
        for j in range(len(trace_distinct)):
            if trace[i] == trace_distinct[j]:
                matrix[j][i] = 1
            else:
                matrix[j][i] = 0

    #get frequency of distinct activities
    #create activity frequency vector 
    sum_vector = np.empty([len(trace_distinct), 1], dtype=int)
    #write the vector
    for i in range(len(trace_distinct)):
        sum_vector[i] = np.sum(matrix[i])

    #cluster frequency vector
    #bucket counter: S2, S1, S0, C2, C1, C0, E2, E1, E0
    distinct_buckets = [0]*9
    for i in range(len(trace_distinct)):
        if (trace_distinct[i] in S2) and (sum_vector[i] > 0):
            distinct_buckets[0] = distinct_buckets[0] + 1
        if (trace_distinct[i] in S1) and (sum_vector[i] > 0):
            distinct_buckets[1] = distinct_buckets[1] + 1
        if (trace_distinct[i] in S0) and (sum_vector[i] > 0):
            distinct_buckets[2] = distinct_buckets[2] + 1
        if (trace_distinct[i] in C2):
            distinct_buckets[3] = int(distinct_buckets[3]) + int(sum_vector[i])
        if (trace_distinct[i] in C1) and (sum_vector[i] > 1):
            distinct_buckets[4] = distinct_buckets[4] + 1
        if (trace_distinct[i] in C0) and (sum_vector[i] > 0):
            distinct_buckets[5] = distinct_buckets[5] + 1
        if (trace_distinct[i] in E2) and (sum_vector[i] > 0):
            distinct_buckets[6] = distinct_buckets[6] + 1
        if (trace_distinct[i] in E1) and (sum_vector[i] > 0):
            distinct_buckets[7] = distinct_buckets[7] + 1
        if (trace_distinct[i] in E0) and (sum_vector[i] > 0):
            distinct_buckets[8] = distinct_buckets[8] + 1
    
    #normalization
    score_S2_norm = 0
    score_S1_norm = 0
    score_S0_norm = 0
    score_C2_norm = 0
    score_C1_norm = 0
    score_C0_norm = 0
    score_E2_norm = 0
    score_E1_norm = 0
    score_E0_norm = 0
    
    #enter the calculation of the normalization only if the trace contains activities of this category
    
    #normalization S2
    if distinct_buckets[0] > 0:
        #worst trace contains as many distinct S2 activities as possible
        #the last index must be the first type again
        #if there are more than one space left, fill all the remaining spaces with the first type
        worst_trace_S2 = [S2[0]]*len(trace)
        #if trace length == 2, the first activity must not be S2
        if len(trace) < 3:
            worst_trace_S2[0] = C2[0]
        else:
            #if there is just one S2 activity, we leave index 1 empty (replace it with another C2 activity)
            if len(S2) == 1:
                worst_trace_S2[1] = C2[0]
            else:
                for i in range(len(trace)-1):
                    if i <= (len(S2)-1):
                        worst_trace_S2[i] = S2[i]
                    else:
                        break
        score_S2_norm = absolute_inefficiency(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['S2'] / absolute_inefficiency(worst_trace_S2, S2, S1, S0, C2, C1, C0, E2, E1, E0)['S2']
    
    #normalization S1
    if distinct_buckets[1] > 0:
        #worst trace must have one type of S1 activities at all places
        worst_trace_S1 = [S1[0]]*len(trace)
        if len(trace) == 1:
            score_S1_norm = 0
        else:
            score_S1_norm = absolute_inefficiency(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['S1'] / absolute_inefficiency(worst_trace_S1, S2, S1, S0, C2, C1, C0, E2, E1, E0)['S1']
    
    #normalization S0
    if distinct_buckets[2] > 0:
        #S0 score is binary
        score_S0_norm = absolute_inefficiency(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['S0']
    
    #normalization E1
    if distinct_buckets[7] > 0:
        #worst trace must have one type of E1 activities at all places
        worst_trace_E1 = [E1[0]]*len(trace)
        if len(trace) == 1:
            score_E1_norm = 0
        else:
            score_E1_norm = absolute_inefficiency(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['E1'] / absolute_inefficiency(worst_trace_E1, S2, S1, S0, C2, C1, C0, E2, E1, E0)['E1']
    
    #normalization E2
    if distinct_buckets[6] > 0:
        #starting from the back
        #worst trace contains as many different types of E2 as possible. 
        #the first index must be filled with the first type of E2 activity
        #if there are more than one space left, fill all the remaining spaces with the first type
        worst_trace_E2 = [E2[0]]*len(trace)
        #if trace length == 2, the last activity must not be E2
        if len(trace) == 2:
            if len(C2)>0:
                worst_trace_E2[0] = C2[0] 
            elif len(C1)>0:
                worst_trace_E2[0] = C1[0]
                                     
        else:
            if len(E2) == 1:
                #from the second last to the middle of the trace, the activities must not be E2
                if len(C2)>0:
                    for i in range(1, math.floor(len(trace)/2)+1):
                        worst_trace_E2[i] = C2[0]
                elif len(C1)>0:
                    for i in range(1, math.floor(len(trace)/2)+1):
                        worst_trace_E2[i] = C1[0]
            else:
                for i in range(len(trace)-1):
                    if i <= (len(E2)-1):
                        worst_trace_E2[i] = E2[i]
                    else:
                        break
                worst_trace_E2[1] = C2[0]
        worst_trace_E2.reverse()
        score_E2_norm = absolute_inefficiency(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['E2'] / absolute_inefficiency(worst_trace_E2, S2, S1, S0, C2, C1, C0, E2, E1, E0)['E2']
    
    #normalization E0
    if distinct_buckets[8] > 0:
        #E0 score is binary
        score_E0_norm = absolute_inefficiency(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['E0']
    
    #normalization C2
    if distinct_buckets[3] > 0:
        #worst trace must have a C2 activity at start and end
        worst_trace_C2 = [C2[0]]*len(trace)
        score_C2_norm = absolute_inefficiency(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['C2'] / absolute_inefficiency(worst_trace_C2, S2, S1, S0, C2, C1, C0, E2, E1, E0)['C2']
    
    #normalization C1
    if distinct_buckets[4] > 0:
        #worst trace consists of one type of C1 activity only
        worst_trace_C1 = [C1[0]]*len(trace)
        score_C1_norm = absolute_inefficiency(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['C1'] / absolute_inefficiency(worst_trace_C1, S2, S1, S0, C2, C1, C0, E2, E1, E0)['C1']
    
    #normalization C0
    if distinct_buckets[5] > 0:
        #worst trace contains as many different C0 activities as possible at the core of the trace
        #if the trace is longer than the number of different C0 activities, fill all remaining spaces with the first type of C0
        worst_trace_C0 = [C0[0]]*len(trace)
        #if trace length == 2, there are no within trace activities
        if len(trace)==2:
            score_C0_norm = 0
        else:
            #we only consider within trace activities
            for i in range(1, len(trace)-1):
                if i <= (len(C0)):
                    worst_trace_C0[i] = C0[i-1]
                else:
                    break
            #if trace contains more than five activities, the second last activity must be the same as the first C0 activity
            if len(trace)>5:
                worst_trace_C0[-2] = C0[0]
            score_C0_norm = absolute_inefficiency(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['C0'] / absolute_inefficiency(worst_trace_C0, S2, S1, S0, C2, C1, C0, E2, E1, E0)['C0']
    
    #overall results
    result = {'S2': score_S2_norm, 'S1': score_S1_norm, 'S0': score_S0_norm, 'C2': score_C2_norm, 'C1': score_C1_norm, 'C0': score_C0_norm, 'E2': score_E2_norm, 'E1': score_E1_norm, 'E0': score_E0_norm}
    
    return result