from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.db.models import Q

from collections import defaultdict

from tenk_dashboard.helpers import *
from tenk_dashboard.models import *
from tenk_dashboard.forms import *

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import logout
import csv
import os

@login_required
def create_view(request):
    template = 'tenk_dashboard/create.html'

    if request.method == 'POST':
        posted_form = ParticipantForm(request.POST)

        if posted_form.is_valid():
            #Good data, Save and continue to next entry
            new_participant = posted_form.save(commit=False)
            new_participant.timestamp=timezone.now()
            new_participant.save()

            #Go on to the next entry, prepopulate with last entry's data
            nextbib=get_next_bib(new_participant.bib_number)
            new_form = ParticipantForm(
                initial={'bib_number': nextbib,
                         'registration_type': new_participant.registration_type.id,
                         'division': new_participant.division.id,
                         #'event': new_participant.event.id,
                        })
            context = {'form': new_form, 'search_form': SearchParticipantForm()}
            return render(request, template, context)
        else:
            #There were errors, return the form with them.
            context = {'form': posted_form, 'search_form': SearchParticipantForm()}
            return render(request, template, context)
    else:
        nextbib=get_next_bib()
        form = ParticipantForm(initial={'bib_number': nextbib})
        context = {'form': form, 'search_form': SearchParticipantForm()}
        return render(request, template, context)

@login_required
def quick_create_view(request):
    template = 'tenk_dashboard/quick.html'

    if request.method == 'POST':
        posted_form = QuickParticipantForm(request.POST)

        if posted_form.is_valid():
            #Good data, Save and continue to next entry
            new_participant = posted_form.save(commit=False)
            new_participant.timestamp=timezone.now()
            new_participant.registration_type=Registration.objects.get(shortname="PP")
            new_participant.shirt_size=Size.objects.get(shortname="UK")
            new_participant.save()

            #Go on to the next entry, prepopulate with last entry's data
            nextbib=get_next_bib()
            new_form = QuickParticipantForm(
                initial={'bib_number': nextbib,
                         'division': new_participant.division.id,
                         #'event': new_participant.event.id,
                        })
            context = {'form': new_form}
            return render(request, template, context)
        else:
            #There were errors, return the form with them.
            context = {'form': posted_form}
            return render(request, template, context)
    else:
        nextbib=get_next_bib()
        form = QuickParticipantForm(initial={'bib_number': nextbib})
        context = {'form': form}
        return render(request, template, context)

@login_required
def search_view(request):
    template = 'tenk_dashboard/search.html'
    if request.method == 'POST':
        results = Participant.objects.all()
        search = request.POST.get('search', None)
        if search:
            results = results.filter(Q(first_name__contains=search)|Q(last_name__contains=search)|Q(bib_number__contains=search)|Q(zipcode__contains=search))
        return render(request, template, {'search_form': SearchParticipantForm(request.POST), 'results': results})

@login_required
def update_view(request, participant_id=None):
    template = 'tenk_dashboard/update.html'
    if participant_id==None:
        participant_id=request.POST['participant_id']
    participant = Participant.objects.get(id=participant_id)

    if request.method == 'POST':
        posted_form = ParticipantForm(request.POST, instance=participant)

        if posted_form.is_valid():
            posted_form.save()
            context = {'form': posted_form, 'participant_id': participant.id, 'search_form': SearchParticipantForm()}
            return render(request, template, context)
        else:
            #There were errors, return the form with them.
            context = {'form': posted_form, 'participant_id': participant.id, 'search_form': SearchParticipantForm()}
            return render(request, template, context)
    else:
        form = ParticipantForm(instance=participant) # A empty, unbound form
        context = {'form': form, 'participant_id': participant.id, 'search_form': SearchParticipantForm()}

    return render(request, template, context)

@login_required
def stats_view(request):
    template = 'tenk_dashboard/stats.html'
    allparticipants = Participant.objects.all()

    #count participants
    participant_count={'Total participants ': Participant.objects.count()}

    #count genders
    gender_count=defaultdict(int)
    for participant in allparticipants:
        gender_count[participant.gender.name]+=1

    #count events
    event_count=defaultdict(int)
    for participant in allparticipants:
        event_count[participant.event.name]+=1

    #count ages
    age_count = defaultdict(int)
    age_ranges = settings.AGE_RANGES
    for i in range(0,len(age_ranges)-1):
        for participant in allparticipants:
            if participant.age > age_ranges[i] and participant.age <= age_ranges[i+1]:
                age_count[str(age_ranges[i])+"-"+str(age_ranges[i+1])] += 1

    stats = participant_count.items() + gender_count.items() + event_count.items() + age_count.items()

    context = {'stats': stats}
    return render(request, template, context)

def checkbib_view(request, bib_number):
    try:
        bib=Participant.objects.get(bib_number=bib_number)
        result="true"
    except:
        result="false"
    return HttpResponse(result)

def logout_view(request):
        #log user out and redirect to login page.
        template = 'tenk_dashboard/auth.html'
        logout(request)
        return redirect('login')

@login_required
def csv_import_view(request):
    template = 'tenk_dashboard/import.html'
    # Handle file upload
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = CSVFile(
                csvfile = request.FILES['csvfile'],
                starting_bib_number=request.POST['starting_bib_number'],
                ending_bib_number=0,
                total_imports=0,)
            csv_file.save()

            #Get data we need to start parsing the CSV
            csv_path   = os.path.join(settings.MEDIA_ROOT , str(csv_file.csvfile))
            csv_reader = csv.DictReader(open(csv_path))
            bib_number = int(csv_file.starting_bib_number)
            new_participant_list = []

            #generate a list of new participants to be added,
            #only complete the add if everything is valid

            for row in csv_reader:
                valid_row=validate_csv_row(row,bib_number)
                new_participant_list.append(generate_participant(valid_row, bib_number))
                bib_number+=1

            #All validations passed, save all new participants
            for participant in new_participant_list:
                participant.save()

            #Update csv object and save.
            ending_bib_number = bib_number-1
            total_imports = bib_number - int(csv_file.starting_bib_number)
            csv_file.ending_bib_number = ending_bib_number
            csv_file.total_imports = total_imports
            csv_file.save()

            return redirect('csv_import')
    else:
        form = ImportForm() # A empty, unbound form

    imported_files = CSVFile.objects.all()
    return render(request, template,{'imported_files': imported_files, 'form': form},
    )


@login_required
def csv_export_view(request):
    template = 'tenk_dashboard/export.html'
    if request.method == 'POST':
        form = ExportForm(request.POST)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
        writer = csv.writer(response)
        writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
        writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
        return response
    else:
        form = ExportForm()
        return render(request, template, {'form': form})