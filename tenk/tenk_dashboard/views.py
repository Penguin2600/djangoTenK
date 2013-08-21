from django.shortcuts import render, redirect
from tenk_dashboard.models import *
from tenk_dashboard.models import ParticipantForm
from collections import defaultdict
from django.conf import settings
from django.db.models import Max
from django.utils import timezone

def index(request):
    template = 'tenk_dashboard/index.html'

    if request.method == 'POST':
        posted_form = ParticipantForm(request.POST)

        if posted_form.is_valid():
            #Good data, Save and continue to next entry
            new_participant = posted_form.save(commit=False)
            new_participant.timestamp=timezone.now()
            new_participant.save()
            #Go on to the next entry, prepopulate with last entry's data

            nextbib=get_next_bib()
            new_form = ParticipantForm(
                initial={'bib_number': nextbib,
                         'registration_type': new_participant.registration_type.id,
                         'division': new_participant.division.id,
                         'event': new_participant.event.id,
                         'age': 25,
                        })
            context = {'form': new_form}
            return render(request, template, context)
        else:
            #There were errors, return the form with them.
            context = {'form': posted_form}
            return render(request, template, context)
    else:
        nextbib=get_next_bib()
        form = ParticipantForm(initial={'bib_number': nextbib})
        context = {'form': form}
        return render(request, template, context)

def update(request, participanlt_id):
    template = 'tenk_dashboard/index.html'

    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            return render(request, template, context)
        else:
            return render(request, template, context)
    else:
        participant = Participant.objects.get(pk=participant_id)
        form = ParticipantForm(instance=participant) # A empty, unbound form
    context = {'form': form}

    return render(request, template, context)


def stats(request):
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

def get_next_bib():
    try:
        next_bib=Participant.objects.all().aggregate(Max('bib_number'))['bib_number__max']+1
    except:
        next_bib=settings.DEFAULT_BIB
    return next_bib