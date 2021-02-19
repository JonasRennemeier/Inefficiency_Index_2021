# Inefficiency_Index_BPM2021

There are three functions (here presented as modules) that make up the inefficiency index:
  - The function "absolute_inefficiency" computes the absolute inefficiency of a trace in terms of every cluster separately
  - The function "inefficiency_index_cluster" derives the artificial worst trace and compares it to the actual trace. Thereby, it computes the inefficiency index of each cluster
  - The function "inefficiency_index_section" aggregates the inefficiency indices of the clusters to a total of three indices (one for each section of the trace, i.e., start, core, and end)
