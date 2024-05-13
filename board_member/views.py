import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from administrator.models import SenateMembers
from administrator.views import senate_members
from e_voting import settings
from voting.models import Candidate, Position, Voter, Votes
from .models import ElectionPost, NominationPost
from datetime import datetime, time
from django.utils import timezone


# Dashboard view
def dashboard(request):
    return render(request, "dashboard.html")


def nominationposts(request):
    nominationposts = NominationPost.objects.all()

    if request.method == "POST":
        form = NominationPostForm(request.POST)
        posted = request.POST.get("post")
        unpost = request.POST.get("unpost")
        if posted:
            posted_nomination = NominationPost.objects.get(pk=posted)
            posted_nomination.is_posted = True
            posted_nomination.save()
        elif unpost:
            unposted_nomination = NominationPost.objects.get(pk=unpost)
            unposted_nomination.is_posted = False
            unposted_nomination.save()
        if form.is_valid():
            form.save()  # This will save the form data to the database
            # messages.success(request,"success!")
            # print("added")
            return redirect(
                "nominationposts"
            )  # Redirect to a success page or any other page
    else:
        form = NominationPostForm()
        

# Calculate remaining time for each nomination post
    # now = timezone.localtime(timezone.now())  # Make now timezone-aware
    # for nomination_post in nominationposts:
    #     # If the nomination post is not posted yet, calculate the remaining time
    #     if not nomination_post.is_posted:
    #         end_time = nomination_post.end_time
    #         # Create a datetime object combining the date portion of now with the time portion of end_time
    #         end_datetime = timezone.make_aware(datetime.combine(now.date(), end_time))
    #         remaining_time = end_datetime - now
    #         nomination_post.remaining_time = remaining_time

    context = {
        "form": form,
        "nominationposts": nominationposts,
    }

    return render(request, "NominationPost.html", context)


from django.shortcuts import render
from voting.models import Nominee


def viewnominatedcandidate(request):
    nominatedcandidates = Nominee.objects.all()

    if request.method == "POST":
        candidate_approved = request.POST.get("approve_candidate")
        candidate_dispproved = request.POST.get("candidate_dispproved")
        if candidate_approved:
            approved_candidate = Nominee.objects.get(pk=candidate_approved)
            approved_candidate.is_approved = True
            try:
                approved_nominee = Candidate.objects.create(
                    fullname=approved_candidate.fullname,
                    bio=approved_candidate.bio,
                    position_id = approved_candidate.id
                )
                # Optionally, you might need to save the image if it's uploaded
                # approved_nominee.photo = nominated_candidate.photo
                approved_nominee.save()
                print("Candidate created successfully:", approved_nominee)
            except Exception as e:
                print("Error creating candidate:", e)
            
            approved_candidate.save()
        elif candidate_dispproved:
            approved_candidate = Nominee.objects.get(pk=candidate_dispproved)
            approved_candidate.is_approved = False
            approved_candidate.save()

    return render(
        request,
        "nominatedcandidates.html",
        {"nominated_candidates": nominatedcandidates},
    )


from django.shortcuts import render, redirect
from .forms import ElectionPostForm, NominationPostForm

# def add_nomination_post(request):
#     if request.method == 'POST':
#         form = NominationPostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('nomination_post_list') # Redirect to a page listing all nomination posts
#     else:
#         form = NominationPostForm()
#     return render(request, 'NominationPost.html', {'form': form})


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ElectionPostForm
from .models import ElectionPost
import datetime
from django.utils import timezone

def electionposts(request):
    # Fetch all election posts
    electionposts = ElectionPost.objects.all()

    if request.method == "POST":
        form = ElectionPostForm(request.POST)
        if form.is_valid():
            form.save()  # This will save the form data to the database
            return redirect("electionposts")

        # Check if a post or unpost action was submitted
        posted = request.POST.get("post")
        unpost = request.POST.get("unpost")
        if posted:
            posted_election = ElectionPost.objects.get(pk=posted)
            posted_election.is_posted = True
            posted_election.save()
        elif unpost:
            unposted_election = ElectionPost.objects.get(pk=unpost)
            unposted_election.is_posted = False
            unposted_election.save()
    else:
        form = ElectionPostForm()
    
    # Calculate the remaining time for each election post
    now = timezone.now()
    for post in electionposts:
        end_datetime = timezone.make_aware(datetime.datetime.combine(post.end_date, post.end_time))
        if now < end_datetime:
            time_diff = end_datetime - now
            post.remaining_time = time_diff
        else:
            post.remaining_time = datetime.timedelta(seconds=0)

    return render(request, 'ElectionPost.html', {'form': form, 'electionposts': electionposts})

    # else:
        # Handle GET requests or other cases
        # You may want to render a template or return a different response
        # return HttpResponse("Method not allowed or invalid request.")



# View for displaying list of voters
def view_voters_list(request):
    # Retrieve all registered voters
    voters = Voter.objects.all()

    # Pass voter data to template
    context = {"voters": voters}

    # Render template with voter data
    return render(request, "voters_list.html", context)


# View for displaying nominated candidates
def nominated_candidates(request):
    # Add logic here to retrieve nominated candidates data
    # Example: nominated_candidates = NominatedCandidate.objects.all()

    # Pass nominated candidates data to template
    context = {}  # Add your data to pass to the template

    # Render template with nominated candidates data
    return render(request, "nominatedcandidates.html", context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from voting.models import Nominee, Candidate  # Import Candidate model
import json

@csrf_exempt
def approve_nomination(request, nominated_candidate_id):
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        approved = post_data.get("approved", False)
        nominated_candidate = Nominee.objects.get(id=nominated_candidate_id)
        nominated_candidate.is_approved = approved
        nominated_candidate.save()
        
        if approved:  # Only create a Candidate if the nomination is approved
            candidate = Candidate.objects.create(
                fullname=nominated_candidate.fullname,
                bio=nominated_candidate.bio,
                position=nominated_candidate.position
            )
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "message": "Nomination not approved"})
    return JsonResponse({"status": "error", "message": "Invalid request method"})


# views.py

# from django.shortcuts import get_object_or_404, HttpResponse
# from voting.models import Nominee, Candidate

# def submit_nomination(request, nominated_candidate_id):
#     nominated_candidate = get_object_or_404(Nominee, id=nominated_candidate_id)

#     # Create a new candidate with the data from the nominated candidate
#     Candidate = Candidate.objects.create(
#         fullname=nominated_candidate.fullname,
#         position=nominated_candidate.position,
#         # bio=nominated_candidate.bio,
#         # photo=nominated_candidate.photo
#     )

#     # Optionally, you can delete the nominated candidate after transferring the data
#     # nominated_candidate.delete()

#     return HttpResponse("Candidate submitted successfully")


# View for displaying list of candidates
def candidates(request):
    # Add logic here to retrieve candidates data
    # Example: candidates = Candidate.objects.all()
    approved_candidates = Nominee.objects.filter(is_approved=True)
    # Pass candidates data to template

    # Render template with candidates data
    return render(
        request, "candidatesview.html", {"approved_candidates": approved_candidates}
    )


# View for displaying votes
def votes(request):
    # Add logic here to retrieve votes data
    # Example: votes = Vote.objects.all()

    # Pass votes data to template
    context = {}  # Add your data to pass to the template

    # Render template with votes data
    return render(request, "votesview.html", context)


from django.shortcuts import render
from voting.models import Nominee


# def viewnominatedcandidate(request):
#     nominatedcandidates = Nominee.objects.all()

#     if request.method == "POST":
#         candidate_approved = request.POST.get("approve_candidate")
#         candidate_dispproved = request.POST.get("candidate_dispproved")
#         if candidate_approved:
#             approved_candidate = Nominee.objects.get(pk=candidate_approved)
#             approved_candidate.is_approved = True
#             approved_candidate.save()
#         elif candidate_dispproved:
#             approved_candidate = Nominee.objects.get(pk=candidate_dispproved)
#             approved_candidate.is_approved = False
#             approved_candidate.save()

#     return render(
#         request,
#         "nominatedcandidates.html",
#         {"nominated_candidates": nominatedcandidates},
#     )


from django_renderpdf.views import PDFView


class PrintView(PDFView):
    template_name = "admin/print.html"
    prompt_download = True

    @property
    def download_name(self):
        return "Election Result.pdf"

    def get_context_data(self, *args, **kwargs):
        title = "Hu E-voting"
        try:
            file = open(settings.ELECTION_TITLE_PATH, "r")
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
                this_candidate_data["name"] = candidate.fullname
                this_candidate_data["votes"] = votes
                candidate_data.append(this_candidate_data)
            print(
                "Candidate Data For  ", str(position.name), " = ", str(candidate_data)
            )
            # ! Check Winner
            if len(candidate_data) < 1:
                winner = "Position does not have candidates"
            else:
                # Check if max_vote is more than 1
                winner = max(candidate_data, key=lambda x: x["votes"])
                if winner["votes"] == 0:
                    winner = "No one voted for this position yet."
                else:
                    winner = "Winner : " + winner["name"]
            print(
                "Candidate Data For  ", str(position.name), " = ", str(candidate_data)
            )
            position_data[position.name] = {
                "candidate_data": candidate_data,
                "winner": winner,
            }
        context["positions"] = position_data
        print(context)
        return context


def view_senate_member_by_id(request):
    # Retrieve all registered voters
    senate_members = SenateMembers.objects.all()  # Fetch all Senate members

    # Pass voter data to template

    # Render template with voter data
    return render(request, "senatemembers.html", {'senate_members': senate_members})


def result(request):
    return render(request, "AnnounceResult.html")