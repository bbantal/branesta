=======================
BRAin NEtwork STAbility
=======================


.. image:: https://img.shields.io/pypi/v/branesta.svg
        :target: https://pypi.python.org/pypi/branesta

.. image:: https://img.shields.io/travis/BotondA/branesta.svg
        :target: https://travis-ci.com/BotondA/branesta

.. image:: https://readthedocs.org/projects/branesta/badge/?version=latest
        :target: https://branesta.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/BotondA/branesta/shield.svg
     :target: https://pyup.io/repos/github/BotondA/branesta/
     :alt: Updates

.. image:: https://img.shields.io/badge/License-MIT-brightgreen.svg
     :target: https://opensource.org/licenses/MIT

Introduction
------------

Tool for computing brain network stability, a biomarker for brain aging.

* Free software: MIT license
* Documentation: https://branesta.readthedocs.io.

Please cite our article:

Mujica-Parodi, Lilianne R., et al. "Diet modulates brain network stability, a biomarker for brain aging, in young adults." Proceedings of the National Academy of Sciences 117.11 (2020): 6170-6177.
link: https://www.pnas.org/content/117/11/6170


Description
------------

Brain network stability measures the extent of temporal reorganization that takes place in brain networks. Brain networks describe inter-regional communication across the brain. Lower network stability (represented by higher values) is related to weaker persistence of brain networks. Network stability and network instability are used interchangibly. When it comes to the metric itself, both expressions refer to the exact same.

The procedure of computing brain network stability is as follows: fMRI time-series that were previously parcelled into ROIs are first binned into time windows (=snapshots) of N timepoints without overlaps. Next, pairwise correlations among all ROIs are computed separately for each time window. For the whole brain, brain network stability (scalar) is quantified by taking the l2 norm of the element-wise differences of correlation matrices corresponding to two different snapshots. τ is the number of steps separating two snapshots from which a given value of brain network stability is calculated from. For instance, if τ=1, two consecutive snapshots snapshots are used (e.g. #4 and #5). If τ=16, then 16 snapshots are separating the two snapshots (e.g. #3 and #19). If the time-series have a length of 720 timepoints, then there will be 24 snapshots (720/30=24, given N=30). At τ=1, there are 23 instability values, whereas at τ=20 4 different instability values are calculated.

For functional networks (labeled as "subnetworks" in our program), the procedure is analog to the above. The only difference is that once correlations are computed for each time window, element-wise differences are calculated only across those ROIs that spatially overlap with the functional network. In order to facilitate comparison of network instability among networks consisting of different number of nodes, network stability is normalized with the number of edges. 

Features
--------

This is a command line tool, allowing execution with a single line. It computes network stability at every tau value, and optionally for multiple subnetworks.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
