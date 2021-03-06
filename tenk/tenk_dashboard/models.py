from django.db import models

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
    import_name = models.CharField(max_length=16)
    export_name = models.CharField(max_length=255)
    order = models.IntegerField(max_length=16)


    def __unicode__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=255)
    import_name = models.CharField(max_length=16)
    export_name = models.CharField(max_length=255)
    order = models.IntegerField(max_length=16)

    class Meta:
        ordering=['order']

    def __unicode__(self):
        return self.name

class Registration(models.Model):
    name = models.CharField(max_length=255)
    import_name = models.CharField(max_length=255)
    export_name = models.CharField(max_length=255)
    order = models.IntegerField(max_length=16)


    def __unicode__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=255)
    import_name = models.CharField(max_length=16)
    export_name = models.CharField(max_length=255)
    order = models.IntegerField(max_length=16)


    def __unicode__(self):
        return self.name

class Gender(models.Model):
    name = models.CharField(max_length=255)
    import_name = models.CharField(max_length=16)
    export_name = models.CharField(max_length=255)
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
    activeid = models.IntegerField(max_length=12, unique=True, blank=True, null=True)
    bib_number = models.IntegerField(max_length=4, unique=True)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255, blank=True, null=True)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zipcode = models.CharField(max_length=7, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    age = IntegerRangeField(max_length=3, min_value=1, max_value=99)
    team_name = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return self.last_name+", "+self.first_name

class CSVFile(models.Model):
    csvfile = models.FileField(upload_to='csvfiles')
    starting_bib_number = models.IntegerField(max_length=10)
    ending_bib_number = models.IntegerField(max_length=10)
    total_imports = models.IntegerField(max_length=10)

# This sucks, build dynamically later.
class ExportSet(models.Model):
    name = models.CharField(max_length=255)
    field_names = models.CharField(max_length=255)
    field_headers = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name
