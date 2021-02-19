def absolute_inefficiency(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0):
    import numpy as np
    import math
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

    #add information on buckets to the sum_vector
    sum_vector_buckets = np.empty([len(trace_distinct), 1], dtype='<U2')
    for i in range(len(trace_distinct)):
        if trace_distinct[i] in S2: 
            sum_vector_buckets[i] = 'S2'
        elif trace_distinct[i] in S1: 
            sum_vector_buckets[i] = 'S1'
        elif trace_distinct[i] in S0: 
            sum_vector_buckets[i] = 'S0'
        elif trace_distinct[i] in C2:
            sum_vector_buckets[i] = 'C2'
        elif trace_distinct[i] in C1:
            sum_vector_buckets[i] = 'C1'
        elif trace_distinct[i] in C0:
            sum_vector_buckets[i] = 'C0'
        elif trace_distinct[i] in E2:
            sum_vector_buckets[i] = 'E2'
        elif trace_distinct[i] in E1:
            sum_vector_buckets[i] = 'E1'
        elif trace_distinct[i] in E0:
            sum_vector_buckets[i] = 'E0'

    #count items of buckets
    #bucket counter: S2, S1, S0, C2, C1, C0, E2, E1, E0
    buckets = [0]*9
    for i in range(len(trace_distinct)):
        if trace_distinct[i] in S2:
            buckets[0] = int(buckets[0]) + int(sum_vector[i])
        elif trace_distinct[i] in S1:
            buckets[1] = int(buckets[1]) + int(sum_vector[i])
        elif trace_distinct[i] in S0:
            buckets[2] = int(buckets[2]) + int(sum_vector[i])
        elif trace_distinct[i] in C2:
            buckets[3] = int(buckets[3]) + int(sum_vector[i])
        elif trace_distinct[i] in C1:
            buckets[4] = int(buckets[4]) + int(sum_vector[i])
        elif trace_distinct[i] in C0:
            buckets[5] = int(buckets[5]) + int(sum_vector[i])
        elif trace_distinct[i] in E2:
            buckets[6] = int(buckets[6]) + int(sum_vector[i])
        elif trace_distinct[i] in E1:
            buckets[7] = int(buckets[7]) + int(sum_vector[i])
        elif trace_distinct[i] in E0:
            buckets[8] = int(buckets[8]) + int(sum_vector[i])

    #cluster frequency vector
    #bucket counter: S2, S1, S0, C2, C1, C0, E2, E1, E0
    distinct_buckets = [0]*9
    for i in range(len(trace_distinct)):
        if (sum_vector_buckets[i] == 'S2') and (sum_vector[i] > 0):
            distinct_buckets[0] = distinct_buckets[0] + 1
        elif (sum_vector_buckets[i] == 'S1') and (sum_vector[i] > 0):
            distinct_buckets[1] = distinct_buckets[1] + 1
        elif (sum_vector_buckets[i] == 'S0') and (sum_vector[i] > 0):
            distinct_buckets[2] = distinct_buckets[2] + 1
        elif (sum_vector_buckets[i] == 'C2'):
            distinct_buckets[3] = int(distinct_buckets[3]) + int(sum_vector[i])
        elif (sum_vector_buckets[i] == 'C1') and (sum_vector[i] > 1):
            distinct_buckets[4] = distinct_buckets[4] + 1
        elif (sum_vector_buckets[i] == 'C0') and (sum_vector[i] > 0):
            distinct_buckets[5] = distinct_buckets[5] + 1
        elif (sum_vector_buckets[i] == 'E2') and (sum_vector[i] > 0):
            distinct_buckets[6] = distinct_buckets[6] + 1
        elif (sum_vector_buckets[i] == 'E1') and (sum_vector[i] > 0):
            distinct_buckets[7] = distinct_buckets[7] + 1
        elif (sum_vector_buckets[i] == 'E0') and (sum_vector[i] > 0):
            distinct_buckets[8] = distinct_buckets[8] + 1
    
    #score for bucket S2
    score_S2 = 0
    for i in range(len(trace_distinct)):
        if (trace_distinct[i] in S2) and (sum_vector[i]>0):
            #get indices
            indices = []
            for j in range(len(trace)):
                if trace[j] == trace_distinct[i]:
                    indices.append(j)
            #go through the list of indices
            for k in range(1, int(sum_vector[i]+1)):
                #score_S2 = score_S2 + location x (1 + distance + distinct_activities)
                score_S2 = score_S2 + ((1-k+indices[k-1]) * (1/max(1, len(trace)-k))) * (1+((1-k+(((len(trace)-1) if k==1 else indices[0]) - indices[k-1])) * (1/max(1, len(trace)-k))) + ((distinct_buckets[0] - 1)*(1/(max(1, (len(trace)-1))))))
                
    #score for bucket S1
    score_S1 = 0
    counter_S1 = 0
    for i in range(len(trace_distinct)):
        if (trace_distinct[i] in S1) and (sum_vector[i]>0):
            #get indices
            indices = []
            for j in range(len(trace)):
                if trace[j] == trace_distinct[i]:
                    indices.append(j)
            #increase counter
            counter_S1 = counter_S1 + 1
            #go through the list of indices
            for k in range(1, int(sum_vector[i]+1)):
                #score_S1 = score_S1 + location x (1 + distance + frequency)
                score_S1 = score_S1 + (((indices[k-1])*(1/(max(1,(len(trace)-1)))))) * (1+((indices[k-1] - indices[0]) * (1/(max(1,(len(trace)-1))))) + (((k-1) * (1/(max(1,(len(trace)-1)))))))
    
    #score for bucket S0
    score_S0 = 0
    if trace[0] in S0:
        score_S0 = 1
    
    #score for bucket E2
    score_E2 = 0
    for i in range(len(trace_distinct)):
        if (trace_distinct[i] in E2) and (sum_vector[i]>0):
            #get indices
            indices = []
            for j in range(len(trace)):
                if trace[j] == trace_distinct[i]:
                    indices.append(j)
            indices.sort(reverse=True)
            #go through the list of indices
            for k in range(1, int(sum_vector[i]+1)):
                #score_E2 = score_E2 + location x (1 + distance + distinct_activities)
                score_E2 = score_E2 + (1-(1 if len(trace) == sum_vector[i] else ((indices[k-1]) * (1/max(1, len(trace)-k))))) * (1+((1-k+((len(trace)-1) if k==1 else indices[0] - indices[k-1])) * (1/max(1, len(trace)-k))) + ((distinct_buckets[6] - 1)*(1/(max(1, (len(trace)-1))))))
    
    #score for bucket E1
    score_E1 = 0
    for i in range(len(trace_distinct)):
        if (trace_distinct[i] in E1) and (sum_vector[i]>0):
            #get indices
            indices = []
            for j in range(len(trace)):
                if trace[j] == trace_distinct[i]:
                    indices.append(j)
            indices.sort(reverse=True)
            #go through the list of indices
            for k in range(1, int(sum_vector[i]+1)):
                #score_E1 = score_E1 + location x (1 + distance + frequency)
                score_E1 = score_E1 + (1-((indices[k-1])*(1/(max(1,(len(trace)-1)))))) * (1+((indices[0] - indices[k-1]) * (1/(max(1,(len(trace)-1))))) + (((k-1) * (1/(max(1,(len(trace)-1)))))))
    
    #score bucket E0
    score_E0 = 0
    if trace[-1] in E0:
        score_E0 = 1
    
    #score bucket C2
    score_C2 = 0
    for i in range(len(trace_distinct)):
        if (trace_distinct[i] in C2):
            #get indices
            indices = []
            for j in range(len(trace)):
                if trace[j] == trace_distinct[i]:
                    indices.append(j)
            #check location of first and last C2 activity; must not be in the beginning or end
            if indices[0] == 0:
                score_C2 = score_C2 + 1
            if indices[-1] == len(trace)-1:
                score_C2 = score_C2 + 1
    
    #score bucket C1
    score_C1 = 0
    for i in range(len(trace_distinct)):
        if (trace_distinct[i] in C1):
            #get indices
            indices = []
            for j in range(len(trace)):
                if trace[j] == trace_distinct[i]:
                    indices.append(j)
            #check location of first and last C1 activity; must not be in the beginning or end (boundaries)
            if indices[0] == 0:
                score_C1 = score_C1 + 1
            if indices[-1] == len(trace)-1:
                score_C1 = score_C1 + 1
            #if there are multiple C1 activities of one type, also check their frequency and distance
            if (sum_vector[i]>1):
                for k in range(2, int(sum_vector[i]+1)):
                    #score_C1 = score_C1 + distance + location
                    score_C1 = score_C1 + ((indices[k-1] - indices[0]) * (1/(max(1,(len(trace)-1)))))  + ((indices[k-1])*(1/(max(1,(len(trace)-1)))))
    
    #score for bucket C0
    score_C0 = 0
    #only if trace has length > 2, there can be a violation of C0 activities
    if len(trace)>2:
        #get number of distinct C0 activities only within the trace (not start, not end)
        distinct_C0 = []
        for i in range(1, len(trace)-1):#we iterate over the trace, without start and end
            if trace[i] in C0:
                distinct_C0.append(trace[i])
        distinct_C0 = list(set(distinct_C0))
        count_distinct_C0 = len(distinct_C0)
        #start iterating through the trace to compute the score
        for i in range(len(trace_distinct)):
            if (trace_distinct[i] in C0) and (sum_vector[i]>0):
                #get indices
                indices = []
                for j in range(len(trace)):
                    if trace[j] == trace_distinct[i]:
                        indices.append(j)
                #check if C0 activities are at start or end of the trace; do not need to be considered later
                if len(indices)!=0 and indices[0] == 0:
                    del indices[0]
                if len(indices)!=0 and indices[-1] == len(trace)-1:
                    del indices[-1]
                if len(indices)==0:
                    score_C0 = score_C0 + 0
                else:
                    #if there is just 1 C0-activity of a certain distinction, only the location & distinct_buckets are of importance
                    #score_C0 = score_C0 + (1 + distinct_activities) x (location)
                    score_C0 = score_C0 + (1+(count_distinct_C0-1)*(1/(max(1, (len(trace)-3))))) * ((indices[0])*(1/(max(1, (len(trace)-2)))))
                    #if there is more than 1 C0-activity of a certain distinction, we further increase the score
                    if len(indices) > 1:
                        #go through the list of indices
                        for k in range(2, len(indices)+1):
                            #score_C0 = score_C0 + (1 + distinct_activities) x (distance + location)
                            score_C0 = score_C0 + (1+(count_distinct_C0-1)*(1/(max(1, (len(trace)-3))))) * (((indices[k-1] - indices[0]-1) * (1/(max(1, (len(trace)-3))))) + ((indices[k-1]-1)*(1/(max(1, (len(trace)-3))))))

    #overall results
    result = {'S2': score_S2, 'S1': score_S1, 'S0': score_S0, 'C2': score_C2, 'C1': score_C1, 'C0': score_C0, 'E2': score_E2, 'E1': score_E1, 'E0': score_E0}
    
    return result