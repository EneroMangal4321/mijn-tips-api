TIPS-API
--------

Tips-api delivers tip content for Mijn-Amsterdam.

Ontwikkelling
-------------

Running it
==========
* Activate/create virtual env
* :code:`pip install -r requirements.txt`
* :code:`export FLASK_APP=tips.server`
* :code:`flask run`

Tests
=====
* Activate/create virtual env
* :code:`pip install -r requirements.txt`
* :code:`python -m unittest`


Updating Dependencies
=====================
Direct dependencies are specified in `requirements-root.txt`. These should not have pinned a version (except when needed)
This works best with a new/temporary virtualenv.

* :code:`pip install -r requirements-root.txt`
* :code:`requirements.txt && pip freeze >> requirements.txt`

