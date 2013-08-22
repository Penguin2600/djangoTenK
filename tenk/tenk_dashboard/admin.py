from django.contrib import admin
from tenk_dashboard.models import *
from django.http import HttpResponse
import csv

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('bib_number', 'activeid', 'last_name', 'first_name', 'city', 'state', 'zipcode', 'age', 'event', 'registration_type')

class GenericAdmin(admin.ModelAdmin):
    list_display = ('name', 'shortname', 'order')

class CSVAdmin(admin.ModelAdmin):
    list_display = ('csvfile', 'starting_bib_number', 'ending_bib_number', 'total_imports')

class ExportAdmin(admin.ModelAdmin):
    list_display = ('name', 'field_names')

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Event, GenericAdmin)
admin.site.register(Division, GenericAdmin)
admin.site.register(Registration, GenericAdmin)
admin.site.register(Size, GenericAdmin)
admin.site.register(Gender, GenericAdmin)
admin.site.register(CSVFile, CSVAdmin)
admin.site.register(ExportSet, ExportAdmin)
