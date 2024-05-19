from django.shortcuts import render, redirect, reverse
from account.views import account_login
from board_member.forms import ElectionPost
from board_member.models import ElectionResult
from .models import Nominee, Position, Candidate, Voter, Votes
from django.http import JsonResponse
from django.utils.text import slugify
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
import requests
import json

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return account_login(request)
    context = {}
    return render(request, "voting/login.html", context)


def dashboard(request):
    user = request.user
    if user.voter.voted:  # User has voted
        context = {
            "my_votes": Votes.objects.filter(voter=user.voter),
        }
        return redirect(reverse("vote"))
    else:
        return redirect(reverse("electionpage"))

def vote(request):
    return render(request, "voting/voter/myvote.html")

def electionpage(request):
    # return render(request, "voting/voter/votingandnominatingpage.html")
    return redirect(reverse("show_ballot"))








def view_ballot(request):
    if request.user.is_authenticated:
        voter = request.user.voter
        try:
            vote = Votes.objects.get(voter=voter)
            context = {
                'vote': vote
            }
            return render(request, 'voting/voter/view_ballot.html', context)
        except Votes.DoesNotExist:
            return render(request, 'voting/voter/no_vote.html')
    else:
        return redirect('login')  # Redirect to login page if user is not authenticated 
    
    
def generate_ballot(display_controls=False):
    electionposts = ElectionPost.objects.filter(is_posted=True)
    falseelectionposts = ElectionPost.objects.filter(is_posted=False)
    positions = Position.objects.order_by("priority").all()
    output = ""
    candidates_data = ""
    num = 1
    for position in positions:
        name = position.name
        position_name = slugify(name)
        candidates = Candidate.objects.filter(position=position)
        for candidate in candidates:
            input_box = (
                '<input value="'
                + str(candidate.id)
                + '" type="radio" class="flat-red '
                + position_name
                + '" name="'
                + position_name
                + '">'
            )
            image = "/media/" + str(candidate.photo)
            candidates_data = (
                candidates_data
                + "<li>"
                + input_box
                + '<button type="button" class="btn btn-primary btn-sm btn-flat clist platform" data-fullname="'
                + candidate.fullname
                + '" data-bio="'
                + candidate.bio
                + '"><i class="fa fa-search"></i> Platform</button><img src="'
                + image
                + '" height="100px" width="100px" class="clist"><span class="cname clist">'
                + candidate.fullname
                + "</span></li>"
            )
        up = ""
        if position.priority == 1:
            up = "disabled"
        down = ""
        if position.priority == positions.count():
            down = "disabled"
        output += f"""<div class="row">	<div class="col-xs-12"><div class="box box-solid" id="{position.id}">
             <div class="box-header with-border">
            <h3 class="box-title"><b>{name}</b></h3>"""

        if display_controls:
            output += f""" <div class="pull-right box-tools">
        <button type="button" class="btn btn-default btn-sm moveup" data-id="{position.id}" {up}><i class="fa fa-arrow-up"></i> </button>
        <button type="button" class="btn btn-default btn-sm movedown" data-id="{position.id}" {down}><i class="fa fa-arrow-down"></i></button>
        </div>"""

        output += f"""</div>
        <div class="box-body">
        <p>Select only one candidate
        <span class="pull-right">
        <button type="button" class="btn btn-success btn-sm btn-flat reset" data-desc="{position_name}"><i class="fa fa-refresh"></i> Reset</button>
        </span>
        </p>
        <div id="candidate_list">
        <ul>
        {candidates_data}
        </ul>
        </div>
        </div>
        </div>
        </div>
        </div>
        """
        position.priority = num
        position.save()
        num += 1
        candidates_data = ""
    return output


def fetch_ballot(request):
    output = generate_ballot(display_controls=True)
    return JsonResponse(output, safe=False)




def show_ballot(request):
    electionposts = ElectionPost.objects.filter(is_posted=True)
    falseelectionposts = ElectionPost.objects.filter(is_posted=False)
    candidates = Candidate.objects.all()  # Using a more intuitive variable name
    if request.user.voter.voted:
        messages.error(request, "You have voted already")
        return redirect(reverse("voterDashboard"))
    ballot = generate_ballot(display_controls=False)
    context = {
        "ballot": ballot,
        'electionposts': electionposts,
        'candidates': candidates,  # Updated variable name
    }
    return render(request, "voting/voter/ballot.html", context)


def preview_vote(request):
    electionposts = ElectionPost.objects.filter(is_posted=True)
    falseelectionposts = ElectionPost.objects.filter(is_posted=False)
    if request.method != "POST":
        error = True
        response = "Please browse the system properly"
    else:
        output = ""
        form = dict(request.POST)
        form.pop("csrfmiddlewaretoken", None)
        error = False
        data = []
        positions = Position.objects.all()
        for position in positions:
            pos = slugify(position.name)
            if pos in form:
                form_position = form[pos][0]
                candidate = Candidate.objects.get(position=position, id=form_position)
                output += f"""
                        <div class='row votelist' style='padding-bottom: 2px'>
                          	<span class='col-sm-4'><span class='pull-right'><b>{position.name} :</b></span></span>
                          	<span class='col-sm-8'><i class="fa fa-check-circle-o"></i> {candidate.fullname}</span>
                        </div>
                        <hr/>
                    """
    context = {"error": error, "list": output}
    return JsonResponse(context, safe=False)

from django.shortcuts import render, redirect
from .models import Votes, Nominee  # Import your models here
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Votes, Nominee
from django.contrib import messages

from .models import Voter, Votes, Nominee

from .models import Position, Votes

def submit_ballot(request):
    if request.method == 'POST':
        selected_candidate_id = request.POST.get('selected_candidate')
        if selected_candidate_id:
            try:
                selected_candidate = Nominee.objects.get(pk=selected_candidate_id)
                candidate_name = selected_candidate.fullname
                
                if request.user.is_authenticated:
                    voter = request.user.voter
                    # Check if the voter has already voted
                    if Votes.objects.filter(voter=voter).exists():
                        return redirect('vote')
                    else:
                        # Retrieve the Position instance for 'President'
                        president_position, _ = Position.objects.get_or_create(name='President', defaults={'priority': 1})
                        
                        # Create the Vote instance
                        vote = Votes.objects.create(voter=voter, position=president_position, candidate=candidate_name)
                        vote.save()
                        messages.success(request, f'Vote submitted successfully for {candidate_name}.')
                else:
                    messages.error(request, 'User is not authenticated.')
            except Nominee.DoesNotExist:
                messages.error(request, 'Selected candidate does not exist.')
        else:
            messages.error(request, '') #   No candidate selected.
        return redirect('electionpage')
    else:
        return redirect('electionpage')


from administrator.views import PrintView  # Import the PrintView class

def resultpage(request):
    resultpage = ElectionResult.objects.filter(isposted=True)
    falseresultpage = ElectionResult.objects.filter(isposted=False)
    # Instantiate the PrintView class to generate context data
    print_view = PrintView()
    # context = print_view.get_context_data()
    # context = {'resultpage' : resultpage}
    
    context = {**print_view.get_context_data(), 'resultpage': resultpage}


    # Render the template with the context data
    return render(request, "voting/voter/ResultPage.html", context)


# def candidate_platform(request, candidate_id):
#     try:
#         candidate = Candidate.objects.get(pk=candidate_id)
#         data = {
#             'fullname': candidate.fullname,
#             'bio': candidate.bio,
#         }
#         return JsonResponse(data)
#     except Candidate.DoesNotExist:
#         return JsonResponse({'error': 'Candidate does not exist'}, status=404)




# from .models import CampaignMessage
# from .models import Ballot

# def match_names_and_link():
#     campaign_messages = CampaignMessage.objects.all()
#     ballots = Ballot.objects.all()

#     for message in campaign_messages:
#         for ballot in ballots:
#             if message.candidate_name == ballot.candidate_name:
#                 message.ballot_id = ballot.id
#                 message.save()
#                 break  # Once a match is found, break out of the inner loop






    
# def submit_ballot(request):
#     if request.method != "POST":
#         messages.error(request, "Please, browse the system properly")
#         return redirect(reverse("show_ballot"))

#     voter = request.user.voter
#     if voter.voted:
#         messages.error(request, "You have voted already")
#         return redirect(reverse("voterDashboard"))

#     president_position, created = Position.objects.get_or_create(name='President', defaults={'priority': 1})

#     form = dict(request.POST)
#     form.pop("csrfmiddlewaretoken", None)
#     form.pop("submit_vote", None)

#     if len(form.keys()) < 1:
#         messages.error(request, "Please select at least one candidate")
#         return redirect(reverse("show_ballot"))

#     for pos, form_position in form.items():
#         position = Position.objects.get(name=pos)
#         form_position = form_position[0]
#         candidate = Candidate.objects.get(position=position, id=form_position)
#         vote = Votes.objects.create(candidate=candidate, voter=voter, position=position)

#     inserted_votes = Votes.objects.filter(voter=voter)
#     if inserted_votes.count() != len(form):
#         inserted_votes.delete()
#         messages.error(request, "Please try voting again!")
#         return redirect(reverse("show_ballot"))
#     else:
#         voter.voted = True
#         voter.save()
#         messages.success(request, "Thanks for voting")
#         return redirect(reverse("voterDashboard"))



from django.shortcuts import render, redirect
from .forms import NomineeForm
from board_member.forms import NominationPost


def nominate_candidate(request):
    nominationposts = NominationPost.objects.filter(is_posted=True)
    falsenominationposts = NominationPost.objects.filter(is_posted=False)
    if request.method == "POST":
        form = NomineeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nomination Successful!")
            return redirect("nominate_candidate")
    else:
        form = NomineeForm()
    return render(
        request,
        "voting/voter/nomination_form.html",
        {"form": form, "nominationposts": nominationposts},
    )


# views.py
# from django.shortcuts import get_object_or_404, redirect
# from django.http import JsonResponse
# from .models import Candidate
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def update_candidate_bio(request):
#     if request.method == 'POST':
#         candidate_id = request.POST.get('candidate_id')
#         new_bio = request.POST.get('bio')
#         candidate = get_object_or_404(Candidate, id=candidate_id)
#         candidate.bio = new_bio
#         candidate.save()
#         return JsonResponse({'status': 'success', 'message': 'Bio updated successfully.'})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


