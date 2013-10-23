from django.forms import ModelForm, ModelChoiceField, CharField, TextInput, IntegerField
from django.forms.forms import Form
from tenk_dashboard.models import *

class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        #Render order of fields
        fields = ('bib_number', 'first_name', 'last_name','address_1',
                  'address_2','zipcode','city','state','email','age',
                  'gender', 'shirt_size','event','team_name', 'division',
                  'registration_type')

class QuickParticipantForm(ModelForm):
    class Meta:
        model = Participant
        #Render order of fields
        fields = ('bib_number', 'first_name', 'last_name', 'age',
                  'gender','state','email','event','team_name','division')

class SearchParticipantForm(Form):
    search = CharField(max_length=100, widget=TextInput(attrs={'class':'searchform', 'onkeydown':"if (event.keyCode == 13) { this.form.submit(); return false; }"}))

class ImportForm(ModelForm):
    class Meta:
        model = CSVFile
        fields = ('starting_bib_number','csvfile')

class ExportForm(Form):
    starting_bib = IntegerField()
    ending_bib = IntegerField()
    export_set = ModelChoiceField(queryset=ExportSet.objects.all())
