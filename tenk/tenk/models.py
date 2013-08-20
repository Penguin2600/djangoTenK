from django.db import models

class Division(models.Model):
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name

class Registration(models.Model):
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name

class Participant(models.Model):
    #ForeignKeys
    event = models.ForeignKey(Event)
    division = models.ForeignKey(Division)
    registration_type = models.ForeignKey(Registration)
    shirt_size = models.ForeignKey(Size)

    #Fields
    activeid = models.IntegerField(max_length=12)
    bibnumber = models.IntegerField(max_length=4)
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zipcode = models.IntegerField(max_length=5)
    email = models.EmailField(max_length=255)
    age = models.IntegerField(max_length=3)
    gender = models.CharField(max_length=1)

    team = models.CharField(max_length=255)
    registration = models.IntegerField(max_length=3)
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return self.name