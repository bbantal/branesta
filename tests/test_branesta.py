#!/usr/bin/env python

"""Tests for `branesta` package."""

import os
import glob
import unittest
import pandas as pd

from branesta import branesta


class TestBranesta(unittest.TestCase):
    """Tests for `branesta` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

        # Run branesta, output results into temp dir
        branesta.analyze(
                "tests", "tests/testdata/ts", "tests/temp/", win_len=30,
                subnetpath="tests/testdata/subnets/subnetworks_willard.csv",
                tot_len=720, tot_roi_num=498
            )

    def tearDown(self):
        """Tear down test fixtures, if any."""

        # Delete temp outputs
        os.system("rm tests/temp/*")


    def test_branesta(self):
        """Test whether output csv with stability values is as expected."""

        # Open output
        out = pd.read_csv("tests/temp/brain_network_stability_tests.csv")

        # Open reference
        ref = pd.read_csv(glob.glob("tests/ref/brain_network_stability_*.csv")[-1])

        # Print some info
        print("Info from test-case:", "\nshape:", out.shape, "\nhead:\n", out.head())

        # Assert equality
        pd.testing.assert_frame_equal(out, ref)

