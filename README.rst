TIPS-API
--------

Tips-api delivers tip content for Mijn-Amsterdam.

Ontwikkelling
-------------

Tests
=====
* activate virtual env
* :code:`python -m unittest`


Updating Dependencies
=====================
Direct dependencies are specified in `requirements-root.txt`. These should not have pinned a version (except when needed)

* ``pip install -r requirements-root.txt``
* ``echo "--extra-index-url https://nexus.secure.amsterdam.nl/repository/pypi-hosted/simple" > requirements.txt && pip freeze >> requirements.txt``

