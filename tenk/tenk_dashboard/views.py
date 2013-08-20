from django.shortcuts import render
from tenk_dashboard.models import Participant
from tenk_dashboard.models import ParticipantForm

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