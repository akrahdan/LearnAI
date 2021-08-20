from django.db import models

class PublishStateOptions(models.TextChoices):
        LIVE = 'LIVE', 'Live'
        DRAFT = 'DRAFT', 'Draft'
        PENDING = 'PENDING', 'Pending'
        DELETED = 'DELETE', 'Deleted'