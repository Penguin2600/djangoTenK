from django.shortcuts import render, redirect
from tenk_dashboard.models import *
from tenk_dashboard.models import ParticipantForm
from collections import defaultdict
from django.conf import settings
from django.db.models import Max
from django.utils import timezone

def index(request, context=None):
    template = 'tenk_dashboard/index.html'
    import pdb; pdb.set_trace()
    if context:
        return render(request, template, context)
    else:
        nextbib=get_next_bib()
        form = ParticipantForm(initial={'bib_number': nextbib})
        context = {'form': form}
        return render(request, template, context)

def create(request):
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
            new_form = ParticipantForm(initial={'bib_number': nextbib,
                                                'registration_type': posted_form.cleaned_data['registration_type'].id,
                                                'division': posted_form.cleaned_data['division'].id,
                                                'event': posted_form.cleaned_data['event'].id,
                                                })
            context = {'form': new_form}
            return redirect('tenk_dashboard.views.index', context=context)
        else:
            #There were errors, return the form with them.
            context = {'form': posted_form}
            return redirect('tenk_dashboard.views.index', context=context)

    return redirect('index')

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

    context = {'total_participants ': Participant.objects.count(),
               'gender_count': gender_count,
               'event_count': event_count,
               'age_count': age_count,
               }
    return render(request, template, context)

def get_next_bib():
    try:
        next_bib=Participant.objects.all().aggregate(Max('bib_number'))['bib_number__max']+1
    except:
        next_bib=settings.DEFAULT_BIB
    return next_bib