Contributing
============

1. Fork it.

2. Clone it

create a `virtualenv <http://pypi.python.org/pypi/virtualenv>`__

.. code:: bash

    $ virtualenv margo              # Create virtual environment
    $ source margo/bin/activate     # Change default python to virtual one
    (margo)$ git clone https://github.com/prodicus/margo.git
    (margo)$ cd margo
    (margo)$ pip install -r requirements.txt  # Install requirements for 'margo' in virtual environment

Or, if ``virtualenv`` is not installed on your system:

.. code:: bash

    $ wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    $ python virtualenv.py margo    # Create virtual environment
    $ source margo/bin/activate     # Change default python to virtual one
    (margo)$ git clone https://github.com/prodicus/margo.git
    (margo)$ cd margo
    (margo)$ pip install -r requirements.txt  # Install requirements for 'margo' in virtual environment

3. Create your feature branch (``$ git checkout -b my-new-awesome-feature``)

4. Commit your changes (``$ git commit -am 'Added <xyz> feature'``)

5. Conform to `PEP8 <https://www.python.org/dev/peps/pep-0008/>`__

6. Push to the branch (``$ git push origin my-new-awesome-feature``)

7. Create new Pull Request

Hack away!
