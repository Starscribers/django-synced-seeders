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

Handle related data carefully using priorities to ensure dependencies load first:

.. code-block:: python
   :linenos:

   # Use priority to control load order
   @seeder_registry.register()
   class CategorySeeder(Seeder):
       seed_slug = "categories"
       priority = 10  # Load first
       exporting_querysets = (Category.objects.all(),)

   @seeder_registry.register()
   class BrandSeeder(Seeder):
       seed_slug = "brands"
       priority = 10  # Load first (same priority as categories)
       exporting_querysets = (Brand.objects.all(),)

   @seeder_registry.register()
   class ProductSeeder(Seeder):
       seed_slug = "products"
       priority = 20  # Load after categories and brands
       exporting_querysets = (Product.objects.all(),)

   @seeder_registry.register()
   class ProductVariantSeeder(Seeder):
       seed_slug = "product_variants"
       priority = 30  # Load after products
       exporting_querysets = (ProductVariant.objects.all(),)

Priority Patterns for Foreign Keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you have models with foreign key relationships, use priorities to prevent database integrity errors:

.. code-block:: python
   :linenos:

   # Example: E-commerce schema
   # Country -> Region -> Store -> Employee

   @seeder_registry.register()
   class CountrySeeder(Seeder):
       seed_slug = "countries"
       priority = 1  # No dependencies
       exporting_querysets = (Country.objects.all(),)

   @seeder_registry.register()
   class RegionSeeder(Seeder):
       seed_slug = "regions"
       priority = 2  # Depends on Country
       exporting_querysets = (Region.objects.all(),)

   @seeder_registry.register()
   class StoreSeeder(Seeder):
       seed_slug = "stores"
       priority = 3  # Depends on Region
       exporting_querysets = (Store.objects.all(),)

   @seeder_registry.register()
   class EmployeeSeeder(Seeder):
       seed_slug = "employees"
       priority = 4  # Depends on Store
       exporting_querysets = (Employee.objects.all(),)

Tagging Strategy
~~~~~~~~~~~~~~~~

Use tags to organize seeders by purpose and environment:

.. code-block:: python
   :linenos:

   # Testing tags - organize by test type
   @seeder_registry.register(tags="e2e")
   class E2EUserSeeder(Seeder):
       seed_slug = "e2e_users"
       exporting_querysets = (User.objects.all(),)

   @seeder_registry.register(tags=["integration", "e2e"])
   class IntegrationTestSeeder(Seeder):
       seed_slug = "integration_data"
       exporting_querysets = (Product.objects.all(),)

   # Environment tags - organize by deployment stage
   @seeder_registry.register(tags="development")
   class DevSampleDataSeeder(Seeder):
       seed_slug = "dev_samples"
       exporting_querysets = (Product.objects.all(),)

   @seeder_registry.register(tags="demo")
   class DemoSeeder(Seeder):
       seed_slug = "demo_showcase"
       exporting_querysets = (Product.objects.all(),)

   # Data category tags - organize by data type
   @seeder_registry.register(tags="base")
   class BaseConfigSeeder(Seeder):
       seed_slug = "base_config"
       exporting_querysets = (
           Settings.objects.all(),
           Roles.objects.all(),
       )

Recommended Tag Conventions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Testing Environments:**

- ``e2e`` - End-to-end test data
- ``integration`` - Integration test fixtures
- ``unit`` - Unit test data
- ``performance`` - Performance test datasets

**Deployment Stages:**

- ``development`` - Development environment data
- ``staging`` - Staging environment data
- ``demo`` - Demo/showcase data
- ``production`` - Production-safe reference data

**Data Categories:**

- ``base`` - Essential base data (users, roles, settings)
- ``reference`` - Reference data (countries, currencies)
- ``sample`` - Sample content for testing
- ``migration`` - Data migration seeders

**Best Practices for Tags:**

- Use lowercase names for consistency
- Keep tag names short and descriptive
- Document your tagging convention in README
- Don't over-tag - 1-3 tags per seeder is usually enough
- Use tags to enable selective deployment

.. code-block:: bash

   # In CI/CD pipelines
   # Development: Load all development data
   python manage.py syncseeds development

   # Staging: Load demo and integration test data
   python manage.py syncseeds demo integration

   # Production: Load only base reference data
   python manage.py syncseeds base reference

   # E2E tests: Load only test-specific data
   python manage.py syncseeds e2e

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



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
