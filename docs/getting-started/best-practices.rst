Best Practices
==============

Production-ready patterns and recommendations for Django Synced Seeds.

Seeder Design
-------------

Keep It Simple
~~~~~~~~~~~~~~

- One seeder per logical data group
- Use descriptive ``seed_slug`` names
- Avoid complex inheritance hierarchies

.. code-block:: python
   :linenos:

   # Good: Focused and clear
   @seeder_registry.register()
   class CategorySeeder(Seeder):
       seed_slug = "categories"
       exporting_querysets = (Category.objects.all(),)

   # Avoid: Too broad and complex
   class EverythingSeeder(Seeder):
       seed_slug = "everything"  # Too vague
       exporting_querysets = (
           User.objects.all(),
           Product.objects.all(),
           Order.objects.all(),  # Unrelated to categories
           # ... many more
       )

Data Relationships
~~~~~~~~~~~~~~~~~~

Handle related data carefully:

.. code-block:: python
   :linenos:

   # Include related models in logical order
   @seeder_registry.register()
   class ProductSeeder(Seeder):
       seed_slug = "products"
       exporting_querysets = (
           Category.objects.all(),      # Dependencies first
           Brand.objects.all(),         # Dependencies first
           Product.objects.all(),       # Main model
           ProductVariant.objects.all(), # Dependent models last
       )

Version Control
---------------

Seed File Management
~~~~~~~~~~~~~~~~~~~~

- Commit seed files to version control
- Use meaningful commit messages
- Tag releases that include seed updates

.. code-block:: bash

   # Good commit practices
   git add seeds/
   git commit -m "feat(seeds): add initial product categories

   - Add 12 main categories
   - Include subcategories for electronics
   - Update revision to v3"

   # Tag important releases
   git tag -a v1.2.0 -m "Release with updated seed data"

Branching Strategy
~~~~~~~~~~~~~~~~~~

- Keep seed changes in feature branches
- Review seed updates like code changes
- Test seed updates in staging before production

Environment Management
----------------------

Auto-sync in entrypoint scripts
~~~~~~~~~~~~~~~~~~



.. code-block:: bash

   ...
   python manage.py migrate --dry-run

   python manage.py syncseeds # <- Add this line

   python manage.py runserver

Testing Strategy
----------------

Unit Tests
~~~~~~~~~~

Init seed data in tests:

.. code-block:: python
    :linenos:

    # conftest.py
    import pytest
    from django.core.management import call_command
    from shop.models import Category, Product
    @pytest.fixture(scope='session', autouse=True)
    def load_seed_data():
        """Load seed data once per test session."""
        call_command('syncseeds')
