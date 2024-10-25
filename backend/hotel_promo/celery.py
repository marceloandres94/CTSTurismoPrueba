from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Configuración del módulo de Django para Celery.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_promo.settings')

# Creación de la instancia de Celery con el nombre del proyecto.
app = Celery('hotel_promo')

# Configuración de Celery para leer opciones desde las configuraciones de Django, usando el prefijo CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscovery: Celery buscará automáticamente tareas en cada aplicación de Django registrada en INSTALLED_APPS
app.autodiscover_tasks()
