from django.db import models

# Create your models here.
class Subcriptions(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        permissions = [
            ("advanced", "Advanced Perm"), # subcriptions.advanced
            ("pro", "Pro Perm"), # subcriptions.pro
            ("basic", "Basic Perm"), # subcriptions.basic
            ("basic_ai", "Basic AI Perm")
        ]