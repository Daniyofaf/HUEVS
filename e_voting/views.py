
from django.shortcuts import render



def homepage(request):
    welcome_message = "Welcome to the Voting System!"

    # context = {
    #     # 'welcome_message': welcome_message,
    # }

    return render(request, "voting/homepage.html")
