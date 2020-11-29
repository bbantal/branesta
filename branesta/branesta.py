#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 01:01:19 2020

@author: botond antal

Notes:
    This application computes network stability from a set of time-series.
"""

import os
import argparse
import logging
import numpy as np
import pandas as pd
import itertools
from nilearn.connectome import ConnectivityMeasure


class NetworkMetricsPipeline:
    """
    Class with methods for calculating network stability
    from ROI space time-series
    """

    def __init__(self, roi_time_series):

        # Convert input time_series to numpy array
        self.roi_time_series = np.array(roi_time_series)

    def calc_windows(self, win_len):
        """
        Divides time-series up into time windows
        """

        # Number of windows-1
        num = int((self.roi_time_series.shape[0] - 1 - \
                   (self.roi_time_series.shape[0] - 1) % win_len) /
                  win_len)

        # Indicies at which slicing should occur
        indicies = np.linspace(win_len, num*win_len, num) \
                        .astype(int)

        # 30 frame long time windows (last window might be shorter)
        windows = np.split(self.roi_time_series, indicies, axis=0)

        # Remove last window if shorter than window_size
        windows = windows[:-1] \
            if self.roi_time_series.shape[0] % win_len > 0 \
            else windows

        # Given that all dimensions are consistent, convert list to np array
        self.windows = np.array(windows)

        return self

    def calc_corrs(self):
        """
        Calculates correlations between ROIs
        """

        # Take pairwise correlation of ROI tracers separately within all windows
        correlation_measure = ConnectivityMeasure(kind='correlation')
        self.corr_matrices = correlation_measure.fit_transform(self.windows)

        return self

    def calc_stab(self, subnet_ixs):
        """
        Calculates network stability
        """

        # Array of tau values
        self.tau_vals = np.arange(1, len(self.corr_matrices))

        # Array for storing normalized stability values
        self.stability = [None] * len(self.tau_vals)

        # Iterate over all taus
        for i, tau in enumerate(self.tau_vals):

            # Pairs of windows at a given tau between which the element-wise
            # differences of correlations will be calculated between
            window_pairs = [[start, start + tau] \
                       for start in range(len(self.corr_matrices) - tau)]

            # Calculate elementwise differences
            corr_diffs_ls = [np.diff(
                                (self.corr_matrices[win1],
                                 self.corr_matrices[win2]),
                                     axis=0) \
                                 for win1, win2 in window_pairs]

            # Concatenate elementwise differences
            corr_diffs = np.concatenate(corr_diffs_ls)

            # Preallocate for temporarily storing stability values,
            # filled with nans
            subnets_stab = np.full(
                    (len(subnet_ixs), len(self.tau_vals)), np.nan)

            # Iterate over all fROIs
            for j, ixs in enumerate(subnet_ixs.values()):

                # Extract corr_diffs corresponding to fROI
                subnet_corr_diffs = corr_diffs[:, ixs[0], ixs[1]]

                # Take l2norm
                stabs_prenorm = \
                    np.linalg.norm(subnet_corr_diffs, axis=1)

                # Normalize with sqroot of number of non-main-diagonal values
                subnets_stab[j][:len(corr_diffs)] =  stabs_prenorm/ \
                    np.sqrt(np.sqrt(len(ixs.T))*(np.sqrt(len(ixs.T))-1))

            # Store computed stability values
            self.stability[i] = list(subnets_stab.T)

        return self

    def convert_stab_to_df(self, meta, subnet_ixs):
        """
        Converts computed stability values to dataframe
        """

        # Indexes
        mtx = pd.MultiIndex.from_frame(
                 pd.DataFrame(
                         itertools.product(
                                 self.tau_vals,
                                 self.tau_vals,
                                 list(subnet_ixs.keys()))) \
                    .T.set_index(pd.Index(["tau", "time", "subnetwork"])).T \
                    .assign(**meta) \
                    .loc[:, list(meta.keys()) + ["tau", "time", "subnetwork"]])

        # Construct dataframe of stabilitities for current instance
        self.df = pd \
            .DataFrame(self.stability) \
            .T.melt() \
            .drop(labels="variable", axis=1) \
            .explode(column="value") \
            .set_index(mtx) \
            .rename({"value": "stability"}, axis=1)

        return self


def compute_network_stability(
        file, meta={}, srcdir=None, win_len=30, subnet_ixs={},
        tot_roi_num=None, tot_len=None):

    """
    Wrapper function for calculating stability values for a single time-series
    entity which was already preprocessed and converted into ROI space

    Parameters
    ----------
    file: str
        name of file containing time-series, located in srcdir, must follow BIDS
        naming convention. Shape must be: [samples, channels] or [time, space]
    srcdir: str
        path to source directory with containing data files
    win_len: int
        number of frames in time windows/snapshots considered for computing
        network stability
    subnet_ixs: dict
        dictionary of indexes specific to functional ROIs, the format is
        {key=func_label of the fROI, value=2D array of the product of
        ROI indexes included in the fROI},
        examples for labels: "whole_brain", "visuospatial", "auditory"
    tot_roi_num: int
        optional, total number of ROIs expected in time-series
    tot_len: int
        optional, total number of time frames expected in time-series
    """

    # Load data
    # --------

    # Status
    text = f"Loading {file}"
#    print(text)
    logging.info(text)

    # Construct meta data according to BIDS
    # example: {'sub': '057', 'ses': 'glc', 'task': 'task', 'run': '2'}
    file_info = file.split(".")[0].split("_")
    meta = {}

    for item in file_info:
        id_, info = item.split("-")
        meta[id_] = info

    # Load ROI space time-series
    roi_time_series = pd.read_csv(os.path.join(srcdir, file),
                                  header=None, index_col=False)
    roi_time_series = np.array(roi_time_series)

    # Add subnetwork with all ROIs called whole brain
    subnet_ixs["whole_brain"] = \
        np.array(list(itertools.product(
                np.arange(roi_time_series.shape[1]),
                np.arange(roi_time_series.shape[1])))).T

    # Check shape of time-series if expected values are provided
    if tot_len and tot_roi_num:
        if roi_time_series.shape != (tot_len, tot_roi_num):
            text = f"\n[!] Abnormal shape {roi_time_series.shape} in item: " \
            f"{file}! Item will be excluded!\n"
#            print(text)
            logging.warning(text)
            return

    # Check for zero/close-to-zero ROIs
    roi_means =  np.mean(np.abs(roi_time_series), axis=0)
    zero_rois = np.argwhere(roi_means < 1e-10)
    if len(zero_rois) > 0:
        text = f"[!] Zero ROI(s) {zero_rois} found in item: {file}! Proceeding."
#        print(text)
        logging.warning(text)

    # Compute metrics
    # -------

    # Status
    text = f"Computing metrics for {file}"
#    print(text)
    logging.info(text)

    # Compute stability
    df = NetworkMetricsPipeline(roi_time_series) \
        .calc_windows(win_len) \
        .calc_corrs() \
        .calc_stab(subnet_ixs) \
        .convert_stab_to_df(meta, subnet_ixs) \
        .df

    # Status
    text = f"Finished computations for {file}"
#    print(text)
    logging.info(text)

    # Returns
    return df


def analyze(ver, srcdir, outdir, subnetpath=None, **opts):
    """
    Computes network stability for files in srcdir. Considers only
    .csv files. Naming must follow BIDS format.

    Parameters
    ----------
    ver: str
        version of current analysis
    srcdir: str
        path to directory with data files to analyze
    outdir: dict
        path where results are dumped
    subnetpath: str
        path to csv with subnetwork labels and indexes
    opts: dict
        dictionary with optional keyword arguments for computations
    """

    # Set up logger
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        handlers=[
                                logging.FileHandler(
                                    filename=os.path.join(outdir, f"{ver}.log")),
                                logging.StreamHandler()],
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Dict to store edge indexes for each subnetwork
    subnet_ixs = {}

    # If path was given, fill up subnet labels and ixs
    if subnetpath:

        # Import subnetwork labels and ROI indexes
        subnet_data = pd.read_csv(subnetpath)

        # Get subnet labels
        subnet_labels = subnet_data["network"].unique()

        # Iterate over all subnetworks
        for label in subnet_labels:

            # Extract ROI indexes found within fROI
            ids = subnet_data \
                .loc[subnet_data["network"] == label, "roi"].to_numpy() - 1

            # Assign combinations of ROI indexes representing edges within subnet
            subnet_ixs[f"{label}"] = np.array(list(itertools.product(ids, ids))).T


    # Build analysis_kwargs dict
    analysis_kwargs = {"srcdir": srcdir, "subnet_ixs": subnet_ixs, **opts}

    # Status
    text = 'Starting analysis with the following settings:\n' \
           + "\n".join([": ".join([str(key), str(value)]) \
                        if key != "subnet_ixs" else  \
                        ": ".join([str(key), str(list(value.keys()))]) \
                        for key, value in analysis_kwargs.items()])
#    print(text)
    logging.info(text)

    # Collect files to analyze
    files = sorted([file for file in os.listdir(srcdir) if ".csv" in file])

    # Initiate collection of outputs
    out = []

    # Analyze files
    for file in files:

        # Compute metrics
        res = compute_network_stability(
                file=file,
                **analysis_kwargs
                )

        # If file was not skipped and output exists
        if type(res) == pd.DataFrame:

            # Append results to collection of outputs
            out.append(res)

    # Convert outputs pandas dataframe and write into csv
    pd.concat(out, axis=0).to_csv(os.path.join(outdir, f"brain_network_stability_{ver}.csv"))

    # Status
    text = f"Analysis has finished. Number of files analyzed: {len(out)}."
#    print(text)
    logging.info(text)

    # Shut down logging
    logging.shutdown()


