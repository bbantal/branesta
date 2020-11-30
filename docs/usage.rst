=====
Usage
=====

To diplay options, simply run the following line in terminaal

.. code-block:: console

    $ branesta -h

The following options will be available

.. code-block:: console

    usage: branesta [-h] [--subnetpath SUBNETPATH] [--tot_len TOT_LEN]
                    [--tot_roi_num TOT_ROI_NUM]
                    srcdir outdir win_len
    
    positional arguments:
      srcdir                path to source directory with time-series
      outdir                path to out directory for results and logs
      win_len               number of time-frames in each snapshot
    
    optional arguments:
      -h, --help            show this help message and exit
      --subnetpath, -s
                            path to csv file with subnetwork labels and ixs,
                            optional
      --tot_len, -l
                            expected total number of time frames, optional
      --tot_roi_num, -r
                            expected total number of ROIs, optional

The options are explained below in more details:

* srcdir: path to times-series to analyze. There are certain requirements for the input time-series:
1. Must be parcelled into ROIs, should not be more than a few hundred ROIs.
2. Shape must be 2D: time x space
3. File format must be .csv with no header row or index column
4. Filenames must follow BIDS convention (https://bids.neuroimaging.io/)
(see example time-series for reference)

* outdir: path to output directory. Computed metrics and log files will be placed here.

* win_len: number of time-frames within each time window. With a TR of ~1s, at least 30 is recommended. The more regions we use, the more time-frames we need to properly estimate the covariance matrix

* --subnetpath: optional, path to subnetwork indexes file. If provided, network stability is computed separately for edges corresponding to subnetworks. If not provided, the program defaults to a default subnetwork (labeled as whole_brain) consisting of all ROIs. Must be a .csv with two columns and a header row (roi, network).
(see example subnetworks_willard.csv for reference)

* --tot_len: optional, expected length of input time-series. If provided together with tot_roi_num, the program checks for proper shape of every input file.

* --tot_roi_num: optional, expected number of spatial ROIs. If provided together with tot_len, the program checks for proper shape of every input file.

To use branesta in a python shell:

.. code-block:: console

    import branesta.branesta


We plan to add more details here. Contact Botond Antal if you need help.
