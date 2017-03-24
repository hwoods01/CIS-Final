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

    def addTrail(self):
        self.save()



class MtbProjStateId(models.Model):
    state_id = models.IntegerField(primary_key=True)
    state_name = models.CharField(max_length=25)


class MtbProjTrailId(models.Model):
    trailId=models.IntegerField(primary_key=True)
    name = models.TextField()
    stateId=models.ForeignKey('MtbProjStateId')

class TFState(models.Model):
    _id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=20)

class TFStateArea(models.Model):
    stateId= models.ForeignKey('TFState')
    riding_area = models.TextField()
    area_id = models.IntegerField(default=None)

class TFid(models.Model):
    area_id = models.ForeignKey('TFStateArea')
    name = models.TextField()
    trail_id = models.IntegerField(default=None)
    url = models.TextField()

