#views.py
#Sion Zhan (sszhan24@bu.edu), 10/27/26
#Defines class based views for the voter_analytics application

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter

# Create your views here.

class VoterListView(ListView):
    """Display a list of voter records, with filtering and pagination"""

    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        """Filter the voter records based on the GET parameters"""

        queryset = super().get_queryset()

        #get the filter values from the URL, if they exist
        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        score = self.request.GET.get('score')

        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        #apply filters if they're provided
        if party:
            queryset = queryset.filter(party_affiliation=party)
        if min_dob:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_dob))
        if max_dob:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_dob))
        if score:
            queryset = queryset.filter(voter_score=int(score))

        if v20state:
            queryset = queryset.filter(v20state=True)
        if v21town:
            queryset = queryset.filter(v21town=True)
        if v21primary:
            queryset = queryset.filter(v21primary=True)
        if v22general:
            queryset = queryset.filter(v22general=True)
        if v23town:
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        """Add the current filter choices to the context to pre-select them"""

        context = super().get_context_data(**kwargs)

        #calculate birth years for the dropdowns
        context['birth_years'] = range(1900, 2026)
        context['scores'] = range(0,6) #0 through 5

        #pass current GET parameters back to the template
        context['current_filters'] = self.request.GET
        return context

class VoterDetailView(DetailView):
    """Display a single voter record"""

    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

