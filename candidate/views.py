from django.shortcuts import render, redirect, get_object_or_404
from .forms import CampaignMessageForm
from .models import CampaignMessage

def dashboard(request):
    return render(request, "candidatedashboard.html")

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
            return view_campaign_messages
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
