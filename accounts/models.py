from django.db import models

class Account(models.Model):
    name     = models.CharField(max_length=50)
    email    = models.EmailField()
    password = models.CharField(max_length=200)
    address  = models.CharField(max_length=200)

    class Meta:
        db_table = 'accounts'

