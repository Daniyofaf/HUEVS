from django.http import JsonResponse
from django.shortcuts import render
from administrator.models import SenateMembers
from administrator.views import senate_members
from e_voting import settings
from voting.models import Candidate, Position, Voter, Votes

# Dashboard view
def dashboard(request):
    return render(request, 'dashboard.html')

# View for displaying list of voters
def view_voters_list(request):
    # Retrieve all registered voters
    voters = Voter.objects.all()
    
    # Pass voter data to template
    context = {'voters': voters}
    
    # Render template with voter data
    return render(request, 'voters_list.html', context)

# View for displaying nominated candidates
def nominated_candidates(request):
    # Add logic here to retrieve nominated candidates data
    # Example: nominated_candidates = NominatedCandidate.objects.all()
    
    # Pass nominated candidates data to template
    context = {}  # Add your data to pass to the template
    
    # Render template with nominated candidates data
    return render(request, 'nominatedcandidates.html', context)


# views.py

from django.shortcuts import get_object_or_404, HttpResponse
from voting.models import Nominee, Candidate

def submit_nomination(request, nominated_candidate_id):
    nominated_candidate = get_object_or_404(Nominee, id=nominated_candidate_id)

    # Create a new candidate with the data from the nominated candidate
    new_candidate = Candidate.objects.create(
        fullname=nominated_candidate.fullname,
        position=nominated_candidate.position,
        # bio=nominated_candidate.bio,
        # photo=nominated_candidate.photo
    )

    # Optionally, you can delete the nominated candidate after transferring the data
    # nominated_candidate.delete()

    return HttpResponse("Candidate submitted successfully")



# View for displaying list of candidates
def candidates(request):
    # Add logic here to retrieve candidates data
    # Example: candidates = Candidate.objects.all()
    
    # Pass candidates data to template
    context = {}  # Add your data to pass to the template
    
    # Render template with candidates data
    return render(request, 'candidatesview.html', context)

# View for displaying votes
def votes(request):
    # Add logic here to retrieve votes data
    # Example: votes = Vote.objects.all()
    
    # Pass votes data to template
    context = {}  # Add your data to pass to the template
    
    # Render template with votes data
    return render(request, 'votesview.html', context)

from django.shortcuts import render
from voting.models import Nominee

def viewnominatedcandidate(request):
    nominatedcandidates = Nominee.objects.all()
    return render(request, 'nominatedcandidates.html', {'nominated_candidates': nominatedcandidates})


from django_renderpdf.views import PDFView

class PrintView(PDFView):
    template_name = 'admin/print.html'
    prompt_download = True

    @property
    def download_name(self):
        return "Election Result.pdf"

    def get_context_data(self, *args, **kwargs):
        title = "Hu E-voting"
        try:
            file = open(settings.ELECTION_TITLE_PATH, 'r')
            title = file.read()
        except:
            pass
        context = super().get_context_data(*args, **kwargs)
        position_data = {}
        for position in Position.objects.all():
            candidate_data = []
            winner = ""
            for candidate in Candidate.objects.filter(position=position):
                this_candidate_data = {}
                votes = Votes.objects.filter(candidate=candidate).count()
                this_candidate_data['name'] = candidate.fullname
                this_candidate_data['votes'] = votes
                candidate_data.append(this_candidate_data)
            print("Candidate Data For  ", str(
                position.name), " = ", str(candidate_data))
            # ! Check Winner
            if len(candidate_data) < 1:
                winner = "Position does not have candidates"
            else:
                # Check if max_vote is more than 1
                winner = max(candidate_data, key=lambda x: x['votes'])
                if winner['votes'] == 0:
                    winner = "No one voted for this position yet."
                else:
                    winner = "Winner : " + winner['name']
            print("Candidate Data For  ", str(
                position.name), " = ", str(candidate_data))
            position_data[position.name] = {
                'candidate_data': candidate_data, 'winner': winner}
        context['positions'] = position_data
        print(context)
        return context


def view_senate_member_by_id(request):
     # Retrieve all registered voters
    senate_members = SenateMembers.objects.all()
    
    # Pass voter data to template
    context = {'senate_membera': senate_members}
    
    # Render template with voter data
    return render(request, 'senatemembers.html', context)