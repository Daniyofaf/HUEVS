from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from board_member.models import ElectionResult
from voting.forms import CandidateForm
from voting.models import Candidate, Position, Voter
from .forms import CampaignMessageForm
from .models import CampaignMessage

def dashboard(request):
    positions = Position.objects.all().order_by('priority')
    candidates = Candidate.objects.all()
    voters = Voter.objects.all()
    list_of_candidates = []
  

    for position in positions:
        list_of_candidates = []
        for candidate in Candidate.objects.filter(position=position):
            list_of_candidates.append(candidate.fullname)
           
        

    context = {
        'position_count': positions.count(),
        'candidate_count': candidates.count(),
        'voters_count': voters.count(),
        'positions': positions,
        'page_title': "Dashboard"
    }
    return render(request, "result_page.html", context)

def post_campaign_message(request):
    try:
        existing_message = CampaignMessage.objects.get(candidate=request.user)
        # If an existing message is found, redirect to edit_message view
        return redirect('edit_message', message_id=existing_message.pk)
    except CampaignMessage.DoesNotExist:
        existing_message = None

    if request.method == 'POST':
        form = CampaignMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.candidate = request.user
            message.save()
            return redirect('view_campaign_messages')
    else:
        form = CampaignMessageForm()

    return render(request, 'post_campaign_message.html', {'form': form})



def view_campaign_messages(request):
    messages = CampaignMessage.objects.filter(candidate=request.user)
    return render(request, "view_campaign_messages.html", {"messages": messages})

def edit_message(request, message_id):
    message = get_object_or_404(CampaignMessage, pk=message_id, candidate=request.user)

    if request.method == "POST":
        form = CampaignMessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect("view_campaign_messages")
    else:
        form = CampaignMessageForm(instance=message)
    return render(request, "edit_campaign_message.html", {"form": form, "message": message})


def view_Candidate(request):
    candidatesview = Candidate.objects.all()
    context = {
        'candidatesview': candidatesview,
        'page_title': 'Candidates'
    }
 
    return render(request, "candidates.html", context)

# def viewcandidatebyid(request):
#     candidate_id = request.GET.get('id', None)
#     candidate = Candidate.objects.filter(id=candidate_id)
#     context = {}
#     if not candidate.exists():
#         context['code'] = 404
#     else:
#         candidate = candidate[0]
#         context['code'] = 200
#         context['fullname'] = candidate.fullname
#         previous = CandidateForm(instance=candidate)
#         context['form'] = str(previous.as_p())
#     return JsonResponse(context)


from administrator.views import PrintView  # Import the PrintView class

def result_page(request):
    resultpage = ElectionResult.objects.filter(isposted=True)
    falseresultpage = ElectionResult.objects.filter(isposted=False)
    # Instantiate the PrintView class to generate context data
    print_view = PrintView()
    # context = print_view.get_context_data()
    # context = {'resultpage' : resultpage}
    
    context = {**print_view.get_context_data(), 'resultpage': resultpage}


    # Render the template with the context data
    return render(request, "result_page.html", context)


