Django Synced Seeds Documentation
======================================

.. image:: https://badge.fury.io/py/django-synced-seeders.svg
   :target: https://badge.fury.io/py/django-synced-seeders
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/django-synced-seeders.svg
   :target: https://pypi.org/project/django-synced-seeders/
   :alt: Python Support

.. image:: https://img.shields.io/badge/Django-4.2%2B-brightgreen.svg
   :target: https://www.djangoproject.com/
   :alt: Django Support

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

.. image:: https://github.com/Starscribers/django-synced-seeders/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/Starscribers/django-synced-seeders/actions
   :alt: Tests

An easy-to-use seeder manager to keep seed data in sync across multiple environments. Perfect for managing reference data, initial configurations, and test data across development, staging, and production environments.

Features
--------

**Version Control for Seeds** - Track and manage seed versions with automatic revision tracking

**Environment Sync** - Keep data consistent across development, staging, and production

**Export & Import** - Easy data export from any environment and import to others

**Selective Loading** - Load only the seeds you need with intelligent version checking

**Django Integration** - Built specifically for Django with full ORM support

**Test-Friendly** - Comprehensive test suite with function-based tests

**Extensible** - Easy to extend with custom seeders for your specific needs

Quick Start
-----------

Install django-synced-seeders:

**Using uv (Recommended)**

.. code-block:: bash
   # Install django-synced-seeders
   uv add django-synced-seeders

**Using pip**

.. code-block:: bash

   pip install django-synced-seeders

Add to your Django settings:

.. code-block:: python
   :linenos:

   # settings.py
   INSTALLED_APPS = [
       # ... your apps
       'seeders',
   ]

Run migrations:

.. code-block:: bash

   python manage.py migrate

Create your first seeder:

.. code-block:: python
   :linenos:

   # myapp/seeders.py
   from seeds import seeder_registry, Seeder
   from .models import Category

   @seeder_registry.register()
   class CategorySeeder(Seeder):
       seed_slug = "categories"
       exporting_querysets = (Category.objects.all(),)

Export and sync data:

.. code-block:: bash

   # Export data from current environment
   python manage.py exportseed categories
   # Sync to another environment
   python manage.py syncseeds

License
-------

This project is licensed under the MIT License.

----

**Happy coding!**

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   getting-started/installation
   getting-started/usage
   getting-started/best-practices

.. toctree::
   :maxdepth: 2
   :caption: Guides

   guides/concepts
   guides/examples


Community
---------

* **GitHub**: `Source code and issues <https://github.com/Starscribers/django-synced-seeders>`_
* **PyPI**: `Package releases <https://pypi.org/project/django-synced-seeders/>`_
* **Discord**: `Community chat <https://discord.gg/ngE8JxjDx7>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Features
--------

**Version Control for Seeds** - Track and manage seed versions with automatic revision tracking

**Environment Sync** - Keep data consistent across development, staging, and production

**Export & Import** - Easy data export from any environment and import to others

**Selective Loading** - Load only the seeds you need with intelligent version checking

**Django Integration** - Built specifically for Django with full ORM support

**Test-Friendly** - Comprehensive test suite with function-based tests

**Extensible** - Easy to extend with custom seeders for your specific needs

Quick Start
-----------

.. code-block:: bash

   pip install django-synced-seeders

Add to your Django settings:

.. code-block:: python
   :linenos:

   # settings.py
   INSTALLED_APPS = [
       # ... your apps
       'seeders',
   ]

Run migrations:

.. code-block:: bash

   python manage.py migrate

Create your first seeder:

.. code-block:: python
   :linenos:

   # myapp/seeders.py
   from seeds import seeder_registry, Seeder
   from .models import Category

   @seeder_registry.register()
   class CategorySeeder(Seeder):
       seed_slug = "categories"
       exporting_querysets = (Category.objects.all(),)

Export and sync data:

.. code-block:: bash

   # Export data
   python manage.py exportseed categories

   # Sync to another environment
   python manage.py syncseeds

Community
---------

* **GitHub**: `Source code and issues <https://github.com/Starscribers/django-synced-seeders>`_
* **PyPI**: `Package releases <https://pypi.org/project/django-synced-seeders/>`_
* **Discord**: `Community chat <https://discord.gg/ngE8JxjDx7>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
