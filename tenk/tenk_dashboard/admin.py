from django.contrib import admin
from tenk_dashboard.models import *
from django.http import HttpResponse
import csv

admin.site.register(Division)
admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(Size)
admin.site.register(Participant)
admin.site.register(Gender)
admin.site.register(CSVFile)