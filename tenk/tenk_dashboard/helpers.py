from tenk_dashboard.models import *
from tenk_dashboard.forms import *
from django.utils import timezone
from django.forms import ValidationError
from django.conf import settings
from django.db.models import Max

def bib_number_exists(bib_number):
    try:
        Participant.objects.get(bib_number=bib_number)
        return True
    except:
        return False

def active_id_exists(active_id):
    try:
        Participant.objects.get(active_id=active_id)
        return True
    except:
        return False

def validate_csv_row(row, bib_number):

    if active_id_exists(row['ACTIVEUSERID']):
        raise ValidationError('Invalid CSV Conent, existing active ids found', code='invalid',)

    if bib_number_exists(bib_number):
        raise ValidationError('Invalid CSV Conent, existing bib numbers found', code='invalid',)

    #Canadians....
    try:
        val = int(row['ZIP'])
    except:
        row['ZIP']="00000"

    #Default Division to "None"
    if not (row['DIVISION']):
        row['DIVISION']="NONE"

    # #If Event is Half Division is Half
    # if row['CATEGORY']=="HALF":
    #     row['DIVISION']="HALF"

    #If Event is HalfC Division is Half, Event is Half
    if row['CATEGORY']=="HALFC":
        row['CATEGORY']="HALF"
        row['DIVISION']="HALF"

    #Default Registration Type to PP
    if not row['REGTYPE']:
        row['REGTYPE']="PP"

    return row

def generate_participant(row, bib_number):
    new_participant=Participant(
        activeid=row['ACTIVEUSERID'],
        bib_number=bib_number,
        first_name=row['FIRSTNAME'],
        last_name=row['LASTNAME'],
        address_1=row['ADDRESS1'],
        city=row['CITY'],
        state=row['STATE'],
        zipcode=row['ZIP'],
        email=row['EMAIL'],
        age=row['AGE'],
        team_name=row['TEAM']+row['5KTEAM'],
        gender=Gender.objects.get(import_name=row['GENDER']),
        shirt_size=Size.objects.get(import_name=row['TSHIRT']),
        event=Event.objects.get(import_name=row['CATEGORY']),
        division=Division.objects.get(import_name=row['DIVISION']),
        registration_type=Registration.objects.get(import_name=row['REGTYPE']),
        timestamp=timezone.now())
    return new_participant