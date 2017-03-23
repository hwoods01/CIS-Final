from django.db import models


# Create your models here.

class SingletracksTrail(models.Model):
    key = models.AutoField(primary_key=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20)
    name = models.TextField()
    longitude = models.DecimalField(max_digits=8, decimal_places=5)
    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    description = models.TextField()
    url = models.TextField()
    difficulty = models.TextField(default = "Unknown")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=2.00)
    length = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)

    def addTrail(self):
        self.save()
