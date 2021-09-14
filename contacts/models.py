import logging

from django.db import models

logger = logging.getLogger('main')


class Contact(models.Model):
    first_name = models.CharField(null=False, blank=False, max_length=512)
