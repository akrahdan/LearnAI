from django.db import models

class PublishStateOptions(models.TextChoices):
        LIVE = 'LIVE', 'Live'
        DRAFT = 'DR', 'Draft'
        PENDING = 'PD', 'Pending'
        DELETED = 'DEL', 'Deleted'