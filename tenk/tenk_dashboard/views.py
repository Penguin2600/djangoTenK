from django.shortcuts import render
from tenk_dashboard.models import *
from tenk_dashboard.models import ParticipantForm
from collections import defaultdict
from django.config import settings

def index(request):
    template = 'tenk_dashboard/index.html'

    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
                return render(request, template, context)
    else:
        form = ParticipantForm() # A empty, unbound form
    context = {'form': form}
    # Render list page with the documents and the form
    return render(request, template, context)

def update(request, participant_id):
    template = 'tenk_dashboard/index.html'

    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
                return render(request, template, context)
    else:
        participant = Participant.objects.get(pk=participant_id)
        form = ParticipantForm(instance=participant) # A empty, unbound form
    context = {'form': form}
    # Render list page with the documents and the form
    return render(request, template, context)


def stats(request):
    template = 'tenk_dashboard/stats.html'
    allparticipants = Participant.objects.getall()

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
    for i in range(0,len(age_ranges)-2):
        for participant in allparticipants:
            if participant.age > age_ranges[i] and participant.age <= age_ranges[i+1]:
                age_count[str(age_ranges[i]+"-"+age_ranges[i+1])] += 1

    context = {'total_participants ': Participant.objects.count(),
               'gender_count': gender_count,
               'event_count': event_count,
               'age_count': age_count,
               }
    return render(request, template, context)