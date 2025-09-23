"""
Django Synced Seeders

A flexible framework for managing and syncing database seed data in Django applications.
Uses the registry pattern to allow easy extension with custom seeder backends.
"""

from .registries import seeder_registry
from .seeders import Seeder

__version__ = "0.1.0"
__all__ = [
    "seeder_registry",
    "Seeder",
]
