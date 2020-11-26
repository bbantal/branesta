========
branesta
========


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



Tool for computing brain network stability, a biomarker for brain aging.


* Free software: MIT license
* Documentation: https://branesta.readthedocs.io.

brain\_network\_instability
===========================

--------------

Please cite our article:

| Mujica-Parodi, Lilianne R., et al. "Diet modulates brain network
stability, a biomarker for brain aging, in young adults."
| Proceedings of the National Academy of Sciences 117.11 (2020):
6170-6177.

link: https://www.pnas.org/content/117/11/6170

--------------

Description:

| Brain network instability measures the extent of temporal
reorganization that takes place in brain networks. Brain networks
describe
| inter-regional communication across the brain. Higher network
instability is related to weaker persistence of brain networks.

| The procedure of computing brain network instabilities is as follows:
fMRI time-series that were previously parcelled into ROIs,
| are first binned into time windows (=snapshots) of 30 timepoints
without overlaps. Next, pairwise correlations among all ROIs are
| computed separately for each time window. For the whole brain
(=total), brain network instability (scalar) is quantified by taking
| the l2 norm of the element-wise differences of correlation matrices
corresponding to two different snapshots. τ is the number of
| steps separating two snapshots from which a given value of brain
network instability is calculated from. For instance, if τ=1, two
| consecutive snapshots snapshots are used (e.g. #4 and #5). If τ=16,
then 16 snapshots are separating the two snapshots (e.g. #3
| and #19). If the time-series have a length of 720 timepoints, then
there will be 24 snapshots (720/30=24). At τ=1, there are 23
| instability values, whereas at τ=20 4 different instability values are
calculated.

| For functional networks (labeled as "subnetworks" in our program), the
procedure is analog to above. The only difference being that
| once correlations are computed for each time window, element-wise
differences are calculated not across all ROIs, but
| only across those ROIs that spatially overlap with the functional
network. In order to facilitate comparison of network instability
| among networks consisting of different number of nodes, network
instability is normalized with the number of edges.

Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
