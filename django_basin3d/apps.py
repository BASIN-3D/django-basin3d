from django.apps import AppConfig
from django.db.models.signals import post_migrate

from django_basin3d.catalog import reload_data_sources


class Basin3DConfig(AppConfig):
    name = 'django_basin3d'

    def ready(self):
        # Execute the post migration scripts
        post_migrate.connect(reload_data_sources, sender=self)
