from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from collections import defaultdict
from tenk_dashboard.helpers import *
from tenk_dashboard.models import *
from tenk_dashboard.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import csv
import os

from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

class TenkView(TemplateView):

    def get_context_data(self, **kwargs):
        context = {'search_form': SearchParticipantForm()}
        for k,v in kwargs.iteritems():
            if k not in context:
                context[k]=v
        return context

    def get(self, request, *args, **kwargs):
        return redirect('index')

    def post(self, request, *args, **kwargs):
        return redirect('index')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TenkView, self).dispatch(*args, **kwargs)

class CreateView(TenkView):
    template_name = "tenk_dashboard/create.html"

    def get(self, request, *args, **kwargs):
        form = ParticipantForm(
            initial={'registration_type': Registration.objects.get(name='Instant').id,
                     'division': Division.objects.get(name='None').id,
                    })
        context=self.get_context_data(form=form)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        posted_form = ParticipantForm(request.POST)

        if posted_form.is_valid():
            new_participant = posted_form.save(commit=False)
            new_participant.timestamp=timezone.now()
            new_participant.save()

            nextbib=new_participant.bib_number+1
            new_form = ParticipantForm(
                initial={'bib_number': nextbib,
                         'registration_type': new_participant.registration_type.id,
                         'division': new_participant.division.id,
                        })
            context=self.get_context_data(form=new_form)
            return render(request, self.template_name, context)

        context=self.get_context_data(form=posted_form)
        return render(request, self.template_name, context)

class QuickView(TenkView):
    template_name = "tenk_dashboard/quick.html"

    def get(self, request, *args, **kwargs):
        form = QuickParticipantForm(
            initial={'registration_type': Registration.objects.get(name='Instant').id,
                     'division': Division.objects.get(name='None').id,
                    })
        context=self.get_context_data(form=form)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        posted_form = QuickParticipantForm(request.POST)

        if posted_form.is_valid():
            new_participant = posted_form.save(commit=False)
            new_participant.timestamp=timezone.now()
            new_participant.registration_type=Registration.objects.get(name="Instant")
            new_participant.shirt_size=Size.objects.get(name="Unknown")
            new_participant.save()

            nextbib=new_participant.bib_number+1
            new_form = QuickParticipantForm(
                initial={'bib_number': nextbib,
                         'division': new_participant.division.id,
                        })
            context=self.get_context_data(form=new_form)
            return render(request, self.template_name, context)

        context=self.get_context_data(form=posted_form)
        return render(request, self.template_name, context)

class SearchView(TenkView):
    template_name = 'tenk_dashboard/search.html'

    def post(self, request, *args, **kwargs):
        search = request.POST.get('search', None)
        if search:
            results = Participant.objects.all().filter(Q(first_name__contains=search)|
                                                       Q(last_name__contains=search)|
                                                       Q(bib_number__contains=search)|
                                                       Q(zipcode__contains=search))
            if results:
                context=self.get_context_data(results=results)
                return render(request, self.template_name, context)
            return redirect(request.META['HTTP_REFERER'])
        return redirect(request.META['HTTP_REFERER'])

class UpdateView(TenkView):
    template_name = "tenk_dashboard/update.html"

    def get(self, request, participant_id):
        participant = Participant.objects.get(id=participant_id)
        form = ParticipantForm(instance=participant) # A empty, unbound form
        context=self.get_context_data(form=form, participant_id=participant.id)
        return render(request, self.template_name, context)

    def post(self, request):
        participant = Participant.objects.get(id=request.POST['participant_id'])
        posted_form = ParticipantForm(request.POST, instance=participant)

        if posted_form.is_valid():
            posted_form.save()
            context=self.get_context_data(form=posted_form, participant_id=participant.id)
            return render(request, self.template_name, context)

        context=self.get_context_data(form=posted_form, participant_id=participant.id)
        return render(request, self.template_name, context)

class StatsView(TenkView):
    template_name = "tenk_dashboard/stats.html"

    def get(self, request):
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
                    age_count[str(age_ranges[i]+1)+"-"+str(age_ranges[i+1])] += 1

        stats = participant_count.items() + gender_count.items() + event_count.items() + sorted(age_count.items())

        context=self.get_context_data(stats=stats)
        return render(request, self.template_name, context)

class ImportView(TenkView):
    template_name = "tenk_dashboard/import.html"

    def get(self, request, *args, **kwargs):
        form = ImportForm()
        imported_files = CSVFile.objects.all()
        context=self.get_context_data(imported_files= imported_files, form= form)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
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
        return redirect('csv_import')

class ExportView(TenkView):
    template_name = "tenk_dashboard/export.html"

    def get(self, request, *args, **kwargs):
        try:
            ending_bib=Participant.objects.all().aggregate(Max('bib_number'))['bib_number__max']
        except:
            ending_bib=0
        form = ExportForm(
            initial={'starting_bib': 0,
                'ending_bib': ending_bib,
            })

        context=self.get_context_data(form=form)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ExportForm(request.POST)
        if form.is_valid():
            fields=ExportSet.objects.get(id=form.data['export_set']).field_names.split()
            #generate csv headers
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="tenk_export_%s.csv"' % timezone.now()
            writer = csv.writer(response)
            #write header
            writer.writerow(fields)
            #write csv rows
            participants=Participant.objects.filter(bib_number__range=(form.data['starting_bib'], form.data['ending_bib']))
            for participant in participants:
                csvrow=[]
                for field in fields:
                    value=getattr(participant, field)
                    if hasattr(value, 'export_name'):
                        result=getattr(value, 'export_name')
                    else:
                        result=getattr(participant, field)
                    csvrow.append(result)
                writer.writerow(csvrow)
            return response
        return redirect('csv_export')

def checkbib_view(request, bib_number):
    try:
        bib = Participant.objects.get(bib_number=bib_number)
        result="true"
    except:
        result="false"
    return HttpResponse(result)

def logout_view(request):
        logout(request)
        return redirect('login')


def checksearch_view(request, query):
    results = Participant.objects.all().filter(Q(first_name__contains=query)|
                                               Q(last_name__contains=query)|
                                               Q(bib_number__contains=query)|
                                               Q(zipcode__contains=query))
    if results:
        result="true"
    else:
        result="false"
    return HttpResponse(result)