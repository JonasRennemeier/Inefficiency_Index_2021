def inefficiency_index_section(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0):
    from absolute_inefficiency import absolute_inefficiency
    from inefficiency_index_cluster import inefficiency_index_cluster
    
    #we take the average of those clusters, that have at least one activitiy assigned to
    #count how many clusters have activities assigned to them
    start_clusters = (len(S2)>0)+(len(S1)>0)+(len(S0)>0)
    core_clusters = (len(C2)>0)+(len(C1)>0)+(len(C0)>0)
    end_clusters = (len(E2)>0)+(len(E1)>0)+(len(E0)>0)
    
    #calculate indices per section
    index_start = (inefficiency_index_cluster(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['S2'] + inefficiency_index_cluster(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['S1'] + inefficiency_index_cluster(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['S0']) / start_clusters
    index_core = (inefficiency_index_cluster(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['C2'] + inefficiency_index_cluster(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['C1'] + inefficiency_index_cluster(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['C0']) / core_clusters
    index_end = (inefficiency_index_cluster(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['E2'] + inefficiency_index_cluster(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['E1'] + inefficiency_index_cluster(trace, S2, S1, S0, C2, C1, C0, E2, E1, E0)['E0']) / end_clusters
    
    #result
    result = {'Start': index_start, 'Core': index_core, 'End': index_end}
    
    return result