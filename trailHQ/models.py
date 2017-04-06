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



class MtbProjStateId(models.Model):
    state_id = models.IntegerField(primary_key=True)
    state_name = models.CharField(max_length=25)


class MtbProjTrailId(models.Model):
    trailId=models.IntegerField(primary_key=True)
    name = models.TextField()
    stateId=models.ForeignKey('MtbProjStateId')

class TFState(models.Model):
    Sid = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=20)

class TFStateArea(models.Model):
    Aid = models.AutoField(primary_key=True)
    stateId= models.ForeignKey('TFState')
    riding_area = models.TextField()
    area_id = models.IntegerField(default=None,null=True, blank=True )

class TFid(models.Model):
    Tid = models.AutoField(primary_key=True)
    areaId = models.ForeignKey('TFStateArea')
    name = models.TextField()
    trail_id = models.IntegerField(default=None)
    url = models.TextField()