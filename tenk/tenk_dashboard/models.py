from django.db import models
from django.forms import ModelForm

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class Division(models.Model):
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=16)
    order = models.IntegerField(max_length=16)

    def __unicode__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=16)
    order = models.IntegerField(max_length=16)

    def __unicode__(self):
        return self.name

class Registration(models.Model):
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=16)
    order = models.IntegerField(max_length=16)

    def __unicode__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=16)
    order = models.IntegerField(max_length=16)

    def __unicode__(self):
        return self.name

class Gender(models.Model):
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=16)
    order = models.IntegerField(max_length=16)

    def __unicode__(self):
        return self.name

class Participant(models.Model):
    #ForeignKeys
    event = models.ForeignKey(Event)
    division = models.ForeignKey(Division)
    registration_type = models.ForeignKey(Registration)
    shirt_size = models.ForeignKey(Size)
    gender = models.ForeignKey(Gender)

    #Fields
    activeid = models.IntegerField(max_length=12)
    bibnumber = models.IntegerField(max_length=4)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zipcode = models.IntegerField(max_length=5)
    email = models.EmailField(max_length=255)
    age = IntegerRangeField(max_length=3, min_value=1, max_value=99)
    team_name = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return self.last_name+", "+self.first_name


class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        #Render order of fields
        fields = ('bibnumber', 'last_name', 'first_name','address_1',
                  'address_2','zipcode','city','state','email','age',
                  'gender', 'shirt_size','event','team_name', 'division',
                  'registration_type')