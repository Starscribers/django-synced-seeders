Installation
============

Django Synced Seeds can be installed using either uv (recommended) or pip.

Using uv (Recommended)
----------------------

.. code-block:: bash

   
   # Install django-synced-seeders
   uv add django-synced-seeders

Using pip
---------

.. code-block:: bash

   pip install django-synced-seeders

Django Settings
---------------

Add ``seeders`` to your ``INSTALLED_APPS``:

.. code-block:: python
   :linenos:

   # settings.py
   INSTALLED_APPS = [
       # ... your other apps
       'seeders',
   ]

Run Migrations
--------------

.. code-block:: bash

   python manage.py migrate

Verify Installation
-------------------

Verify the installation by running:

.. code-block:: bash

   python manage.py help | grep seed

You should see the seeder management commands listed.

Next Steps
----------

- :doc:`usage` - Learn basic commands