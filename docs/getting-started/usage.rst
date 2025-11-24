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

   # Sync only seeders with specific tags
   python manage.py syncseeds e2e

   # Sync multiple tags (union of all matching seeders)
   python manage.py syncseeds e2e development

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

Tagging Seeders
---------------

Organize seeders with tags for targeted execution. This is useful for different testing scenarios or deployment strategies.

Single Tag
~~~~~~~~~~

Register a seeder with a single tag:

.. code-block:: python
   :linenos:

   # myapp/seeders.py
   from seeds import seeder_registry, Seeder
   from .models import User

   @seeder_registry.register(tags="e2e")
   class E2ETestSeeder(Seeder):
       seed_slug = "e2e_test_data"
       exporting_querysets = (User.objects.all(),)

Multiple Tags
~~~~~~~~~~~~~

Register a seeder with multiple tags:

.. code-block:: python
   :linenos:

   # myapp/seeders.py
   from seeds import seeder_registry, Seeder
   from .models import Product

   @seeder_registry.register(tags=["development", "demo"])
   class DemoSeeder(Seeder):
       seed_slug = "demo_data"
       exporting_querysets = (Product.objects.all(),)

Running Tagged Seeders
~~~~~~~~~~~~~~~~~~~~~~

Execute seeders by tag:

.. code-block:: bash

   # Sync only e2e tagged seeders
   python manage.py syncseeds e2e

   # Sync multiple tags (union of all matching seeders)
   python manage.py syncseeds e2e development

   # Sync all seeders (default behavior)
   python manage.py syncseeds

Common Use Cases
~~~~~~~~~~~~~~~~

**Testing Environments:**

- ``e2e`` - End-to-end test data
- ``integration`` - Integration test data
- ``unit`` - Unit test data

**Deployment Stages:**

- ``development`` - Development environment data
- ``staging`` - Staging environment data
- ``demo`` - Demo/showcase data

**Data Categories:**

- ``base`` - Essential base data (users, roles)
- ``sample`` - Sample content for testing
- ``reference`` - Reference data (countries, currencies)

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
