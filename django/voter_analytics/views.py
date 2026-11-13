#views.py
#Sion Zhan (sszhan24@bu.edu), 10/27/26
#Defines class based views for the voter_analytics application

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
import plotly.graph_objects as go
from collections import Counter

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

class VoterGraphView(ListView):
    """Display aggregate graphs of voter data, with filtering"""

    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        """Re use the same filter logic from VoterListView"""

        queryset = super().get_queryset()

        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        score = self.request.GET.get('score')

        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

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
        """Generate plotly graphs and pass them to the template"""

        context = super().get_context_data(**kwargs)

        #get the filtered queryset
        voters = self.get_queryset()
        n = voters.count()

        #pass form data back to template so filters stay selected
        context['birth_years'] = range(1900, 2026)
        context['scores'] = range(0, 6)
        context['current_filters'] = self.request.GET
        context['n'] = n

        if n == 0:
            #if no voters match the filters, don't try to build empty charts
            return context

        #graph 1: voter distribution by year of birth
        #get a list of birth years from the queryset
        years = [v.date_of_birth.year for v in voters]
        year_counts = Counter(years)
        sorted_years = sorted(year_counts.keys())
        fig1 = go.Figure(data=[go.Bar(x=sorted_years, y=[year_counts[y] for y in sorted_years])])
        fig1.update_layout(title=f"Voter distribution by Year of Birth (n={n})", xaxis_title="Year of Birth", yaxis_title="Count", bargap=0.1,)
        context['graph1'] = fig1.to_html(full_html=False, include_plotlyjs='cdn', default_width='100%')

        #graph 2: voter distribution by party affiliation
        #count occurrences of each party
        parties = [p.strip() for p in voters.values_list('party_affiliation', flat=True)]
        party_counts = Counter(parties)
        party_labels = [p.strip() for p in party_counts.keys()]
        fig2 = go.Figure(data=[go.Pie(labels=party_labels, values=list(party_counts.values()))])
        fig2.update_layout(title=f"Voter distribution by Party Affiliation (n={n})")
        context['graph2'] = fig2.to_html(full_html=False, include_plotlyjs=False, default_width='100%')

        #graph 3: vote count by election
        #count True values for each election field
        election_labels = ['v20state','v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = [voters.filter(**{label: True}).count() for label in election_labels]
        fig3 = go.Figure(data=[go.Bar(x=election_labels, y=election_counts)])
        fig3.update_layout(title=f"Vote Count by Election (n={n})", xaxis_title="Election", yaxis_title="Number of Voters",)
        context['graph3'] = fig3.to_html(full_html=False, include_plotlyjs=False, default_width='100%')

        return context
    