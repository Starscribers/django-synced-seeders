Usage
=====

This guide covers the basic usage patterns for Django Synced Seeds.

Management Commands
-------------------

Django Synced Seeds provides several management commands:

Export Seeds
~~~~~~~~~~~~

Export seed data from your current environment:

.. code-block:: bash

   python manage.py exportseed <seeder_slug>

   # Example
   python manage.py exportseed categories

Sync Seeds
~~~~~~~~~~

Sync all available seeds to the current environment:

.. code-block:: bash

   python manage.py syncseeds

Creating Seeders
----------------

Create a seeder by subclassing ``Seeder`` and registering it:

.. code-block:: python
   :linenos:

   # myapp/seeders.py
   from seeds import seeder_registry, Seeder
   from .models import Category

   @seeder_registry.register()
   class CategorySeeder(Seeder):
       seed_slug = "categories"
       exporting_querysets = (Category.objects.all(),)

Auto-discovery
---------------

The seeder registry automatically discovers seeders in your installed apps.

Auto-discovery looks for ``seeders.py`` files in each app.

Version Management
------------------

Seeders automatically track versions using revision numbers.

Each time you export data, a new revision is created.

During sync, only newer revisions are imported.

Next Steps
----------

- :doc:`best-practices` - Learn best practices for using seeders
