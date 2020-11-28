=====
Usage
=====


To use branesta, simply run branesta command from terminal and provive the following arguments

srcdir: path to times-series to analyze. There are certain requirements for the input time-series:
1. Must be parcelled into ROIs, max 1000 ROIs
2. Shape must be 2D: time x space
3. File format must be .csv with no header row or index column
4. Filenames must follow BIDS convention (https://bids.neuroimaging.io/)
(see example time-series for reference)

outdir: path to output directory. Computed metrics and log files will be placed here.

win_len: number of time-frames within each time window. With a TR of ~1s, at least 30 is recommended.

--subnetpath: optional, path to subnetwork indexes file. If provided, network stability is computed separately for edges corresponding to subnetworks. If not provided, the program defaults to a default subnetwork (labeled as whole_brain) consisting of all ROIs. Must be a .csv with two columns and a header row (roi, network).
(see example subnetworks_willard.csv for reference)

--tot_len: optional, expected length of input time-series. If provided together with tot_roi_num, the program checks for proper shape of every input file.

--tot_roi_num: optional, expected number of spatial ROIs. If provided together with tot_len, the program checks for proper shape of every input file.

To use branesta in a python shell:
    import branesta.branesta


We plan to add more details here. Contact me if you need help.
