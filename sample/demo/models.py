from django.db import models

# Create your models here.
class DemoModel(models.Model):
    master = models.ForeignKey('renderer.MasterImage')
