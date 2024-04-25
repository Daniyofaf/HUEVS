from django.shortcuts import render, redirect, reverse
from account.views import account_login
from .models import Position, Candidate, Voter, Votes
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
        return render(request, "voting/voter/result.html", context)
    else:
        return redirect(reverse("nominate_candidate"))
    
def vote(request):
    user = request.user
    if user.voter.voted:  # User has voted
        context = {
            "my_votes": Votes.objects.filter(voter=user.voter),
        }
        return render(request, "voting/voter/result.html", context)
    else:
        return redirect(reverse("show_ballot"))


def generate_ballot(display_controls=False):
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
    if request.user.voter.voted:
        messages.error(request, "You have voted already")
        return redirect(reverse("voterDashboard"))
    ballot = generate_ballot(display_controls=False)
    context = {"ballot": ballot}
    return render(request, "voting/voter/ballot.html", context)


def preview_vote(request):
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


def submit_ballot(request):
    if request.method != "POST":
        messages.error(request, "Please, browse the system properly")
        return redirect(reverse("show_ballot"))

    voter = request.user.voter
    if voter.voted:
        messages.error(request, "You have voted already")
        return redirect(reverse("voterDashboard"))

    form = dict(request.POST)
    form.pop("csrfmiddlewaretoken", None)
    form.pop("submit_vote", None)

    if len(form.keys()) < 1:
        messages.error(request, "Please select at least one candidate")
        return redirect(reverse("show_ballot"))

    for pos, form_position in form.items():
        position = Position.objects.get(name=pos)
        form_position = form_position[0]
        candidate = Candidate.objects.get(position=position, id=form_position)
        vote = Votes()
        vote.candidate = candidate
        vote.voter = voter
        vote.position = position
        vote.save()

    inserted_votes = Votes.objects.filter(voter=voter)
    if inserted_votes.count() != len(form):
        inserted_votes.delete()
        messages.error(request, "Please try voting again!")
        return redirect(reverse("show_ballot"))
    else:
        voter.voted = True
        voter.save()
        messages.success(request, "Thanks for voting")
        return redirect(reverse("voterDashboard"))


from django.shortcuts import render, redirect
from .forms import NomineeForm


def nominate_candidate(request):
    if request.method == "POST":
        form = NomineeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("confirmation")
    else:
        form = NomineeForm()
    return render(request, "voting/voter/nomination_form.html", {"form": form})


def confirmation(request):
    return render(request, "voting/voter/confirmation.html")


