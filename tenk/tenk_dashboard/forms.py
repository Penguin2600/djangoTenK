from django.forms import ModelForm, ModelChoiceField
from django.forms.forms import Form
from tenk_dashboard.models import *

class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        #Render order of fields
        fields = ('bib_number', 'last_name', 'first_name','address_1',
                  'address_2','zipcode','city','state','email','age',
                  'gender', 'shirt_size','event','team_name', 'division',
                  'registration_type')

class QuickParticipantForm(ModelForm):
    class Meta:
        model = Participant
        #Render order of fields
        fields = ('bib_number', 'last_name', 'first_name','age',
                  'gender','state','email','event','team_name','division')

class ImportForm(ModelForm):
    class Meta:
        model = CSVFile
        fields = ('starting_bib_number','csvfile')

class ExportForm(Form):
    export_set = ModelChoiceField(queryset=ExportSet.objects.all())
