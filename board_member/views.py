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
from django.http import JsonResponse
from django.contrib import messages
from .models import NominationPost
from .forms import NominationPostForm

def nominationposts(request):
    nominationposts = NominationPost.objects.all()
    form = NominationPostForm(request.POST or None)
    if request.method == 'POST':
        if 'post' in request.POST:
            id = request.POST.get('post')
            nomination_post = NominationPost.objects.get(id=id)
            nomination_post.is_posted = True
            nomination_post.save()
        elif 'unpost' in request.POST:
            id = request.POST.get('unpost')
            nomination_post = NominationPost.objects.get(id=id)
            nomination_post.is_posted = False
            nomination_post.save()
        elif form.is_valid():
            form.save()
            messages.success(request, "New Nomination Post Created")
        else:
            messages.error(request, "Form errors")

    context = {
        'nominationposts': nominationposts,
        'form': form,
        'page_title': "Nomination Posts"
    }
    return render(request, "NominationPost.html", context)

def nomination_post_by_id(request):
    post_id = request.GET.get('id', None)
    nomination_post = NominationPost.objects.filter(id=post_id).first()
    context = {}
    if not nomination_post:
        context['code'] = 404
    else:
        context['code'] = 200
        context['id'] = nomination_post.id
        context['start_time'] = nomination_post.start_time
        context['start_date'] = nomination_post.start_date
        context['end_time'] = nomination_post.end_time
        context['end_date'] = nomination_post.end_date
    return JsonResponse(context)

def update_nomination_post(request):
    if request.method == 'POST':
        try:
            instance = NominationPost.objects.get(id=request.POST.get('id'))
            form = NominationPostForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, "Nomination Post has been updated")
            else:
                messages.error(request, "Form errors")
        except NominationPost.DoesNotExist:
            messages.error(request, "Nomination Post not found")
    else:
        messages.error(request, "Invalid request method")
    return redirect('nominationposts')

def delete_nomination_post(request):
    if request.method == 'POST':
        try:
            nomination_post = NominationPost.objects.get(id=request.POST.get('id'))
            nomination_post.delete()
            messages.success(request, "Nomination Post has been deleted")
        except NominationPost.DoesNotExist:
            messages.error(request, "Nomination Post not found")
    else:
        messages.error(request, "Invalid request method")
    return redirect('nominationposts')




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
from django.http import JsonResponse
from django.contrib import messages
from .models import ElectionPost
from .forms import ElectionPostForm

def electionposts(request):
    electionposts = ElectionPost.objects.all()
    form = ElectionPostForm(request.POST or None)
    if request.method == 'POST':
        if 'post' in request.POST:
            id = request.POST.get('post')
            election_post = ElectionPost.objects.get(id=id)
            election_post.is_posted = True
            election_post.save()
        elif 'unpost' in request.POST:
            id = request.POST.get('unpost')
            election_post = ElectionPost.objects.get(id=id)
            election_post.is_posted = False
            election_post.save()
        elif form.is_valid():
            form.save()
            messages.success(request, "New Election Post Created")
        else:
            messages.error(request, "Form errors")

    context = {
        'electionposts': electionposts,
        'form': form,
        'page_title': "Election Posts"
    }
    return render(request, "ElectionPost.html", context)

def election_post_by_id(request):
    post_id = request.GET.get('id', None)
    election_post = ElectionPost.objects.filter(id=post_id).first()
    context = {}
    if not election_post:
        context['code'] = 404
    else:
        context['code'] = 200
        context['id'] = election_post.id
        context['start_time'] = election_post.start_time
        context['start_date'] = election_post.start_date
        context['end_time'] = election_post.end_time
        context['end_date'] = election_post.end_date
    return JsonResponse(context)

def update_election_post(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if id:
            try:
                instance = ElectionPost.objects.get(id=id)
                form = ElectionPostForm(request.POST, instance=instance)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Election Post has been updated")
                    return redirect('electionposts')
                else:
                    messages.error(request, "Form errors")
            except ElectionPost.DoesNotExist:
                messages.error(request, "Election Post not found")
        else:
            messages.error(request, "ID field is required")
    else:
        messages.error(request, "Invalid request method")
    return redirect('electionposts')



def delete_election_post(request):
    if request.method == 'POST':
        try:
            election_post = ElectionPost.objects.get(id=request.POST.get('id'))
            election_post.delete()
            messages.success(request, "Election Post has been deleted")
        except ElectionPost.DoesNotExist:
            messages.error(request, "Election Post not found")
    else:
        messages.error(request, "Invalid request method")
    return redirect('electionposts')




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


from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib import messages
from voting.models import Candidate
from voting.forms import CandidateForm

def Candidateview(request):
    candidatesview = Candidate.objects.all()
    form = CandidateForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "New Candidate Created")
        else:
            messages.error(request, "Form errors")

    context = {
        'candidatesview': candidatesview,
        'form1': form,
        'page_title': 'Candidates'
    }
    return render(request, "candidatesview.html", context)

def candidate_view(request):
    candidate_id = request.GET.get('id', None)
    candidate = Candidate.objects.filter(id=candidate_id).first()
    context = {}
    if not candidate:
        context['code'] = 404
    else:
        context['code'] = 200
        context['id'] = candidate.id
        context['fullname'] = candidate.fullname
        form = CandidateForm(instance=candidate)
        context['form'] = form.as_p()
    return JsonResponse(context)

def Candidatesupdate(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
        return redirect('Candidateview')
    try:
        candidate_id = request.POST.get('id')
        candidate = Candidate.objects.get(id=candidate_id)
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, "Candidate Data Updated")
        else:
            messages.error(request, "Form has errors")
    except Candidate.DoesNotExist:
        messages.error(request, "Candidate not found")
    return redirect('Candidateview')

def Candidatesdelete(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
        return redirect('Candidateview')
    try:
        candidate = Candidate.objects.get(id=request.POST.get('id'))
        candidate.delete()
        messages.success(request, "Candidate Has Been Deleted")
    except Candidate.DoesNotExist:
        messages.error(request, "Candidate not found")
    return redirect('Candidateview')







def ViewVotes(request):
    votes = Votes.objects.all()
    context = {
        'votes': votes,
        'page_title': 'Votes'
    }
    return render(request, "votesview.html", context)


def ResetVote(request):
    Votes.objects.all().delete()
    Voter.objects.all().update(voted=False)
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
