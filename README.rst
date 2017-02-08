===================================
Upload portal of the c-VEDA project
===================================

Neuroimaging datasets are uploaded by acquisition centres to the upload portal
for further processing by the databank team.

The upload portal is conceptually part of `c-VEDA databank operations`_ but
the source code lives in its own repository. It is a Python module, based on
PIWS_ / rql_upload_, which in turn are based on the CubicWeb_ semantic web
framework. It runs basic sanity checks on uploaded datasets.
The sanity check code is imported from the cveda_databank_ module.

.. _`c-VEDA databank operations`: https://github.com/cveda/cveda_databank/wiki
.. _PIWS: https://github.com/neurospin/piws
.. _rql_upload: https://github.com/neurospin/rql_upload
.. _CubicWeb: http://cubicweb.readthedocs.io
.. _cveda_databank: https://github.com/cveda/cveda_databank
