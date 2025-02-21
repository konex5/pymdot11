.. _pyfhmdot: https://nokx5.github.io/golden-python

========================================
Welcome to the `pyfhmdot`_ project!
========================================

|CILinuxBadge|_ |CIDarwinBadge|_ |DocBadge|_ |LicenseBadge|_

.. |CILinuxBadge| image:: https://github.com/nokx5/pyfhmdot/workflows/CI-linux/badge.svg
.. _CILinuxBadge: https://github.com/nokx5/pyfhmdot/actions/workflows/ci-linux.yml
.. |CIDarwinBadge| image:: https://github.com/nokx5/pyfhmdot/workflows/CI-darwin/badge.svg
.. _CIDarwinBadge: https://github.com/nokx5/pyfhmdot/actions/workflows/ci-darwin.yml
.. |DocBadge| image:: https://github.com/nokx5/pyfhmdot/workflows/doc-api/badge.svg
.. _DocBadge: https://nokx5.github.io/pyfhmdot
.. |LicenseBadge| image:: http://img.shields.io/badge/license-MIT-blue.svg
.. _LicenseBadge: https://github.com/nokx5/pyfhmdot/blob/master/LICENSE

This project consists in giving a nice gate application interface to
the python layer in a way one can chain them easily. Please find below
the documentation `here <https://nokx5.github.io/pyfhmdot>`_ and the
source code `there <https://github.com/nokx5/pyfhmdot>`_.

.. warning:: **NOTE:** the project is developed using the nix ❄️
             packaging manager, but everything can be compiled by
             hand.

The dependency
========================

* mdot (C++)
* fhmdot (C++/pybind11)
* numpy
* scipy (pytests)
* sphinx (docs)


Use the software
================

Open python and invoke

.. code:: shell

    import pyfhmdot as pyf
    import numpy as np
    a = pyf.import({(1,1,1,1) : np.ndarray([[[[1]]]]))
    b = pyf.import({(1,1,1,1) : np.ndarray([[[[1]]]]))
    theta = pyf.import({(1,1,1,1) : np.ndarray([[[[1]]]]))
    c = pyf.apply(theta,pyfa,pyfb)


Install the software
--------------------

You can not use pip since one of the dependency is compiled from C++.
Start by cloning all dependencies in the same folder. You can clone
`git repository <https://github.com/nokx5/pyfhmdot>`_ them locally.

=============
Code Snippets
=============

.. code:: shell

    black .

    nixpkgs-fmt .

    pip install $(cat requirements.txt) # works for pure python only

    pip list --format=freeze | sed 's/==/>=/g' > requirements.txt

    python -m pytest -k "not bronze"

=======
License
=======

You may copy, distribute and modify the software provided that
modifications are described and licensed for free under the `MIT
<https://opensource.org/licenses/MIT>`_.
