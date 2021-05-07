from django.db import models

# Create your models here.
class BhavData(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length = 150)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    date = models.DateTimeField(auto_now_add=True) 
    