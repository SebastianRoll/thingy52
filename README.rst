=========
Thingy:52
=========


.. image:: https://img.shields.io/pypi/v/thingy52.svg
        :target: https://pypi.python.org/pypi/thingy52

.. image:: https://img.shields.io/travis/SebastianRoll/thingy52.svg
        :target: https://travis-ci.org/SebastianRoll/thingy52

.. image:: https://readthedocs.org/projects/thingy52/badge/?version=latest
        :target: https://thingy52.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/SebastianRoll/thingy52/shield.svg
     :target: https://pyup.io/repos/github/SebastianRoll/thingy52/
     :alt: Updates


Python interface to Thingy:52

.. image:: demos/demo_camera_udp.gif

* Free software: MIT license
* Documentation: https://thingy52.readthedocs.io. <- coming soon

This package is an implementation of a Python interface for the Thingy:52 ble IoT Sensor Kit.

More information about Thingy:52 is found here: https://www.nordicsemi.com/eng/Products/Nordic-Thingy-52

Full disclosure: A reference implementation for thingy:52 already exists in the popular bluepy package:

https://github.com/IanHarvey/bluepy

Install
-------

Python 2 support <- coming soon.

Python 3:

.. highlight:: bash

    $ sudo apt-get install libglib2.0-dev
    $ pip3 install thingy52

If you find bluepy-helper isn't being built, please try:

.. highlight:: bash

    $ pip install --no-binary :all: thingy52

To use the recording demo (/demo/record.py) you will need the PyAudio package (https://people.csail.mit.edu/hubert/pyaudio/).

Features
--------

* CLI interface using Click

* Data conversion functions for all sensors (not yet fully complete)

* Some fun demos to get you started


BUGS
----

The first connection attempt after turning on the thingy:52 usually fails, but it works after that.


TODO
----

- [ ] Python 2.X

- [X] Python 3.X

- [ ] Implementation

  - [X] Toggle notify

  - [ ] Notification frequency

  - [X] Read/Write

  - [X] Services

    - [X] Environment

    - [X] Motion

    - [X] User Interface

    - [ ] Audio

- [ ] Documentation

  - [ ] Installation

  - [ ] Usage

  - [ ] Convert docs to markdown

  - [ ] Badges (CI, Readthedocs)

  - [ ] Photo of thingy:52

  - [ ] Gif of demo (controlling Picam)

- [ ] Distribution

  - [ ] Conda package (conda-forge)

  - [X] Pypi package

More information
----------------

* https://nordicsemiconductor.github.io/Nordic-Thingy52-FW/documentation/firmware_architecture.html
* https://infocenter.nordicsemi.com/index.jsp?topic=%2Fcom.nordic.infocenter.rds%2Fdita%2Frds%2Fdesigns%2Fthingy%2Fhw_description%2Fhw_descr.html&cp=9_0_6

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

