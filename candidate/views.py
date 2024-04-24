# candidate/views.py

from django.shortcuts import render

def dashboard(request):
    return render(request, 'candidatedashboard.html')

from django.shortcuts import render, redirect
from .forms import CampaignMessageForm
from .models import CampaignMessage

def post_campaign_message(request):
    existing_message = None
    try:
        existing_message = CampaignMessage.objects.get(candidate=request.user)
    except CampaignMessage.DoesNotExist:
        pass

    if request.method == 'POST':
        form = CampaignMessageForm(request.POST, instance=existing_message)
        if form.is_valid():
            message = form.save(commit=False)
            message.candidate = request.user
            message.save()
            return redirect('view_campaign_messages')
    else:
        form = CampaignMessageForm(instance=existing_message)
    return render(request, 'post_campaign_message.html', {'form': form, 'existing_message': existing_message})


from django.shortcuts import render
from .models import CampaignMessage

def view_campaign_messages(request):
    messages = CampaignMessage.objects.all()
    return render(request, 'view_campaign_messages.html', {'messages': messages})
