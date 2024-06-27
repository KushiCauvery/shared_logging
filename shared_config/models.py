from django.db import models
from .notification_constants import SMS_SENT_STATUS
from django.contrib.postgres.fields import ArrayField

class ModelBase(models.Model):
    """
        This is a abstract model class to add is_deleted, created_at and modified at fields in any model
    """
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class EmailStatus(ModelBase):
    """
    stores sms related data
    """
    type = models.CharField(max_length=255)
    message_text = models.TextField()
    to_email = models.CharField(max_length=255)
    from_email = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default=SMS_SENT_STATUS)
    sent_at = models.CharField(max_length=255, default="9999-12-31 23:59:59")
    done_at = models.CharField(max_length=255, default="9999-12-31 23:59:59")
    delivery_status = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'notification_emailstatus'
        managed = False
        app_label = 'notification'

class AppConfigurations(ModelBase):
    """
    model to save product versions and force update status
    """
    app_os = models.CharField(max_length=20)
    version_name = models.CharField(max_length=20, blank=True, null=True)
    version_code = models.IntegerField(blank=True, null=True)
    build_number = models.IntegerField(blank=True, null=True)
    specific_version_update = ArrayField(models.CharField(max_length=20), blank=True, null=True, default=list)
    is_force_update = models.BooleanField(default=False)
    force_update_message = models.TextField(default="")

    class Meta:
        db_table = 'renderer_appconfigurations'
        managed = False
        app_label = 'renderer'