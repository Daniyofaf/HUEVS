import datetime
# from pyexpat.errors import messages
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from administrator.models import SenateMembers
from administrator.views import senate_members
from e_voting import settings
from voting.forms import CandidateForm, PositionForm
from voting.models import Candidate, Position, Voter, Votes
from .models import ElectionPost, ElectionResult, NominationPost
from datetime import datetime, time
from django.utils import timezone


def dashboard(request):
    positions = Position.objects.all().order_by('priority')
    candidates = Candidate.objects.all()
    voters = Voter.objects.all()
    voted_voters = Voter.objects.filter(voted=1)
    list_of_candidates = []
    votes_count = []
    chart_data = {}

    for position in positions:
        list_of_candidates = []
        votes_count = []
        for candidate in Candidate.objects.filter(position=position):
            list_of_candidates.append(candidate.fullname)
            votes = Votes.objects.filter(candidate=candidate).count()
            votes_count.append(votes)
        chart_data[position] = {
            'candidates': list_of_candidates,
            'votes': votes_count,
            'pos_id': position.id
        }

    context = {
        'position_count': positions.count(),
        'candidate_count': candidates.count(),
        'voters_count': voters.count(),
        'voted_voters_count': voted_voters.count(),
        'positions': positions,
        'chart_data': chart_data,
        'page_title': "Dashboard"
    }
    return render(request, "home.html", context)


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import NominationPost
from .forms import NominationPostForm

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
            messages.success(request, "Success!")
            return redirect("nominationposts")  # Redirect to a success page or any other page
    else:
        form = NominationPostForm()

    context = {
        'nominationposts': nominationposts,
        'form': form
    }
    return render(request, 'NominationPost.html', context)  # Replace 'your_template.html' with the actual template name



from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .forms import NominationPostForm
from .models import NominationPost

def nomination_post_update(request):
    post_id = request.GET.get('post_id')
    post = get_object_or_404(NominationPost, pk=post_id)
    form = NominationPostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        form = NominationPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return render(request, 'NominationPost.html', {'form': form})

def nomination_post_delete(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(NominationPost, pk=post_id)
    if request.method == 'POST':
        post.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})



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
            # try:
            #     approved_nominee = Candidate.objects.create(
            #         fullname=approved_candidate.fullname,
            #         bio=approved_candidate.bio,
            #         position_id = approved_candidate.id
            #     )
            #     # Optionally, you might need to save the image if it's uploaded
            #     # approved_nominee.photo = nominated_candidate.photo
            #     approved_nominee.save()
            #     print("Candidate created successfully:", approved_nominee)
            # except Exception as e:
            #     print("Error creating candidate:", e)
            
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
from voting.models import Nominee, Candidate
import json

@csrf_exempt
def approve_nomination(request, nominated_candidate_id):
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        approved = post_data.get("approved", False)
        
        try:
            nominated_candidate = Nominee.objects.get(id=nominated_candidate_id)
        except Nominee.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Nominee not found"})
        
        nominated_candidate.is_approved = approved
        nominated_candidate.save()
        
        # if approved:
        #     try:
        #         candidate = Candidate.objects.create(
        #             fullname=nominated_candidate.fullname,
        #             bio=nominated_candidate.bio,
        #             position=nominated_candidate.position
        #         )
        #         return JsonResponse({"status": "success"})
        #     except Exception as e:
        #         return JsonResponse({"status": "error", "message": str(e)})
        # else:
        #     return JsonResponse({"status": "success", "message": "Nomination not approved"})
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
# def candidates(request):
#     # Add logic here to retrieve candidates data
#     # Example: candidates = Candidate.objects.all()
#     approved_candidates = Nominee.objects.filter(is_approved=True)
#     # Pass candidates data to template

#     # Render template with candidates data
#     return render(
#         request, "candidatesview.html", {"approved_candidates": approved_candidates}
#     )



def Candidateview(request):
    candidatesview = Candidate.objects.all()
    form = CandidateForm(request.POST or None, request.FILES or None)
    context = {
        'candidatesview': candidatesview,
        'form1': form,
        'page_title': 'Candidates'
    }
    if request.method == 'POST':
        if form.is_valid():
            form = form.save()
            messages.success(request, "New Candidate Created")
        else:
            messages.error(request, "Form errors")
    return render(request, "candidatesview.html", context)

def candidate_view(request):
    candidate_id = request.GET.get('id', None)
    candidate = Candidate.objects.filter(id=candidate_id)
    context = {}
    if not candidate.exists():
        context['code'] = 404
    else:
        candidate = candidate[0]
        context['code'] = 200
        context['fullname'] = candidate.fullname
        previous = CandidateForm(instance=candidate)
        context['form'] = str(previous.as_p())
    return JsonResponse(context)

def Candidatesupdate(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        candidate_id = request.POST.get('id')
        candidate = Candidate.objects.get(id=candidate_id)
        form = CandidateForm(request.POST or None,
                             request.FILES or None, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, "Candidate Data Updated")
        else:
            messages.error(request, "Form has errors")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('Candidateview'))


def Candidatesdelete(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        pos = Candidate.objects.get(id=request.POST.get('id'))
        pos.delete()
        messages.success(request, "Candidate Has Been Deleted")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('Candidateview'))






def viewVote(request):
    votes = Votes.objects.all()
    context = {
        'votes': votes,
        'page_title': 'Votes'
    }
    return render(request, "votesview.html", context)


def ResetVote(request):
    Votes.objects.all().delete()
    Voter.objects.all().update(voted=False, verified=False, otp=None)
    messages.success(request, "All votes has been reset")
    return redirect(reverse('viewVotes'))


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


from administrator.views import find_n_winners


def result(request):
    # Assuming you have candidate data available in your view, replace `candidate_data` with your actual candidate data
    # candidate_data = [
    #     {'name': 'Candidate 1', 'votes': 100},
    #     {'name': 'Candidate 2', 'votes': 90},
    #     {'name': 'Candidate 3', 'votes': 80},
    #     # Add more candidate data as needed
    # ]
    
    # # Define the number of winners you want to find
    # num_winners = 1  # Change this to the desired number of winners
    
    # # Call the find_n_winners function to find the top `num_winners` winners
    # winners = find_n_winners(candidate_data, num_winners)


    # # Pass the winners data to the template
    # context = {
    #     'winners': winners,
    # }
    
    # Render the template with the winners data
    return render(request, "AnnounceResult.html")

from django.http import JsonResponse
from .models import ElectionResult

def announce_election(request):
    if request.method == 'POST':
        try:
            is_announced = request.POST.get('is_announced', None)
            if is_announced is not None:
                # Convert the string value to boolean
                is_announced = is_announced.lower() == 'true'
                
                # Get or create the ElectionResult object
                election_result, created = ElectionResult.objects.get_or_create(pk=1)  # Assuming there's only one instance
                election_result.isposted = is_announced
                election_result.save()
                
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid request. Missing is_announced parameter.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)






def viewpositionbyid(request):
    pos_id = request.GET.get('id', None)
    pos = Position.objects.filter(id=pos_id)
    context = {}
    if not pos.exists():
        context['code'] = 404
    else:
        context['code'] = 200
        pos = pos[0]
        context['name'] = pos.name
        context['id'] = pos.id
    return JsonResponse(context)


def view_Position(request):
    positions = Position.objects.order_by('-priority').all()
    form = PositionForm(request.POST or None)
    context = {
        'positions': positions,
        'form1': form,
        'page_title': "Positions"
    }
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            form.priority = positions.count() + 1  # Just in case it is empty.
            form.save()
            messages.success(request, "New Position Created")
        else:
            messages.error(request, "Form errors")
    return render(request, "positions.html", context)


def update_Position(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        instance = Position.objects.get(id=request.POST.get('id'))
        pos = PositionForm(request.POST or None, instance=instance)
        pos.save()
        messages.success(request, "Position has been updated")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('view_Position'))


def delete_Position(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        pos = Position.objects.get(id=request.POST.get('id'))
        pos.delete()
        messages.success(request, "Position Has Been Deleted")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('view_Position'))
